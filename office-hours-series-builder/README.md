# Office Hours Series Builder

A Copilot CLI agent skill that analyzes Word/PDF source material and interactively creates one customer-facing weekly office-hours deck at a time.

## Install

Copy the `office-hours-series-builder` folder into one of these locations:

- Project: `.github/skills/office-hours-series-builder/`
- Personal: `~/.copilot/skills/office-hours-series-builder/`

Then start Copilot CLI or run `/skills reload` in an active session. Invoke it with a request such as:

`Use office-hours-series-builder on ./source.pdf to build a weekly customer office-hours series.`

## Optional fallback dependency

The included fallback generator uses `python-pptx`:

`python -m pip install python-pptx`

The primary workflow should use the richest installed slide-generation capability and render/inspect the output before delivery.
