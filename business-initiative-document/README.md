# Business Initiative Document skill

Install the `business-initiative-document` folder under one of these locations:

- Project: `.github/skills/business-initiative-document/`
- Personal: `~/.copilot/skills/business-initiative-document/`

Then start Copilot CLI from the relevant project directory and ask:

`Create a business initiative proposal for my new product idea.`

The skill is designed to collect answers section by section before generating the DOCX. For a deterministic terminal questionnaire, ask Copilot to run the skill in interactive mode.

## Verification commands

```bash
python scripts/create_business_initiative.py --interactive --output initiative.docx
python scripts/validate_output.py initiative.docx
```

The generator requires Python 3 and `python-docx`.
