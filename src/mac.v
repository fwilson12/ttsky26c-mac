`default_nettype none
// Multiply-accumulate: acc <- acc + (a * b) on each enabled cycle.
module mac #(
    parameter IN_WIDTH  = 8,
    parameter ACC_WIDTH = 32
) (
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 en,     // accumulate this cycle
    input  wire [IN_WIDTH-1:0]  a,
    input  wire [IN_WIDTH-1:0]  b,
    output wire [ACC_WIDTH-1:0] acc
);
    // TODO
endmodule
`default_nettype wire
