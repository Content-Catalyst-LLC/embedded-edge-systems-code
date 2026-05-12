"""
Python Workflow: Digital Twin and Hardware-in-the-Loop Readiness Checks

This script checks whether minimum HIL and digital-twin readiness artifacts exist
and whether required validation dimensions are represented.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    hil = load_yaml(article_root / "config" / "hil_readiness.yml")["hardware_in_the_loop_readiness"]
    twin = load_yaml(article_root / "config" / "digital_twin_manifest.yml")["digital_twin"]

    hil_records = []
    for key, value in hil["required"].items():
        hil_records.append({
            "dimension": key,
            "ready": bool(value),
        })

    twin_records = []
    for label, path in twin["model_links"].items():
        twin_records.append({
            "model_link": label,
            "path": path,
            "exists": (article_root / path).exists(),
        })

    hil_df = pd.DataFrame(hil_records)
    twin_df = pd.DataFrame(twin_records)

    hil_df.to_csv(output_dir / "python_hil_readiness.csv", index=False)
    twin_df.to_csv(output_dir / "python_digital_twin_model_links.csv", index=False)

    summary = pd.DataFrame([{
        "hil_dimensions": len(hil_df),
        "hil_ready_rate": float(hil_df["ready"].mean()),
        "digital_twin_model_links": len(twin_df),
        "digital_twin_link_validity_rate": float(twin_df["exists"].mean()),
        "fault_injection_cases": len(hil.get("fault_injection_cases", [])),
    }]).round(4)

    summary.to_csv(output_dir / "python_hil_digital_twin_readiness_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
