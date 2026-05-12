/*
 * C Example: Embedded PID Control Loop with Saturation and Anti-Windup
 *
 * This is a constrained-control scaffold intended for embedded robotics examples.
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float kp;
    float ki;
    float kd;
    float dt;
    float command_limit;
    float integral;
    float previous_error;
} PIDController;

float clamp(float value, float min_value, float max_value) {
    if (value > max_value) return max_value;
    if (value < min_value) return min_value;
    return value;
}

float pid_step(PIDController *controller, float reference, float measurement, bool *saturated) {
    float error = reference - measurement;
    float integral_candidate = controller->integral + error * controller->dt;
    float derivative = (error - controller->previous_error) / controller->dt;

    float raw_command =
        controller->kp * error +
        controller->ki * integral_candidate +
        controller->kd * derivative;

    float command = clamp(raw_command, -controller->command_limit, controller->command_limit);
    *saturated = (command != raw_command);

    if (!(*saturated)) {
        controller->integral = integral_candidate;
    }

    controller->previous_error = error;
    return command;
}

int main(void) {
    PIDController controller = {
        .kp = 4.0f,
        .ki = 0.7f,
        .kd = 0.15f,
        .dt = 0.01f,
        .command_limit = 1.0f,
        .integral = 0.0f,
        .previous_error = 0.0f
    };

    bool saturated = false;
    float command = pid_step(&controller, 0.50f, 0.42f, &saturated);

    printf("Command: %.3f\n", command);
    printf("Saturated: %s\n", saturated ? "true" : "false");

    return 0;
}
