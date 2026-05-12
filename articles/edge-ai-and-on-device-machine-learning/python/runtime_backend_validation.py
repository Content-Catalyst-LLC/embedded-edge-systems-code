"""
Python Workflow: Runtime and Accelerator Backend Validation

This script validates backend parity using reference, quantized, CPU, NPU, DSP,
and PYNQ/FPGA outputs.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    validation = pd.read_csv(article_root / "data" / "backend_validation_report.csv")
    config = yaml.safe_load((article_root / "config" / "backend_validation.yml").read_text(encoding="utf-8"))["backend_validation"]

    output_columns = ["quantized_output", "cpu_output", "npu_output", "dsp_output", "pynq_output"]
    validation["computed_max_backend_delta"] = validation[output_columns].sub(validation["reference_output"], axis=0).abs().max(axis=1)
    validation["delta_passed"] = validation["computed_max_backend_delta"] <= config["max_backend_output_delta"]
    validation["validation_passed"] = validation["delta_passed"] & validation["class_agreement"]

    validation.to_csv(output_dir / "python_runtime_backend_validation.csv", index=False)

    summary = pd.DataFrame([{
        "tests": len(validation),
        "backend_delta_pass_rate": validation["delta_passed"].mean(),
        "class_agreement_rate": validation["class_agreement"].mean(),
        "overall_pass_rate": validation["validation_passed"].mean(),
        "max_observed_delta": validation["computed_max_backend_delta"].max(),
        "max_allowed_delta": config["max_backend_output_delta"],
    }]).round(4)

    summary.to_csv(output_dir / "python_runtime_backend_validation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
