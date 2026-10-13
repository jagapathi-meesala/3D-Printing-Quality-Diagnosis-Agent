from pathlib import Path
import yaml, json, re
ROOT = Path(__file__).resolve().parents[1]
required = ["agent.yaml","SOUL.md","README.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md","requirements.txt",".env.example",".gitignore","pytest.ini",
"core/__init__.py","core/diagnosis.py","core/cli.py",
"tools/classify-print-symptoms.yaml","tools/review-print-settings.yaml","tools/build-diagnosis-report.yaml",
"skills/print-symptom-triage/SKILL.md","skills/slicer-setting-review/SKILL.md","skills/diagnosis-reporting/SKILL.md",
"tests/test_agent.py","examples/print_case.json"]
missing = [x for x in required if not (ROOT/x).is_file()]
if missing:
    print("FAIL: missing files:", missing); raise SystemExit(1)
manifest = yaml.safe_load((ROOT/"agent.yaml").read_text())
assert manifest["spec_version"] == "0.1.0"
assert re.fullmatch(r"[a-z][a-z0-9-]*", manifest["name"])
assert len(manifest["tools"]) == 3 and len(manifest["skills"]) == 3
assert all(re.fullmatch(r"[a-z][a-z0-9-]*", name) for name in manifest["tools"])
for p in (ROOT/"tools").glob("*.yaml"):
    data = yaml.safe_load(p.read_text())
    assert set(data) == {"name","description","input_schema"}, p
    assert re.fullmatch(r"[a-z][a-z0-9-]*", data["name"])
    assert data["input_schema"]["type"] == "object"
for p in (ROOT/"skills").glob("*/SKILL.md"):
    assert p.read_text().startswith("---\nname: ")
doc = (ROOT/"EXPLAINABILITY.md").read_text()
for heading in ["## Inputs","## Decision","## Limits","## Tool: classify-print-symptoms","## Tool: review-print-settings","## Tool: build-diagnosis-report"]:
    assert heading in doc, heading
json.loads((ROOT/"examples/print_case.json").read_text())
print(f"PASS: all {len(required)}/{len(required)} required files present")
print("PASS: manifest IDs, tool schemas, skill frontmatter, explainability headings, and example JSON")
