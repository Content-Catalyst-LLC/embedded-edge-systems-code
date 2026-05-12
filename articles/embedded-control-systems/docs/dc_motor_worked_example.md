# Worked Example: DC Motor Speed-Control Loop

This example models a DC motor speed-control loop.

## Loop structure

1. A supervisor requests a speed setpoint.
2. Encoder pulses are converted into measured speed.
3. A filter or estimator creates an operational speed estimate.
4. A PID controller computes a candidate PWM duty cycle.
5. A safety filter clips or rejects unsafe commands.
6. The motor driver receives the filtered PWM command.
7. The loop logs timing, error, command, saturation, current, temperature, and supervisory state.

## Key signals

- target speed
- measured speed
- estimated speed
- control error
- candidate command
- filtered command
- saturation flag
- loop period
- loop jitter
- deadline slack
- safety-filter reason code
- supervisory state
