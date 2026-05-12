/*
 * C Example: Embedded PID Loop with Anti-Windup, Command Clipping, and Watchdog Checks
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float kp;
    float ki;
    float kd;
    float dt;
    float command_min;
    float command_max;
    float integral;
    float previous_error;
    float previous_command;
} PIDController;

typedef struct {
    float current_a;
    float temperature_c;
    bool deadline_missed;
} SafetyContext;

float clamp(float value, float low, float high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

float safety_filter(float candidate, SafetyContext context, const char **reason) {
    if (context.deadline_missed) {
        *reason = "deadline_miss_safe_stop";
        return 0.0f;
    }

    if (context.temperature_c >= 80.0f) {
        *reason = "thermal_fault_safe_stop";
        return 0.0f;
    }

    if (context.temperature_c >= 70.0f) {
        *reason = "thermal_derate";
        return clamp(candidate, 0.0f, 0.75f);
    }

    if (context.current_a >= 4.0f) {
        *reason = "current_limit_clip";
        return clamp(candidate, 0.0f, 0.50f);
    }

    *reason = "allowed";
    return clamp(candidate, 0.0f, 1.0f);
}

float pid_step(PIDController *pid, float setpoint, float measurement, SafetyContext context, bool *saturated, const char **reason) {
    float error = setpoint - measurement;
    float integral_candidate = pid->integral + error * pid->dt;
    float derivative = (error - pid->previous_error) / pid->dt;

    float candidate =
        pid->kp * error +
        pid->ki * integral_candidate +
        pid->kd * derivative;

    float filtered = safety_filter(candidate, context, reason);

    *saturated = (filtered != candidate);

    if (!(*saturated)) {
        pid->integral = integral_candidate;
    }

    pid->previous_error = error;
    pid->previous_command = filtered;

    return filtered;
}

int main(void) {
    PIDController pid = {
        .kp = 0.0025f,
        .ki = 0.018f,
        .kd = 0.00008f,
        .dt = 0.001f,
        .command_min = 0.0f,
        .command_max = 1.0f,
        .integral = 0.0f,
        .previous_error = 0.0f,
        .previous_command = 0.0f
    };

    SafetyContext context = {
        .current_a = 3.1f,
        .temperature_c = 55.0f,
        .deadline_missed = false
    };

    bool saturated = false;
    const char *reason = "allowed";

    float pwm = pid_step(&pid, 1200.0f, 1080.0f, context, &saturated, &reason);

    printf("Filtered PWM command: %.3f\n", pwm);
    printf("Saturated: %s\n", saturated ? "true" : "false");
    printf("Safety filter reason: %s\n", reason);

    return 0;
}
