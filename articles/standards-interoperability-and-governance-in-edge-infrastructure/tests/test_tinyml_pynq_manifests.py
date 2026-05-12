from pathlib import Path
import json


def test_tinyml_model_manifest_has_governance_fields():
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "tinyml" / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert "model_name" in manifest
    assert "model_version" in manifest
    assert "governance" in manifest
    assert manifest["governance"]["fallback_required"] is True
    assert manifest["governance"]["requires_manifest_validation"] is True


def test_pynq_overlay_manifest_has_lifecycle_fields():
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "pynq" / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert "overlay_name" in manifest
    assert "overlay_version" in manifest
    assert "interfaces" in manifest
    assert "governance" in manifest
    assert manifest["governance"]["requires_overlay_validation"] is True
    assert manifest["governance"]["requires_runtime_compatibility_check"] is True
