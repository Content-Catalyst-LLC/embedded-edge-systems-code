use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/task_manifest.json").expect("unable to read task manifest");
    let manifest: Value = serde_json::from_str(&raw).expect("task manifest is not valid json");

    let tasks = manifest["tasks"].as_array().expect("tasks must be an array");
    assert!(!tasks.is_empty(), "at least one task is required");

    for task in tasks {
        assert!(task["task_name"].is_string(), "task_name required");
        assert!(task["criticality"].is_string(), "criticality required");
        assert!(task["priority"].is_number(), "priority required");
        assert!(task["period_ms"].is_number(), "period_ms required");
        assert!(task["deadline_ms"].is_number(), "deadline_ms required");
        assert!(task["wcet_ms"].is_number(), "wcet_ms required");
        assert!(task["blocking_ms"].is_number(), "blocking_ms required");
        assert!(task["stack_bytes"].is_number(), "stack_bytes required");
        assert!(task["watchdog_required"].is_boolean(), "watchdog requirement required");
    }

    println!("validated {} RTOS task contracts", tasks.len());
}
