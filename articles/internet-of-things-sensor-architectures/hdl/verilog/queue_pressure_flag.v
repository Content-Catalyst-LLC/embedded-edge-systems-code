module queue_pressure_flag #(
    parameter WIDTH = 16,
    parameter THRESHOLD = 800
)(
    input wire [WIDTH-1:0] queue_depth,
    output wire queue_pressure
);
assign queue_pressure = queue_depth >= THRESHOLD;
endmodule
