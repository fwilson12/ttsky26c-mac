`default_nettype none
// Unsigned combinational multiplier: WIDTH x WIDTH -> 2*WIDTH product.
module multiplier #(
    parameter WIDTH = 8
) (
    input  wire [WIDTH-1:0]   a,
    input  wire [WIDTH-1:0]   b,
    output wire [2*WIDTH-1:0] product
);
    // TODO
endmodule
`default_nettype wire
