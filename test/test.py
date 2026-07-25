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

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")


    vec1, vec2 = randomVecs()
    ref = dotProd(vec1, vec2)
    acc_sum = 0

    for i in range(len(vec1)):

        curLo = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())
        dut.ui_in.value = LogicArray.from_signed(vec1[i], 8)
        await ClockCycles(dut.clk, 1)
        await Timer(5, unit="ns") 

        currHi = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())
        dut.ui_in.value = LogicArray.from_signed(vec2[i], 8)
        await ClockCycles(dut.clk, 1)
        await Timer(5, unit="ns") 

        chip_acc = merge(currHi, curLo)
        assert acc_sum == chip_acc, f"Mismatch check at pair {i}: current sum should be {acc_sum} but was {chip_acc}"

        acc_sum += vec1[i] * vec2[i]


    lastLo = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())
    await ClockCycles(dut.clk, 1)
    await Timer(5, unit="ns") 

    lastHi = (dut.uio_out.value.to_unsigned() << 8) | (dut.uo_out.value.to_unsigned())

    chip_acc = merge(lastHi, lastLo)

    assert ref == chip_acc
    
     
