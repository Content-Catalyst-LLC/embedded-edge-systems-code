module acquisition_timestamp_counter (
    input wire clk,
    input wire rst,
    input wire sample_valid,
    output reg [31:0] timestamp_counter,
    output reg [31:0] sample_counter
);
always @(posedge clk) begin
    if (rst) begin
        timestamp_counter <= 32'd0;
        sample_counter <= 32'd0;
    end else begin
        timestamp_counter <= timestamp_counter + 32'd1;
        if (sample_valid) begin
            sample_counter <= sample_counter + 32'd1;
        end
    end
end
endmodule
