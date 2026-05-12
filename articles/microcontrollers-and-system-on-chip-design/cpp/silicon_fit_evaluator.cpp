#include <iostream>
#include <string>

struct Platform {
    std::string name;
    double cpu_mhz;
    double flash_kb;
    double sram_kb;
    double bandwidth_mb_s;
    double active_ma;
    double sleep_ua;
    bool secure_boot;
    bool key_storage;
};

struct Requirement {
    double cpu_mhz;
    double flash_kb;
    double sram_kb;
    double bandwidth_mb_s;
    double max_active_ma;
    double max_sleep_ua;
    bool needs_secure_boot;
    bool needs_key_storage;
};

double fit_score(const Platform& p, const Requirement& r) {
    double score = 0.0;
    score += p.cpu_mhz >= r.cpu_mhz;
    score += p.flash_kb >= r.flash_kb;
    score += p.sram_kb >= r.sram_kb;
    score += p.bandwidth_mb_s >= r.bandwidth_mb_s;
    score += p.active_ma <= r.max_active_ma;
    score += p.sleep_ua <= r.max_sleep_ua;
    score += (!r.needs_secure_boot || p.secure_boot);
    score += (!r.needs_key_storage || p.key_storage);
    return score / 8.0;
}

int main() {
    Platform p{"hybrid_control_soc_f", 600, 2048, 768, 900, 120, 80, true, true};
    Requirement r{400, 1024, 512, 600, 250, 200, true, true};

    std::cout << p.name << " fit_score=" << fit_score(p, r) << "\n";
    return 0;
}
