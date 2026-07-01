from collections import defaultdict
import statistics

def detect_anomalies(records):
    # group counts into time series keyed by (settlement, symptom)
    series = defaultdict(list)
    for r in records:
        series[(r["settlement"], r["symptom"])].append((r["date"], r["count"]))

    alerts = []
    for (settlement, symptom), points in series.items():
        points.sort(key=lambda p: p[0])
        counts = [c for _, c in points]
        if len(counts) < 5:
            continue

        baseline = counts[:-1]      # history, excluding today
        latest = counts[-1]         # today
        latest_date = points[-1][0]

        mean = statistics.mean(baseline)
        stdev = statistics.pstdev(baseline) or 1  # guard divide-by-zero

        z = (latest - mean) / stdev

        # flag a meaningful spike (high z AND a real case volume)
        if z >= 2.5 and latest >= 15:
            alerts.append({
                "settlement": settlement,
                "symptom": symptom,
                "latest_count": latest,
                "baseline_avg": round(mean, 1),
                "z_score": round(z, 1),
                "date": latest_date,
                "severity": "HIGH" if z >= 4 else "MODERATE",
            })

    alerts.sort(key=lambda a: a["z_score"], reverse=True)
    return alerts

def build_trend(records, settlement, symptom):
    """14-day series for one settlement+symptom — feeds the dashboard chart."""
    pts = [r for r in records if r["settlement"] == settlement and r["symptom"] == symptom]
    pts.sort(key=lambda r: r["date"])
    return [{"date": r["date"], "count": r["count"]} for r in pts]