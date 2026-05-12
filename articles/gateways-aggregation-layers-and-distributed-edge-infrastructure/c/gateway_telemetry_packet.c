/*
 * C Example: Telemetry Packet Formation, Child Heartbeat, and Buffer Watermark Checking
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    char device_id[32];
    char gateway_id[32];
    char protocol_family[16];
    float measurement;
    char unit[16];
    unsigned int freshness_s;
    bool protocol_error;
    bool lineage_complete;
} TelemetryEvent;

typedef struct {
    unsigned int buffer_backlog;
    unsigned int high_watermark;
    unsigned int max_buffer;
} BufferStatus;

bool child_heartbeat_valid(TelemetryEvent event, unsigned int expected_heartbeat_s) {
    return event.freshness_s <= expected_heartbeat_s;
}

bool buffer_high_watermark(BufferStatus status) {
    return status.buffer_backlog >= status.high_watermark;
}

void print_packet(TelemetryEvent event, BufferStatus buffer) {
    printf("device_id=%s\n", event.device_id);
    printf("gateway_id=%s\n", event.gateway_id);
    printf("protocol=%s\n", event.protocol_family);
    printf("measurement=%.2f %s\n", event.measurement, event.unit);
    printf("freshness_s=%u\n", event.freshness_s);
    printf("protocol_error=%s\n", event.protocol_error ? "true" : "false");
    printf("lineage_complete=%s\n", event.lineage_complete ? "true" : "false");
    printf("buffer_backlog=%u\n", buffer.buffer_backlog);
    printf("buffer_high_watermark=%s\n", buffer_high_watermark(buffer) ? "true" : "false");
}

int main(void) {
    TelemetryEvent event;
    strcpy(event.device_id, "dev-vib-001");
    strcpy(event.gateway_id, "gw-001");
    strcpy(event.protocol_family, "spi");
    event.measurement = 0.43f;
    strcpy(event.unit, "g");
    event.freshness_s = 3;
    event.protocol_error = false;
    event.lineage_complete = true;

    BufferStatus buffer = {
        .buffer_backlog = 205,
        .high_watermark = 200,
        .max_buffer = 500
    };

    print_packet(event, buffer);
    printf("heartbeat_valid=%s\n", child_heartbeat_valid(event, 10) ? "true" : "false");

    return 0;
}
