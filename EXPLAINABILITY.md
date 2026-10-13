# Explainability

## Inputs
The agent accepts a list of user-reported print symptoms, optional printer/material context, and optional slicer settings such as nozzle temperature, bed temperature, print speed, and retraction distance.

## Decision
It matches reported symptoms to a curated set of plausible causes, then checks supplied settings for missing values or broad review flags. Each cause is accompanied by a reason and a low-risk next check.

## Limits
This is rule-based triage, not a physical inspection or guaranteed root-cause diagnosis. Printer design, filament formulation, humidity, nozzle condition, firmware, and slicer behavior can change the appropriate response.

## Tool: classify-print-symptoms

### Inputs and Data Sources
A list of symptom strings supplied by the user.

### Decision and Reasoning
Normalizes symptom names and matches known symptoms to candidate causes and checks.

### Outputs and Evidence
Returns matched symptoms, candidate causes, and the symptom-to-cause rationale.

### Limits and Constraints
Unrecognized symptom descriptions may not match known rules.

### Failure Handling
Invalid or absent symptom lists return validation errors instead of an invented diagnosis.

### Human Review
Ask the user to clarify unfamiliar symptoms and verify findings on the printer and slicer.

## Tool: review-print-settings

### Inputs and Data Sources
A settings object supplied by the user, plus optional material name.

### Decision and Reasoning
Checks value types and broad, explicitly documented review thresholds. These are prompts for investigation, not universal target values.

### Outputs and Evidence
Returns review flags tied to exact setting names and values.

### Limits and Constraints
The agent does not know every printer, filament, nozzle, or slicer profile.

### Failure Handling
Malformed settings are flagged and are not silently corrected.

### Human Review
Compare settings with the filament manufacturer's guidance and printer/slicer documentation.

## Tool: build-diagnosis-report

### Inputs and Data Sources
Symptoms, optional settings, and optional printer/material details.

### Decision and Reasoning
Combines symptom matches, settings flags, missing-context notes, and safe next checks.

### Outputs and Evidence
Produces a JSON-compatible report with a preliminary status, findings, and recommended checks.

### Limits and Constraints
The report cannot prove a root cause or guarantee a successful print.

### Failure Handling
Invalid input yields a structured error report.

### Human Review
A user should verify one change at a time and follow manufacturer safety instructions.
