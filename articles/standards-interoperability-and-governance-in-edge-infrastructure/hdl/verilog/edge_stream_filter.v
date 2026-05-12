/*
 * Verilog Example: Edge Stream Threshold Filter
 *
 * This simple module represents a hardware-level stream filter that flags values
 * above a configured threshold. It is a scaffold for edge preprocessing,
 * anomaly detection, or FPGA-backed telemetry pipelines.
 */

module edge_stream_filter #(
    parameter DATA_WIDTH = 16,
    parameter THRESHOLD = 16'd1000
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] data_in,
    output reg valid_out,
    output reg [DATA_WIDTH-1:0] data_out,
    output reg alert_out
);

always @(posedge clk) begin
    if (rst) begin
        valid_out <= 1'b0;
        data_out <= {DATA_WIDTH{1'b0}};
        alert_out <= 1'b0;
    end else begin
        valid_out <= valid_in;
        data_out <= data_in;
        alert_out <= valid_in && (data_in > THRESHOLD);
    end
end

endmodule
