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

	// all 8 bits of bdir are input
	assign uio_oe = 8'hFF;



	reg signed [23:0] acc = 24'd0;
	reg signed [7:0] a = 8'h00;
	reg phase = 1'b0;

	always @(posedge clk) begin
		
		// active lo sync reset
		if (!rst_n) begin
			acc <= 24'sd0;
			a <= 8'sd0;
			phase <= 1'b0;
		end
		
		// doin somethin 
		else begin
			// phase is high: component a is loaded, component b is at ui_in; multiply them and add to accum 
			if (phase) 
				acc <= acc + (a * $signed(ui_in));

			// phase is low; old component a is loaded, new component a is at ui_in; load it
			else 
				a <= $signed(ui_in);
			
			// update phase state
			phase <= ~phase;

		end
	end

	// low two bytes when phase is low, high two bytes when phase is high
	assign {uio_out, uo_out} = phase ? acc[23:8] : acc[15:0];

	// List all unused inputs to prevent warnings
	wire _unused = &{ena, uio_in, 1'b0};

endmodule
