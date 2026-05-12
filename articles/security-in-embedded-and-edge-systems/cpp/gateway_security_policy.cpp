/*
 * C++ Example: Gateway Security Policy and Boundary Check
 */

#include <iostream>
#include <string>

struct Request {
    std::string device_id;
    bool mutual_auth;
    bool signed_payload;
    bool management_channel;
    bool privileged_operation;
};

bool allow_request(const Request& request) {
    if (!request.mutual_auth || !request.signed_payload) {
        return false;
    }

    if (request.privileged_operation && !request.management_channel) {
        return false;
    }

    return true;
}

int main() {
    Request telemetry{"gw-chi-001", true, true, false, false};
    Request update{"gw-chi-001", true, true, true, true};

    std::cout << "Telemetry request allowed: " << (allow_request(telemetry) ? "yes" : "no") << "\n";
    std::cout << "Update request allowed: " << (allow_request(update) ? "yes" : "no") << "\n";

    return 0;
}
