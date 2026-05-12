from pathlib import Path
import json

required = {
    "monitoring_stream_in",
    "monitoring_stream_out",
    "timestamp_counter",
    "event_trigger",
    "queue_pressure_signal",
    "quality_state_frame"
}

def main():
    manifest = json.loads((Path(__file__).resolve().parent / "overlay_manifest.json").read_text())
    names = {i["name"] for i in manifest.get("interfaces", [])}
    issues = [f"Missing interface: {name}" for name in required if name not in names]
    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("PYNQ distributed monitoring overlay validation passed:", not issues)
    for issue in issues:
        print("-", issue)

if __name__ == "__main__":
    main()
