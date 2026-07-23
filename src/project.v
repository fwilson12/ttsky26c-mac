/*
 * Copyright (c) 2026 Fletcher Wilson
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_fwilson12_mac (
    input signed wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
	);

	// All output pins must be assigned. If not used, assign to 0.
	assign uio_oe = 8'd0;
	//



	reg signed [23:0] acc = 24'd0;
	reg signed [7:0] a = 8'h00;
	reg phase = 1'b0;

	always @(posedge clk) begin
		
		// active lo sync reset
		if (!rst_n) begin
			acc <= 24'd0;
			a <= 8'd0;
			phase = 1'b0;
		end
		
		// doin somethin 
		else begin
		
			if (phase) 
				acc <= acc + (a * ui_in);
		
			else begin
				a <= ui_in;
				phase <= ~phase;
			end
		end
	end


	assign {uio_out, uo_out} = acc[15:0]

	// List all unused inputs to prevent warnings
	wire _unused = &{ena, uio_in, 1'b0};

endmodule
