# Design Template Generator Skill for GitHub Copilot CLI

This scaffold creates a **GitHub Copilot CLI skill** that generates consistent design templates for **Word**, **PDF**, and **PowerPoint** assets using the visual language extracted from the attached Chef pitch decks.

## What this skill does

- Applies a shared color theme across document types.
- Standardizes typography and spacing.
- Enforces chart styling rules.
- Uses safe layout constraints so text boxes and chart areas do not overlap.
- Generates starter assets:
  - `output/Chef_Design_Template.docx`
  - `output/Chef_Design_Template.pptx`
  - `output/Chef_Design_Style_Guide.pdf`

## Files

- `.github/skills/design-template-generator/SKILL.md` – the Copilot CLI skill definition.
- `.github/agents/design-template-agent.md` – optional agent metadata that tells Copilot when to use the skill.
- `config/brand_tokens.json` – design tokens and chart rules.
- `scripts/generate_design_assets.py` – Python generator for the templates and style guide.

## Suggested usage in Copilot CLI

From the repo root, prompt Copilot with something like:

- `Create a Word template, PowerPoint template, and style guide PDF using the design-template-generator skill.`
- `Generate branded templates for a proposal deck, customer memo, and printable PDF summary.`
- `Use the design-template-generator skill and keep chart styling consistent with the Chef decks.`

## Notes

- The skill stores design rules in `config/brand_tokens.json` so you can revise colors, spacing, or typography without rewriting the skill.
- The included generator script creates baseline files. You can iterate further with Copilot CLI once the scaffold is in your repo.
