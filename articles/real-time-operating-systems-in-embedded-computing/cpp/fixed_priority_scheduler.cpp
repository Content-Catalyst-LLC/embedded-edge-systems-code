#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Task {
    std::string name;
    int priority;
    double period_ms;
    double deadline_ms;
    double wcet_ms;
    double blocking_ms;
};

int main() {
    std::vector<Task> tasks = {
        {"watchdog_supervisor", 0, 100, 80, 1.5, 0.1},
        {"control_loop", 1, 20, 20, 3.5, 0.8},
        {"sensor_acquisition", 2, 50, 40, 4.2, 0.5},
        {"radio_service", 4, 200, 150, 18.0, 5.0},
        {"storage_writer", 5, 500, 400, 30.0, 12.0}
    };

    std::sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        return a.priority < b.priority;
    });

    for (const auto& task : tasks) {
        double interference = 0.0;
        for (const auto& hp : tasks) {
            if (hp.priority < task.priority) {
                interference += hp.wcet_ms;
            }
        }
        double response = task.wcet_ms + task.blocking_ms + interference;
        bool ok = response <= task.deadline_ms;
        std::cout << task.name << " response_ms=" << response
                  << " deadline_ms=" << task.deadline_ms
                  << " schedulable_basic=" << (ok ? "true" : "false") << "\n";
    }

    return 0;
}
