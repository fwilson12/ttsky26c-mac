`default_nettype none
// N-bit register with enable and active-low synchronous reset.
// This is the MAC's accumulator storage.
module register_en #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst_n,   // active-low reset
    input  wire             en,      // load d when high, otherwise hold
    input  wire [WIDTH-1:0] d,
    output reg  [WIDTH-1:0] q
);
    // TODO
endmodule
`default_nettype wire
