from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    policy = yaml.safe_load((root / "config/command_authority_policy.yml").read_text())["command_authority_policy"]
    commands = pd.read_csv(root / "data/command_log.csv")

    def evaluate(row):
        command_type = row["command_type"]
        requirements = policy["command_types"].get(command_type, {})
        issues = []

        if requirements.get("requires_verified_trust", False) and row["trust_state"] != "verified":
            issues.append("unverified_trust")
        if requirements.get("requires_fresh_state", False) and row["observed_freshness_seconds"] > row["freshness_required_seconds"]:
            issues.append("stale_state")
        if requirements.get("requires_local_safety_check", False) and not bool(row["local_safety_check"]):
            issues.append("failed_local_safety_check")
        if requirements.get("requires_acknowledgment", False) and not bool(row["acknowledged"]):
            issues.append("missing_acknowledgment")
        if requirements.get("requires_rollback_ready", False) and not bool(row["rollback_ready"]):
            issues.append("rollback_not_ready")
        if not bool(row["authorized"]):
            issues.append("not_authorized")

        return issues or ["accepted"]

    commands["authority_evaluation"] = commands.apply(evaluate, axis=1)
    commands["safe_to_execute"] = commands["authority_evaluation"].apply(lambda issues: issues == ["accepted"])
    commands["blocked_by_policy"] = ~commands["safe_to_execute"]

    commands.to_csv(out / "python_command_authority_safety_boundary_evaluation.csv", index=False)

    summary = pd.DataFrame([{
        "commands": len(commands),
        "safe_to_execute_rate": commands["safe_to_execute"].mean(),
        "blocked_by_policy_rate": commands["blocked_by_policy"].mean(),
        "acknowledged_rate": commands["acknowledged"].mean(),
        "rollback_ready_rate": commands["rollback_ready"].mean()
    }]).round(4)
    summary.to_csv(out / "python_command_authority_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
