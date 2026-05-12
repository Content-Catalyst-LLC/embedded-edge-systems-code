/*
 * C++ Example: Semantic Gateway Profile Validation
 *
 * This example shows how a gateway might validate whether an incoming telemetry
 * record contains the semantic fields required by a local interoperability profile.
 */

#include <iostream>
#include <set>
#include <string>
#include <vector>

class InterfaceProfile {
public:
    explicit InterfaceProfile(std::set<std::string> required_fields)
        : required_fields_(std::move(required_fields)) {}

    std::vector<std::string> missing_fields(const std::set<std::string>& observed_fields) const {
        std::vector<std::string> missing;

        for (const auto& field : required_fields_) {
            if (observed_fields.find(field) == observed_fields.end()) {
                missing.push_back(field);
            }
        }

        return missing;
    }

private:
    std::set<std::string> required_fields_;
};

int main() {
    InterfaceProfile profile({
        "device_id",
        "timestamp",
        "metric",
        "value",
        "unit",
        "quality_flag",
        "schema_version"
    });

    std::set<std::string> observed = {
        "device_id",
        "timestamp",
        "metric",
        "value",
        "unit"
    };

    auto missing = profile.missing_fields(observed);

    if (missing.empty()) {
        std::cout << "Semantic profile validation: PASS\n";
    } else {
        std::cout << "Semantic profile validation: REVIEW\nMissing fields:\n";
        for (const auto& field : missing) {
            std::cout << "- " << field << "\n";
        }
    }

    return 0;
}
