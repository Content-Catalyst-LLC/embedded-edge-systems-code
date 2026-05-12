module inference_trigger (
    input wire clk,
    input wire rst,
    input wire window_ready,
    input wire runtime_ready,
    output reg trigger_inference
);

always @(posedge clk) begin
    if (rst) begin
        trigger_inference <= 0;
    end else begin
        trigger_inference <= window_ready && runtime_ready;
    end
end

endmodule
