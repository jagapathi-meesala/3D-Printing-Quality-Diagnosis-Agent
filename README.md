# 3D Printing Quality Diagnosis Agent

A portable, deterministic troubleshooting agent for common fused-filament fabrication (FFF/FDM) print-quality issues. It maps user-reported symptoms and supplied print settings to plausible causes, checks the data for gaps, and returns a structured report with confidence labels and safe next steps.

## Included capabilities
- Triage common symptoms: stringing, under-extrusion, layer shifting, warping, poor bed adhesion, blobs, and visible layer gaps.
- Review optional material, nozzle, bed, speed, retraction, and temperature settings against broad, non-prescriptive sanity checks.
- Explain evidence and uncertainty instead of presenting a single cause as fact.
- Generate JSON reports suitable for later UI or workflow integration.

## Scope
This version uses rule-based reasoning over the supplied form data. It does not inspect photos, read printer firmware, control hardware, or replace material/printer-specific manufacturer guidance. Suggested ranges are general prompts for investigation, not universal settings.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 verification/readiness_audit.py
python3 -m core.cli examples/print_case.json
```

## Input
See `examples/print_case.json`. The `symptoms` field is a list of observed issues and `settings` is an object of optional slicer/printer values.

## OpenGAP
The manifest targets OpenGAP v0.1.0. If the official CLI is installed, run `opengap validate`.
