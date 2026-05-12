from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    manifest = yaml.safe_load((root / "config/aggregation_manifest.yml").read_text())["aggregation_manifest"]
    aggregations = pd.read_csv(root / "data/aggregation_records.csv")

    aggregations["source_coverage_complete"] = aggregations["source_node_count"] >= aggregations["required_node_count"]
    aggregations["confidence_sufficient"] = aggregations["confidence"] >= 0.75
    aggregations["aggregation_usable"] = (
        aggregations["source_coverage_complete"]
        & aggregations["confidence_sufficient"]
        & aggregations["lineage_complete"]
        & (aggregations["quality_state"] == "valid")
    )
    aggregations["requires_qualification"] = ~aggregations["aggregation_usable"]

    aggregations.to_csv(out / "python_aggregation_lineage_confidence_evaluation.csv", index=False)

    summary = pd.DataFrame([{
        "aggregations": len(aggregations),
        "aggregation_usable_rate": aggregations["aggregation_usable"].mean(),
        "requires_qualification_rate": aggregations["requires_qualification"].mean(),
        "lineage_complete_rate": aggregations["lineage_complete"].mean(),
        "mean_confidence": aggregations["confidence"].mean()
    }]).round(4)
    summary.to_csv(out / "python_aggregation_lineage_confidence_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
