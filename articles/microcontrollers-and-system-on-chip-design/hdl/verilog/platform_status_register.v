module platform_status_register (
    input wire clk,
    input wire rst,
    input wire secure_boot_ok,
    input wire debug_locked,
    input wire update_slot_valid,
    input wire power_domain_ready,
    output reg [31:0] status
);
always @(posedge clk) begin
    if (rst) begin
        status <= 32'd0;
    end else begin
        status[0] <= secure_boot_ok;
        status[1] <= debug_locked;
        status[2] <= update_slot_valid;
        status[3] <= power_domain_ready;
    end
end
endmodule
