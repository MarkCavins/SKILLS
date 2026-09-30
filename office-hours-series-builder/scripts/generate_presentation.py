#!/usr/bin/env python3
import json, sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt


def add_notes_placeholder(slide, text):
    # python-pptx notes editing support differs by version. Preserve notes in
    # slide speaker-notes metadata when available; otherwise add to PPTX core
    # generation log and keep the JSON companion as the source of truth.
    try:
        tf = slide.notes_slide.notes_text_frame
        tf.text = text
        return True
    except Exception:
        return False


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: generate_presentation.py week-spec.json output.pptx')
    spec_path, out_path = map(Path, sys.argv[1:])
    data=json.loads(spec_path.read_text(encoding='utf-8'))
    prs=Presentation()
    prs.slide_width=Inches(13.333)
    prs.slide_height=Inches(7.5)
    notes_ok=True
    for i,item in enumerate(data['slides']):
        layout=prs.slide_layouts[0] if i==0 else prs.slide_layouts[1]
        slide=prs.slides.add_slide(layout)
        slide.shapes.title.text=item['title']
        if i==0:
            slide.placeholders[1].text='
'.join(item.get('bullets',[]))
        else:
            body=slide.placeholders[1].text_frame
            body.clear()
            for j,b in enumerate(item.get('bullets',[])):
                p=body.paragraphs[0] if j==0 else body.add_paragraph()
                p.text=b
                p.font.size=Pt(24)
        notes=item.get('notes','')
        if item.get('estimated_minutes') is not None:
            notes += f"

Estimated time: {item['estimated_minutes']} minutes."
        notes_ok = add_notes_placeholder(slide, notes) and notes_ok
    prs.save(out_path)
    if not notes_ok:
        print('Warning: speaker notes remain in the JSON companion because this python-pptx version cannot write notes.')
    print(out_path)

if __name__=='__main__': main()
