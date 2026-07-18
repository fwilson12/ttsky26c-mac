/*
 * Copyright (c) 2026 Fletcher Wilson
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_fwilson12_mac (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // TODO (wrapper): instantiate `mac` here and map its clean ports to the TT pins.
  //   - clk, rst_n pass straight through.
  //   - operands a, b: decide how to feed them across the 8-bit ui_in / uio_in budget.
  //   - acc is wider than 8 bits, so expose a selected byte on uo_out.
  // The example passthrough below keeps the build green until the wrapper is wired:

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // placeholder
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
