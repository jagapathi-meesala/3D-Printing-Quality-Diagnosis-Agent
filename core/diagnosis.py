from typing import Any

SYMPTOM_RULES = {
    "stringing": {
        "causes": ["retraction settings may need review", "filament may contain excess moisture", "nozzle temperature may be high for the material"],
        "checks": ["Inspect travel/retraction settings in the slicer profile.", "Store and dry filament only according to its manufacturer's guidance.", "Compare nozzle temperature with the filament manufacturer's recommended range."]
    },
    "under-extrusion": {
        "causes": ["partial nozzle obstruction", "feed-path resistance or extruder slip", "flow or temperature settings may be unsuitable"],
        "checks": ["Inspect the filament path and extruder drive for visible slipping.", "Follow the printer manufacturer's procedure for checking a nozzle obstruction.", "Verify filament diameter and flow settings in the slicer."]
    },
    "layer-shifting": {
        "causes": ["motion system may be obstructed or loose", "acceleration or speed may be too aggressive for the machine", "belt tension may require inspection"],
        "checks": ["With the printer powered off and cool, inspect accessible belts and motion paths per the manual.", "Review speed and acceleration against the printer profile.", "Check for obstructions before another test print."]
    },
    "warping": {
        "causes": ["first-layer adhesion may be inadequate", "temperature or cooling behavior may not suit the material", "part geometry may increase corner lift"],
        "checks": ["Clean the build surface using the manufacturer's recommended method.", "Recheck first-layer setup and material-specific bed guidance.", "Consider orientation or brim settings in the slicer."]
    },
    "poor-bed-adhesion": {
        "causes": ["build surface may be contaminated", "first-layer height or leveling may be incorrect", "bed temperature may not suit the material"],
        "checks": ["Clean the build surface according to its instructions.", "Review first-layer height and bed leveling using the printer's procedure.", "Compare bed temperature with the material manufacturer's guidance."]
    },
    "blobs-or-zits": {
        "causes": ["seam placement or pressure behavior may affect the surface", "temperature or retraction settings may need review", "filament moisture may contribute"],
        "checks": ["Inspect seam placement and preview in the slicer.", "Change one temperature or retraction parameter at a time within manufacturer guidance.", "Check filament storage recommendations."]
    },
    "layer-gaps": {
        "causes": ["flow or extrusion may be inconsistent", "layer height and line width may be incompatible", "partial obstruction or filament feed issues may exist"],
        "checks": ["Inspect extrusion consistency and the filament feed path.", "Check slicer line width and layer height against the nozzle/profile guidance.", "Follow manufacturer instructions before cleaning or servicing the hot end."]
    }
}

ALIASES = {
    "under extrusion": "under-extrusion",
    "underextrusion": "under-extrusion",
    "layer shifting": "layer-shifting",
    "bed adhesion": "poor-bed-adhesion",
    "poor bed adhesion": "poor-bed-adhesion",
    "blobs": "blobs-or-zits",
    "zits": "blobs-or-zits",
    "layer gaps": "layer-gaps",
    "gaps between layers": "layer-gaps",
}

def classify_print_symptoms(symptoms: Any) -> dict[str, Any]:
    if not isinstance(symptoms, list) or not symptoms:
        return {"valid": False, "errors": ["symptoms must be a non-empty list of strings."], "matches": [], "unrecognized": []}
    matches, unrecognized = [], []
    for raw in symptoms:
        if not isinstance(raw, str) or not raw.strip():
            unrecognized.append(str(raw))
            continue
        key = raw.strip().lower()
        key = ALIASES.get(key, key.replace(" ", "-"))
        if key in SYMPTOM_RULES:
            matches.append({"symptom": key, **SYMPTOM_RULES[key]})
        else:
            unrecognized.append(raw)
    return {"valid": True, "errors": [], "matches": matches, "unrecognized": unrecognized}

def review_print_settings(settings: Any, material: str | None = None) -> dict[str, Any]:
    if not isinstance(settings, dict):
        return {"valid": False, "errors": ["settings must be an object."], "flags": []}
    errors, flags = [], []
    numeric_ranges = {
        "nozzle_temp_c": (0, 350),
        "bed_temp_c": (0, 150),
        "print_speed_mm_s": (1, 500),
        "retraction_distance_mm": (0, 20),
        "layer_height_mm": (0.01, 2.0),
        "nozzle_diameter_mm": (0.1, 5.0),
    }
    for key, (low, high) in numeric_ranges.items():
        if key not in settings:
            continue
        value = settings[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{key}: expected a numeric value.")
        elif not low <= value <= high:
            flags.append({"setting": key, "value": value, "reason": f"Outside broad review bounds ({low}–{high}); verify units and printer/material documentation."})
    if "layer_height_mm" in settings and "nozzle_diameter_mm" in settings:
        h, d = settings["layer_height_mm"], settings["nozzle_diameter_mm"]
        if isinstance(h, (int, float)) and not isinstance(h, bool) and isinstance(d, (int, float)) and not isinstance(d, bool) and h > d:
            flags.append({"setting": "layer_height_mm", "value": h, "reason": "Layer height exceeds supplied nozzle diameter; verify the slicer profile and printer capability."})
    if material and isinstance(material, str) and material.strip().lower() in {"pla", "petg", "abs", "asa", "tpu", "nylon"}:
        material_note = f"Use manufacturer-specific guidance for {material.strip()} rather than treating generic settings as universal."
    else:
        material_note = "Material is missing or unrecognized; temperature and cooling advice remains material-dependent."
    return {"valid": not errors, "errors": errors, "flags": flags, "material_note": material_note}

def build_diagnosis_report(case: Any) -> dict[str, Any]:
    if not isinstance(case, dict):
        return {"valid": False, "status": "invalid_input", "errors": ["case must be an object."]}
    symptoms_result = classify_print_symptoms(case.get("symptoms"))
    settings_result = review_print_settings(case.get("settings", {}), case.get("material"))
    errors = symptoms_result.get("errors", []) + settings_result.get("errors", [])
    findings = []
    for match in symptoms_result.get("matches", []):
        findings.append({"type": "symptom_match", "symptom": match["symptom"], "candidate_causes": match["causes"], "checks": match["checks"]})
    for flag in settings_result.get("flags", []):
        findings.append({"type": "setting_review", **flag})
    if symptoms_result.get("unrecognized"):
        findings.append({"type": "unrecognized_symptoms", "items": symptoms_result["unrecognized"], "detail": "Please clarify these symptoms for a more useful review."})
    missing = []
    for field in ("printer_model", "material", "nozzle_diameter_mm"):
        if not case.get(field) and not (field == "nozzle_diameter_mm" and case.get("settings", {}).get(field) if isinstance(case.get("settings", {}), dict) else False):
            missing.append(field)
    return {
        "agent": "3d-printing-quality-diagnosis-agent",
        "valid": not errors,
        "status": "invalid_input" if errors else ("preliminary_review" if missing or findings else "no_flags"),
        "context": {"printer_model": case.get("printer_model"), "material": case.get("material")},
        "errors": errors,
        "findings": findings,
        "settings_review": settings_result,
        "missing_context": missing,
        "limitations": [
            "Diagnosis is rule-based and based only on supplied text/settings.",
            "No photo, G-code, firmware telemetry, or physical printer inspection was analyzed.",
            "Candidate causes are not confirmed root causes; printer and material documentation takes precedence."
        ],
        "recommended_approach": [
            "Inspect the printer safely and follow the manufacturer's instructions.",
            "Change one variable at a time and record the result.",
            "Avoid touching hot or moving components; power down before permitted mechanical inspection."
        ]
    }
