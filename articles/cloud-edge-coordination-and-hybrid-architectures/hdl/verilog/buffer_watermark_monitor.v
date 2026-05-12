module buffer_watermark_monitor #(
    parameter COUNT_WIDTH = 16,
    parameter HIGH_WATERMARK = 200
)(
    input wire [COUNT_WIDTH-1:0] buffer_count,
    output wire high_watermark,
    output wire uplink_pressure
);

assign high_watermark = buffer_count >= HIGH_WATERMARK;
assign uplink_pressure = high_watermark;

endmodule
