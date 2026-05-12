/*
 * C++ Example: Robotic State Machine and Command Validation
 */

#include <iostream>
#include <string>
#include <cmath>

enum class RobotState {
    Idle,
    Tracking,
    Warning,
    SafeStop,
    Fault
};

struct MotionCommand {
    double position;
    double velocity;
    double command;
};

struct SafetyEnvelope {
    double position_min;
    double position_max;
    double velocity_max_abs;
    double command_max_abs;
};

bool validate_command(const MotionCommand& cmd, const SafetyEnvelope& env) {
    return cmd.position >= env.position_min &&
           cmd.position <= env.position_max &&
           std::abs(cmd.velocity) <= env.velocity_max_abs &&
           std::abs(cmd.command) <= env.command_max_abs;
}

std::string state_name(RobotState state) {
    switch (state) {
        case RobotState::Idle: return "Idle";
        case RobotState::Tracking: return "Tracking";
        case RobotState::Warning: return "Warning";
        case RobotState::SafeStop: return "SafeStop";
        case RobotState::Fault: return "Fault";
    }
    return "Unknown";
}

int main() {
    SafetyEnvelope env{-1.0, 1.0, 1.5, 1.0};
    MotionCommand cmd{0.42, 0.35, 0.80};

    RobotState state = validate_command(cmd, env) ? RobotState::Tracking : RobotState::SafeStop;

    std::cout << "Command valid: " << (validate_command(cmd, env) ? "yes" : "no") << "\n";
    std::cout << "Robot state: " << state_name(state) << "\n";

    return 0;
}
