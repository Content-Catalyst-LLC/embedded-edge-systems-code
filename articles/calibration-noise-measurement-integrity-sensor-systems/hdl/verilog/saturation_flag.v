module saturation_flag #(
    parameter WIDTH = 16
)(
    input wire [WIDTH-1:0] sample,
    output wire saturated
);
assign saturated = (sample == {WIDTH{1'b0}}) || (sample == {WIDTH{1'b1}});
endmodule
