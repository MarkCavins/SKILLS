---
name: business-initiative-document
description: Create a comprehensive executive Business Initiative proposal as a Word document. Use when someone asks to create, draft, build, or fill out a business initiative, Amazon Working Backwards proposal, executive initiative brief, commercialization case, product investment proposal, or a document similar to Opsmith.ai Business Initiative. Always interview the user before generating the document.
license: MIT
allowed-tools: shell
---

# Business Initiative Document

Create an executive-ready `.docx` business initiative by interviewing the requester and then running the bundled generator.

## Mandatory interaction behavior

1. Do **not** draft the document immediately.
2. Tell the requester that you will collect the inputs in short sections.
3. Ask the questions in `references/questionnaire.md` **one section at a time**. Never dump the full questionnaire at once.
4. After each section, summarize the answers in 2 to 5 bullets and ask only for missing information that blocks a coherent proposal.
5. Accept `unknown`, `TBD`, or `skip`. Record those items as assumptions or validation needs rather than inventing facts.
6. Explicitly distinguish current availability, committed work, planning assumptions, and future roadmap.
7. Before generation, show a concise review containing: initiative, customer problem, outcome, growth mechanism, scope, timeline, commercial model, major risks, and recommendation.
8. Ask: `What output filename should I use?` If no filename is supplied, use a lowercase hyphenated initiative name ending in `-business-initiative.docx`.
9. Save the collected responses as UTF-8 JSON using the keys in `references/input-schema.json`.
10. Run:

```bash
python scripts/create_business_initiative.py --input <answers.json> --output <filename.docx>
```

11. Confirm that the file exists and report its path. Do not claim that unsupported capabilities are available.

## Direct terminal interview mode

If the requester asks to be prompted directly in the terminal, or supplies no structured answers, run:

```bash
python scripts/create_business_initiative.py --interactive --output <filename.docx>
```

The script asks the required questions, saves a sidecar JSON response file, and generates the Word document.

## Content and quality rules

- Use the reference document's decision-oriented structure, not its company-specific claims.
- Keep the executive snapshot concise and outcome led.
- Put detailed assumptions, scenarios, and validation requirements later in the document.
- Label illustrative financial values as scenarios, not forecasts.
- Never fabricate customer evidence, dates, installed-base counts, prices, conversion rates, ARR, or product availability.
- Preserve deployment choice, governance boundaries, and roadmap truth when relevant.
- End with a clear recommendation and a list of what to validate next.
- Use professional headings, tables, restrained blue accents, and a confidential footer.

## Validation

After generation, run:

```bash
python scripts/validate_output.py <filename.docx>
```

A passing result requires the expected section headings, a non-empty executive snapshot, an explicit recommendation, and no unreplaced placeholders.
