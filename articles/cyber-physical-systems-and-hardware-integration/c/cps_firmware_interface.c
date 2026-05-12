/*
 * C Example: Sensor Read, Command Filter, Watchdog, Actuator Update, and Timing Checks
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float speed_rpm;
    float sample_age_ms;
    bool calibration_valid;
} SensorReading;

typedef struct {
    float candidate_command;
    float previous_command;
    float current_a;
    float temperature_c;
    float deadline_slack_ms;
    float total_uncertainty;
    float uncertainty_budget;
} CpsContext;

float clamp(float value, float low, float high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

float cps_command_filter(CpsContext ctx, const char **reason) {
    if (ctx.deadline_slack_ms < 0.0f) {
        *reason = "deadline_miss_safe_stop";
        return 0.0f;
    }

    if (ctx.total_uncertainty > ctx.uncertainty_budget) {
        *reason = "uncertainty_budget_violation";
        return clamp(ctx.previous_command, 0.0f, 0.5f);
    }

    if (ctx.temperature_c >= 80.0f) {
        *reason = "thermal_fault_safe_stop";
        return 0.0f;
    }

    if (ctx.temperature_c >= 70.0f) {
        *reason = "thermal_derate";
        return clamp(ctx.candidate_command, 0.0f, 0.75f);
    }

    if (ctx.current_a >= 4.0f) {
        *reason = "current_limit_clip";
        return clamp(ctx.previous_command, 0.0f, 0.50f);
    }

    *reason = "allowed";
    return clamp(ctx.candidate_command, 0.0f, 1.0f);
}

int main(void) {
    SensorReading reading = {
        .speed_rpm = 1110.0f,
        .sample_age_ms = 1.2f,
        .calibration_valid = true
    };

    if (!reading.calibration_valid || reading.sample_age_ms > 3.0f) {
        printf("Sensor invalid; safe stop required.\n");
        return 0;
    }

    float setpoint = 1200.0f;
    float error = setpoint - reading.speed_rpm;
    float candidate = 0.0025f * error;

    CpsContext ctx = {
        .candidate_command = candidate,
        .previous_command = 0.40f,
        .current_a = 2.1f,
        .temperature_c = 55.0f,
        .deadline_slack_ms = 0.62f,
        .total_uncertainty = 24.0f,
        .uncertainty_budget = 35.0f
    };

    const char *reason = "allowed";
    float filtered = cps_command_filter(ctx, &reason);

    printf("Candidate command: %.3f\n", candidate);
    printf("Filtered command: %.3f\n", filtered);
    printf("Reason: %s\n", reason);

    return 0;
}
