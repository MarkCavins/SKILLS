---
name: office-hours-series-builder
description: Analyze a Word document or PDF and interactively create a customer-facing weekly office-hours presentation series, generating one PowerPoint deck at a time. Use when a user asks to turn source documents into recurring office hours, weekly enablement sessions, customer education decks, or a multi-week presentation series.
---

# Office Hours Series Builder

Create a weekly, customer-facing office-hours series from one or more `.docx` or `.pdf` source files. Work interactively and generate exactly one week's `.pptx` at a time.

## Non-negotiable behavior

1. Never invent source facts, customer claims, product capabilities, quotations, dates, metrics, or commitments.
2. Clearly label facilitator recommendations and suggested examples as suggestions.
3. Preserve confidentiality. Do not place internal-only, personal, restricted, or customer-confidential details into a customer-facing deck unless the user explicitly confirms they are approved.
4. Ask one compact batch of questions at a time. Do not overwhelm the user.
5. Generate one week only, validate it, report the output path, and then ask whether to continue.
6. The user may type `stop`, `end`, `quit`, `cancel`, or `no more` at any prompt. End immediately, summarize completed weeks, and do not generate another deck.
7. Never continue beyond the configured number of weeks or topics.

## Phase 1: Intake and source analysis

1. Ask for the path(s) to the Word document or PDF unless already supplied.
2. Verify each file exists and is `.docx` or `.pdf`. If not, explain the issue and ask for a replacement.
3. Read the full source. For PDF, use a text extraction or PDF-reading capability. For Word, extract paragraphs, headings, tables, notes, and captions.
4. Build an internal source brief containing:
   - purpose and intended audience
   - major themes and concepts
   - product names and approved terminology
   - procedures, examples, metrics, dates, and claims
   - prerequisites and dependencies
   - potential customer questions
   - sensitive or internal-only content to exclude
   - source gaps or contradictions
5. Show the user a concise analysis summary and ask for corrections before planning the series.

## Phase 2: Series setup

Ask:

1. “How many weeks should the weekly office-hours series run?” Require an integer from 1 to 52.
2. Ask for the intended customer audience and baseline knowledge.
3. Ask for the standard session duration. Default to 45 minutes only if the user accepts that default.
4. Ask for presentation branding or a `.pptx` template. If none is provided, use a clean, accessible 16:9 business design.
5. Ask whether speaker notes, demo steps, Q&A prompts, and take-home actions are required. Recommend all four.
6. Ask for the topic of each week. Accept either:
   - all topics at once, or
   - the next topic when each week begins.

Maintain this state:

```text
series_total_weeks
series_duration_minutes
audience
brand_or_template
source_files
source_brief
week_topics
completed_weeks
next_week_number
```

## Phase 3: Weekly interview

For the current week, confirm or ask for the presentation title, then ask only what is still unknown:

1. What should customers understand or be able to do by the end?
2. What are the 2 to 4 key takeaways?
3. Should the session include a demo, walkthrough, discussion, exercise, or Q&A?
4. Which source sections must be covered or avoided?
5. What customer pain points, scenarios, or objections should be addressed?
6. What call to action or follow-up should close the session?
7. Are there approved examples, screenshots, metrics, links, or customer stories?

If the answers are incomplete, propose a bounded draft and explicitly ask the user to approve or correct it before generating the deck.

## Phase 4: Build one week's deliverables

Create a presentation plan using `templates/week-plan.md`. Typical flow:

1. Title and session promise
2. Why this matters
3. Learning objectives
4. Core concept or framework
5. Two to four instructional content slides
6. Demo or guided exercise, when applicable
7. Practical customer scenario
8. Key takeaways
9. Q&A prompts
10. Next steps and preview of the next week

Adapt slide count to session duration. Keep slides scan-friendly, customer-facing, and visually led. Avoid dense paragraphs. Put delivery detail in speaker notes.

For every slide include:

- slide title
- concise on-slide content
- recommended visual
- speaker notes written as a customer-facing facilitator script
- source attribution in notes for factual claims
- estimated delivery time

Generate a `.pptx` named:

```text
Week-<NN>-<short-kebab-title>.pptx
```

Use an available PowerPoint/slides generation skill when present. Otherwise, use a reliable presentation library such as `python-pptx`. If a brand template is supplied, preserve its layouts, fonts, colors, logo rules, and footer conventions.

Also save the structured week specification as:

```text
Week-<NN>-<short-kebab-title>.json
```

If using the included fallback script, populate the JSON using `templates/week-spec.example.json`, then run:

```bash
python scripts/generate_presentation.py path/to/week-spec.json output.pptx
```

## Phase 5: Quality checks

Before reporting completion, verify:

- the `.pptx` opens successfully
- every slide has a title
- speaker notes or a companion facilitator script are present
- claims are traceable to the source or labeled as suggestions
- no internal-only content appears in customer-facing text
- slides are readable and not text-heavy
- timing totals approximately match the session duration
- filename and week number are correct
- the deck covers the approved objective and takeaways

If rendering tools are available, render slides to images and inspect them for clipping, overlap, tiny text, broken characters, and poor contrast. Fix issues before delivery.

## Phase 6: Continue or stop loop

After completing Week N, say:

> Week N is complete: `<output path>`. Would you like to create Week N+1? You can answer with the next presentation title, say `continue`, or say `stop` to end the series.

Then apply this logic:

```text
if user requests stop:
    end and list completed weeks
elif completed_weeks >= series_total_weeks:
    end and confirm the series is complete
else:
    increment next_week_number
    ask for the next week's title if it is not already known
    run the weekly interview
    generate exactly one additional week
```

Never generate several weekly decks in one pass unless the user explicitly overrides the one-week-at-a-time requirement.

## Additional resources

- `references/interview-and-quality-guide.md`: questioning, customer-facing writing, timing, and validation guidance.
- `templates/week-plan.md`: weekly planning worksheet.
- `templates/week-spec.example.json`: schema example for the fallback generator.
- `scripts/generate_presentation.py`: simple deterministic `.pptx` fallback generator.
