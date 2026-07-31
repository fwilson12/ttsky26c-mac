# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer
from cocotb.types import LogicArray

from helpers import merge, dotProd, randomVecs



@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    async def reset():
        # Reset
        dut._log.info("Reset")
        dut.ena.value = 1
        dut.ui_in.value = 0
        dut.uio_in.value = 0
        dut.rst_n.value = 0
        await ClockCycles(dut.clk, 10)
        dut.rst_n.value = 1

    async def test(vec1: list[int], vec2: list[int], name: str) -> None:
        """
        Given two test vectors (5-511 dimensions, values in [-128, 127]) as lists,
        calculate their dot product, then stream them through the chip one pair at a time, 
        validating the chip's accumulator reg as it goes.
        
        Due to the pin constraints, both the inputs and outputs are time-multiplexed based on a two-state FSM:
            Phase 0: 
                Input: The nth component of vec1 is read from ui_in (signed int8) and stored in an internal buffer reg.
                
                Output: The low 16 bits of the chip's 24-bit accumulator register from the previous state (accumulator after adding the product of the n-1th pair)
                        are read as output and stored per-iteration. The middle byte is read from uio_out, and the low byte from uo_out.
            
            Phase 1:
                Input: The nth component of vec2 is read from ui_in, and is multiplied with the value stored in the chip's buffer reg. The product is then added to the 
                       accumulator reg. Note that this happens after the previous accumulator's value is read and stored, so this round's accumulator update won't be read until 
                       the next phase cycle.

                Output: The high 16 bits of the accumulator's previous state are read; high byte from uio_out, middle byte from uo_out. Note that we've captured the middle byte of the 24-bit
                        reg twice; while just a by-product of capturing a 3 byte output by reading two pairs of two bytes, when the high two bytes are merged with the low two bytes to reconstruct
                        the accumulator's true three-byte value, the (hopefully) shared byte is useful for extra validation.
        """

        # expected values 
        ref = dotProd(vec1, vec2)
        acc_sum = 0

    
        await reset()

        # for each component pair
        for i in range(len(vec1)):

            # phase = 0: the low 16 bits of the past acc state are sent out via the bdir out pins (hi 8 bits) and the dedicated out pins (lo 8 bits)
            curLo = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned()) # shift high byte to its place, merge w/ low byte
            dut.ui_in.value = LogicArray.from_signed(vec1[i], 8) # expose first component of new pair, chip loads it to its reg

            # next clk edge
            await ClockCycles(dut.clk, 1)
            await Timer(5, unit="ns") 

            # phase = 1: the high 16 bits of past acc state are visible: upper 8 via bdir uio_out, lower 8 via uo_out
            currHi = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned()) # same shift; upper byte shited up to its place and merged w/ low byte
            dut.ui_in.value = LogicArray.from_signed(vec2[i], 8) # expose second component of new pair, chip performs the multiplication and adds to the acc register

            # back to phase 0; the results from the multiplication/addition that just occured will be visible upon the next iteration 
            await ClockCycles(dut.clk, 1)
            await Timer(5, unit="ns") 

            # take the high two and low two bytes from the past acc reg's state and merge them at their middle byte, giving us a 24-bit value for what the acc reg currently stores. assert it matches the python model
            chip_acc = merge(currHi, curLo)
            assert acc_sum == chip_acc, f"Mismatch check at pair {i}: current sum should be {acc_sum} but was {chip_acc}"

            # add component product to running ref. sum
            acc_sum += vec1[i] * vec2[i]

        # the final iteration's accumulator update still needs two more clk edges to read the final value, since the ith sum is read on the i + 1th iter
        lastLo = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())
        await ClockCycles(dut.clk, 1)
        await Timer(5, unit="ns") 
        lastHi = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())

        # final accumulator readout
        chip_acc = merge(lastHi, lastLo, name)

        # final check
        assert ref == chip_acc, f"Failed for test: {name} | expected {ref} but read {chip_acc}"


    dut._log.info("Test project behavior")
    
    # random test run
    randVec1, randVec2 = randomVecs()
    await test(randVec1, randVec2, "random")

    # max pos value edge case
    maxVec1 = [-128] * 511
    maxVec2 = [-128] * 511
    await test(maxVec1, maxVec2, "max positive")

    # max neg value edge case
    nMaxVec1 = [127] * 511
    nMaxVec2 = [-128] * 511
    await test(nMaxVec1, nMaxVec2, "max negative")

    # zeros
    zeroVec1 = [0] * 100
    zeroVec2 = [42] * 100
    await test (zeroVec1, zeroVec2, "zeros")