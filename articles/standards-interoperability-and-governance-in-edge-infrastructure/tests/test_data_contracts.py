from pathlib import Path
import pandas as pd


def test_sample_edge_assets_required_columns():
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / "data" / "sample_edge_assets.csv")

    required = {
        "device_id",
        "site",
        "vendor",
        "device_class",
        "standard_profile",
        "protocol_conformance",
        "semantic_alignment",
        "lifecycle_control",
        "security_baseline",
        "operational_accountability",
        "unmanaged_divergence",
        "support_state",
        "firmware_version",
        "schema_version",
    }

    assert required.issubset(set(data.columns))


def test_scores_are_unit_interval_inputs():
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / "data" / "sample_edge_assets.csv")

    score_columns = [
        "protocol_conformance",
        "semantic_alignment",
        "lifecycle_control",
        "security_baseline",
        "operational_accountability",
        "unmanaged_divergence",
    ]

    for column in score_columns:
        assert data[column].between(0, 1).all()
