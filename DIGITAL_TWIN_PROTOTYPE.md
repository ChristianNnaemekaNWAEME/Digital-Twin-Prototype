# Exhibit J-10: Integrated Digital-Twin Prototype

## What this is

This connects three previously separate, independently-verified
components of this endeavor into a single pipeline:

1. **Digitization** (the exact method from Exhibit J-7): legacy
   pattern measurements written to a real DXF file, read back, and
   verified lossless.
2. **Optimization** (the exact method from Exhibit J-1): the
   recovered pattern geometry is converted into piece objects and
   packed using the MaxRects nesting algorithm.
3. **Equipment-health monitoring (SIMULATED)**: a per-sheet
   simulated health score, demonstrating where real predictive-
   maintenance telemetry (Exhibits J-4, J-5, J-6) would attach to
   this same pipeline.

## Why this exists

Exhibits J-1 through J-9 each demonstrate one component of this
endeavor in isolation. This prototype demonstrates that these
components can operate as a single, connected pipeline, directly
supporting the "digital twin" concept referenced elsewhere in this
petition (Exhibit K-29; several L-series job postings), which none of
the prior exhibits individually demonstrated.

## What this honestly is, and is not

This is a small-scale architectural demonstration of integration, not
a claim of a deployed industrial digital-twin system. The equipment-
health scores in Stage 3 are explicitly labeled as simulated, not real
sensor telemetry, generated to demonstrate data flow and architecture
only.

## Results (reported exactly as obtained)

- 8 patterns digitized and recovered losslessly (Stage 1)
- Packed onto 2 sheets at 53.4% material utilization (Stage 2)
- 1 of 2 sheets flagged for simulated maintenance attention (Stage 3)

Confirmed reproducible on repeated runs with a fixed random seed.

## Running it yourself

```
pip install ezdxf
python digital_twin_pipeline.py
```

Requires the `cutting-stock-optimizer` package (Exhibit J-1) to be
present in the same parent directory, and `ezdxf` (used in Exhibit J-7).
