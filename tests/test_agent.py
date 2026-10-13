import json
from pathlib import Path
from core.diagnosis import classify_print_symptoms, review_print_settings, build_diagnosis_report

def sample():
    return json.loads(Path("examples/print_case.json").read_text())

def test_known_symptoms_match():
    result = classify_print_symptoms(["stringing", "poor bed adhesion"])
    assert result["valid"]
    assert len(result["matches"]) == 2

def test_alias_under_extrusion():
    assert classify_print_symptoms(["under extrusion"])["matches"][0]["symptom"] == "under-extrusion"

def test_empty_symptoms_invalid():
    assert not classify_print_symptoms([])["valid"]

def test_unknown_symptom_reported():
    result = classify_print_symptoms(["mystery artifact"])
    assert result["unrecognized"] == ["mystery artifact"]

def test_setting_outside_bounds_flagged():
    result = review_print_settings({"nozzle_temp_c": 999})
    assert result["flags"][0]["setting"] == "nozzle_temp_c"

def test_setting_wrong_type_error():
    assert not review_print_settings({"bed_temp_c": "hot"})["valid"]

def test_report_includes_safety_limits():
    report = build_diagnosis_report(sample())
    assert report["valid"]
    assert report["limitations"]
    assert report["recommended_approach"]

def test_layer_height_vs_nozzle_flag():
    result = review_print_settings({"layer_height_mm": 0.6, "nozzle_diameter_mm": 0.4})
    assert any("nozzle diameter" in f["reason"] for f in result["flags"])
