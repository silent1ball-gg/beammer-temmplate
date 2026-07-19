# Next Change

## Decision To Enable

Determine whether the weekly-report workflow is ready for routine use or needs a minimal layout or build adjustment.

## Smallest Evidence-Producing Change

Build the supplied `weekly-report/report.yaml`, render the resulting PDF pages to images, and inspect the full deck.

## Validation Rule

The report must pass YAML validation and tests, compile successfully, and render with no clipped text, missing images, malformed glyphs, or table/column overlap.

## Result

Passed after one renderer adjustment. The next evidence-producing change should use an actual dense weekly report, especially long overview and plan entries, to test the documented field limits in practice.
