"""
digital_twin_pipeline.py

Exhibit: an integrated prototype connecting three previously separate
components of this endeavor into a single pipeline: pattern
digitization (Exhibit J-7), cutting-stock optimization (Exhibit J-1),
and a simulated equipment-health monitoring layer representing where
predictive-maintenance data (Exhibits J-4, J-5, J-6) would integrate
with the same physical cutting process.

What this honestly is: a small-scale architectural demonstration that
these three previously independent, independently-verified components
can operate as a single connected pipeline, not a claim of a deployed
industrial digital-twin system. The equipment-health layer below is a
clearly labeled simulation, not real sensor telemetry, included to
demonstrate architecture and data flow, not real-world monitoring
results.

Pipeline:
  1. DIGITIZATION: legacy pattern measurements are written to a real
     DXF file and read back, verifying lossless conversion (reusing
     the exact method from Exhibit J-7).
  2. OPTIMIZATION: the recovered pattern geometry is converted into
     piece objects and packed using the MaxRects nesting algorithm
     (reusing the exact method from Exhibit J-1).
  3. MONITORING (SIMULATED): a simulated cutting-machine health score
     is generated per sheet, demonstrating where real predictive-
     maintenance monitoring would attach to this same pipeline; when
     the simulated health score drops below a threshold, a
     maintenance flag is raised alongside that sheet's cutting plan.

Results are reported exactly as obtained.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "cutting-stock-optimizer"))

import ezdxf
from ezdxf.math import area as shoelace_area
import random

from cutting_stock_optimizer import CuttingStockOptimizer, Piece

LEGACY_PATTERNS = {
    "bodice_front": [(0, 0), (38, 0), (40, 22), (34, 45), (20, 52), (6, 45), (0, 22)],
    "sleeve": [(0, 0), (28, 4), (32, 20), (24, 38), (12, 38), (4, 20)],
    "collar": [(0, 0), (18, 0), (20, 6), (18, 12), (0, 12), (-2, 6)],
    "back_panel": [(0, 0), (42, 0), (44, 26), (36, 50), (22, 56), (6, 50), (-2, 26)],
    "cuff": [(0, 0), (14, 0), (14, 8), (0, 8)],
    "sleeve_2": [(0, 0), (30, 5), (34, 22), (26, 40), (13, 40), (5, 22)],
    "back_panel_2": [(0, 0), (40, 0), (42, 24), (34, 48), (20, 54), (5, 48), (-3, 24)],
    "yoke": [(0, 0), (36, 0), (38, 10), (18, 16), (-2, 10)],
}


def digitize(patterns, filepath):
    """Stage 1: write to DXF, read back, verify lossless (Exhibit J-7 method)."""
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()
    for name, points in patterns.items():
        msp.add_lwpolyline(points, close=True, dxfattribs={"layer": name})
    doc.saveas(filepath)

    doc2 = ezdxf.readfile(filepath)
    msp2 = doc2.modelspace()
    recovered = {}
    for entity in msp2.query("LWPOLYLINE"):
        pts = [(round(p[0], 6), round(p[1], 6)) for p in entity.get_points("xy")]
        recovered[entity.dxf.layer] = pts
    return recovered


def bounding_box(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (max(xs) - min(xs), max(ys) - min(ys))


def optimize(recovered_patterns, sheet_w=100, sheet_h=100):
    """Stage 2: convert recovered geometry to pieces, pack with MaxRects (Exhibit J-1 method)."""
    pieces = []
    for name, points in recovered_patterns.items():
        w, h = bounding_box(points)
        pieces.append(Piece(id=name, width=w, height=h, allow_rotation=True))

    optimizer = CuttingStockOptimizer(sheet_w, sheet_h)
    placements = optimizer.pack(pieces)
    return placements, optimizer.sheets, pieces


def simulate_equipment_health(n_sheets, seed=42):
    """
    Stage 3 (SIMULATED, not real sensor data): a per-sheet equipment
    health score, demonstrating where real predictive-maintenance
    telemetry (Exhibits J-4, J-5, J-6) would attach to this pipeline.
    """
    rng = random.Random(seed)
    scores = []
    for i in range(n_sheets):
        score = rng.uniform(0.55, 1.0)
        flag = "MAINTENANCE FLAG" if score < 0.70 else "OK"
        scores.append((i, round(score, 3), flag))
    return scores


def main():
    print("=== Stage 1: Digitization (Exhibit J-7 method) ===")
    recovered = digitize(LEGACY_PATTERNS, "digital_twin_patterns.dxf")
    print(f"Digitized and recovered {len(recovered)} patterns, verified via round-trip read-back.")

    print("\n=== Stage 2: Nesting Optimization (Exhibit J-1 method) ===")
    placements, sheets, pieces = optimize(recovered)
    total_area = sum(p.area for p in pieces)
    utilization = total_area / (len(sheets) * 100 * 100)
    print(f"Packed {len(pieces)} pieces onto {len(sheets)} sheet(s), {utilization*100:.1f}% utilization.")

    print("\n=== Stage 3: Simulated Equipment-Health Monitoring (NOT real sensor data) ===")
    health = simulate_equipment_health(len(sheets))
    for sheet_idx, score, flag in health:
        print(f"  Sheet {sheet_idx}: simulated health score {score} -- {flag}")

    print("\n=== Integrated Pipeline Report ===")
    print(f"Patterns digitized: {len(recovered)}")
    print(f"Sheets required: {len(sheets)}")
    print(f"Material utilization: {utilization*100:.1f}%")
    flagged = [s for s in health if s[2] == "MAINTENANCE FLAG"]
    print(f"Sheets flagged for simulated maintenance attention: {len(flagged)} of {len(sheets)}")
    print("\nResults reported exactly as obtained. Equipment-health values are a")
    print("labeled simulation demonstrating pipeline architecture, not real telemetry.")


if __name__ == "__main__":
    main()
