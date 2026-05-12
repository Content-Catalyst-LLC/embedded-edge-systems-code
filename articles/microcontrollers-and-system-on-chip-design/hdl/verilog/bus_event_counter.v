module bus_event_counter (
    input wire clk,
    input wire rst,
    input wire dma_event,
    input wire bus_stall,
    output reg [31:0] dma_count,
    output reg [31:0] bus_stall_count
);
always @(posedge clk) begin
    if (rst) begin
        dma_count <= 32'd0;
        bus_stall_count <= 32'd0;
    end else begin
        if (dma_event) begin
            dma_count <= dma_count + 32'd1;
        end
        if (bus_stall) begin
            bus_stall_count <= bus_stall_count + 32'd1;
        end
    end
end
endmodule
