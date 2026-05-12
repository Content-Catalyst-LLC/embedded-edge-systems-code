"""
Python Workflow: Requirements Traceability Matrix Validation

This script checks whether each CPS requirement is linked to an implementation
artifact, validation test, operational signal, and coverage status.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "requirement_id",
    "requirement",
    "implementation_artifact",
    "validation_test",
    "operational_signal",
    "status",
]


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    matrix = pd.read_csv(article_root / "data" / "requirements_traceability_matrix.csv")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in matrix.columns]
    if missing_columns:
        raise ValueError(f"Missing traceability columns: {missing_columns}")

    matrix["artifact_exists"] = matrix["implementation_artifact"].apply(lambda p: (article_root / p).exists())
    matrix["validation_exists"] = matrix["validation_test"].apply(lambda p: (article_root / p).exists())
    matrix["covered"] = (
        (matrix["status"].str.lower() == "covered")
        & matrix["artifact_exists"]
        & matrix["validation_exists"]
        & matrix["operational_signal"].notna()
    )

    matrix.to_csv(output_dir / "python_traceability_matrix_validation.csv", index=False)

    summary = pd.DataFrame([{
        "requirements": len(matrix),
        "covered_requirements": int(matrix["covered"].sum()),
        "coverage_rate": float(matrix["covered"].mean()),
        "missing_artifacts": int((~matrix["artifact_exists"]).sum()),
        "missing_validation_tests": int((~matrix["validation_exists"]).sum()),
    }]).round(4)

    summary.to_csv(output_dir / "python_traceability_matrix_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
