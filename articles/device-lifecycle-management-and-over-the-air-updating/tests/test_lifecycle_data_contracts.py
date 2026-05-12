from pathlib import Path
import pandas as pd


def test_device_fleet_required_columns():
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / "data" / "sample_device_fleet.csv")

    required = {
        "device_id",
        "site",
        "vendor",
        "device_class",
        "hardware_rev",
        "current_firmware",
        "target_firmware",
        "support_state",
        "rollout_ring",
        "identity_assurance",
        "compatibility_match",
        "package_integrity",
        "validation_status",
        "rollback_readiness",
        "observability",
        "lifecycle_drift",
        "last_checkin_hours",
    }

    assert required.issubset(set(data.columns))


def test_readiness_inputs_are_unit_interval():
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / "data" / "sample_device_fleet.csv")

    score_columns = [
        "identity_assurance",
        "compatibility_match",
        "package_integrity",
        "validation_status",
        "rollback_readiness",
        "observability",
        "lifecycle_drift",
    ]

    for column in score_columns:
        assert data[column].between(0, 1).all()
