import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pptx import Presentation
from pptx.util import Inches, Pt as PPTPt
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.dml.color import RGBColor as PPTRGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / 'config' / 'brand_tokens.json').read_text())
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)


def hex_rgb(value):
    value = value.replace('#', '')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def make_docx():
    doc = Document()
    styles = doc.styles

    def ensure_style(name, style_type, base=None):
        if name in styles:
            return styles[name]
        s = styles.add_style(name, style_type)
        if base:
            s.base_style = styles[base]
        return s

    body = styles['Normal']
    body.font.name = TOKENS['typography']['font_primary']
    body.font.size = Pt(TOKENS['typography']['word']['body_pt'])
    body.paragraph_format.space_after = Pt(TOKENS['spacing']['paragraph_space_after_pt'])
    body.paragraph_format.line_spacing = TOKENS['spacing']['line_spacing']

    title = styles['Title']
    title.font.name = TOKENS['typography']['font_primary']
    title.font.size = Pt(TOKENS['typography']['word']['title_pt'])
    title.font.color.rgb = RGBColor(*hex_rgb(TOKENS['colors']['background_primary']))

    h1 = styles['Heading 1']
    h1.font.name = TOKENS['typography']['font_primary']
    h1.font.size = Pt(TOKENS['typography']['word']['heading1_pt'])
    h1.font.color.rgb = RGBColor(*hex_rgb(TOKENS['colors']['background_primary']))

    h2 = styles['Heading 2']
    h2.font.name = TOKENS['typography']['font_primary']
    h2.font.size = Pt(TOKENS['typography']['word']['heading2_pt'])
    h2.font.color.rgb = RGBColor(*hex_rgb(TOKENS['colors']['text_secondary']))

    cap = ensure_style('CaptionMuted', WD_STYLE_TYPE.PARAGRAPH, 'Normal')
    cap.font.name = TOKENS['typography']['font_primary']
    cap.font.size = Pt(TOKENS['typography']['word']['caption_pt'])
    cap.font.color.rgb = RGBColor(*hex_rgb(TOKENS['colors']['text_muted']))

    sec = doc.sections[0]
    sec.top_margin = Inches(TOKENS['spacing']['min_margin_in'])
    sec.bottom_margin = Inches(TOKENS['spacing']['min_margin_in'])
    sec.left_margin = Inches(TOKENS['spacing']['min_margin_in'])
    sec.right_margin = Inches(TOKENS['spacing']['min_margin_in'])

    p = doc.add_paragraph('Chef Design Template', style='Title')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.add_paragraph('Reusable starter template for proposals, briefs, and summaries.', style='CaptionMuted')

    doc.add_paragraph('Heading Level 1', style='Heading 1')
    doc.add_paragraph(
        'This paragraph demonstrates the shared body style. It uses consistent spacing and line height to reduce crowding. '
        'Keep sections short and let whitespace do some of the design work.',
        style='Normal'
    )

    doc.add_paragraph('Heading Level 2', style='Heading 2')
    doc.add_paragraph(
        'Charts should use the configured palette, reserve room for labels, and avoid stacking multiple dense visuals in the same block. '
        'Use captions to explain the chart purpose rather than packing notes into the plot area.',
        style='Normal'
    )

    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    hdr[0].text = 'Token'
    hdr[1].text = 'Value'
    for k, v in TOKENS['colors'].items():
        row = table.add_row().cells
        row[0].text = k
        row[1].text = v

    doc.add_paragraph('Caption: Use muted caption text under tables and charts.', style='CaptionMuted')
    doc.save(OUT / 'Chef_Design_Template.docx')


def add_textbox(slide, left, top, width, height, text, font_size, color_hex, bold=False, align=PP_ALIGN.LEFT):
    tx = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = TOKENS['typography']['font_primary']
    run.font.size = PPTPt(font_size)
    run.font.bold = bold
    run.font.color.rgb = PPTRGBColor(*hex_rgb(color_hex))
    return tx


def make_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Blank slide
    blank = prs.slide_layouts[6]

    # Slide 1 - title
    slide = prs.slides.add_slide(blank)
    add_textbox(slide, 0.7, 0.45, 11.8, 0.6, 'Chef Design Template', TOKENS['typography']['ppt']['title_pt'], TOKENS['colors']['background_primary'], True)
    add_textbox(slide, 0.7, 1.15, 11.2, 0.4, 'Starter deck with spacing and chart rules derived from the Chef pitch decks', TOKENS['typography']['ppt']['subtitle_pt'], TOKENS['colors']['text_secondary'])
    # decorative band
    shape = slide.shapes.add_shape(1, Inches(0.7), Inches(1.75), Inches(2.0), Inches(0.12))
    shape.fill.solid()
    shape.fill.fore_color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['accent_gold']))
    shape.line.fill.background()

    # Slide 2 - content layout
    slide = prs.slides.add_slide(blank)
    add_textbox(slide, 0.7, 0.35, 8.0, 0.6, 'Content Layout', TOKENS['typography']['ppt']['section_pt'], TOKENS['colors']['background_primary'], True)
    add_textbox(slide, 0.7, 1.05, 5.8, 4.8,
                '• Keep content within a 0.5 in margin\n'
                '• Reserve footer band for notes/citations\n'
                '• Leave a 0.25 in gutter between text and visuals\n'
                '• Cap text box fill at ~85% of the reserved area\n'
                '• Prefer dark backgrounds with bright headings and muted captions',
                TOKENS['typography']['ppt']['body_pt'], TOKENS['colors']['text_secondary'])
    # visual placeholder
    vis = slide.shapes.add_shape(1, Inches(6.9), Inches(1.15), Inches(5.4), Inches(3.8))
    vis.fill.solid(); vis.fill.fore_color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['background_primary']))
    vis.line.color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['support_blue']))
    add_textbox(slide, 7.15, 2.65, 4.9, 0.5, 'Reserved visual area\n(no overlapping text)', TOKENS['typography']['ppt']['body_pt'], TOKENS['colors']['text_primary'], align=PP_ALIGN.CENTER)
    add_textbox(slide, 0.7, 6.65, 12.0, 0.25, 'Caption: Keep supporting notes outside the visual block.', TOKENS['typography']['ppt']['caption_pt'], TOKENS['colors']['text_muted'])

    # Slide 3 - chart sample
    slide = prs.slides.add_slide(blank)
    add_textbox(slide, 0.7, 0.35, 8.0, 0.6, 'Chart Style Sample', TOKENS['typography']['ppt']['section_pt'], TOKENS['colors']['background_primary'], True)
    chart_data = CategoryChartData()
    chart_data.categories = ['Ops', 'Audit', 'Provisioning', 'Patching']
    chart_data.add_series('Savings', (35, 28, 22, 15))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.9), Inches(1.2), Inches(6.6), Inches(4.4), chart_data).chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['text_muted']))
    chart.value_axis.format.line.color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['text_primary']))
    chart.category_axis.format.line.color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['text_primary']))
    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    # series color
    ser = chart.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['accent_gold']))
    ser.format.line.color.rgb = PPTRGBColor(*hex_rgb(TOKENS['colors']['accent_gold']))
    # Chart side notes
    add_textbox(slide, 8.0, 1.25, 4.3, 3.8,
                'Chart rules\n\n'
                '• Highlight one series in gold\n'
                '• Use white axis labels on dark backgrounds\n'
                '• Keep legend at the bottom\n'
                '• Leave breathing room between plot and commentary\n'
                '• Move narrative into caption text instead of the plot area',
                TOKENS['typography']['ppt']['body_pt'], TOKENS['colors']['text_secondary'])
    add_textbox(slide, 0.9, 6.65, 12.0, 0.25, 'Caption: Example chart style with dark theme and restrained palette.', TOKENS['typography']['ppt']['caption_pt'], TOKENS['colors']['text_muted'])

    prs.save(OUT / 'Chef_Design_Template.pptx')


def make_pdf():
    pdf_path = OUT / 'Chef_Design_Style_Guide.pdf'
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                            leftMargin=TOKENS['spacing']['min_margin_in'] * inch,
                            rightMargin=TOKENS['spacing']['min_margin_in'] * inch,
                            topMargin=TOKENS['spacing']['min_margin_in'] * inch,
                            bottomMargin=TOKENS['spacing']['min_margin_in'] * inch)
    styles = getSampleStyleSheet()
    body = ParagraphStyle('Body', parent=styles['BodyText'],
                          fontName='Helvetica', fontSize=TOKENS['typography']['pdf']['body_pt'],
                          leading=TOKENS['typography']['pdf']['body_pt'] * 1.3,
                          textColor=colors.HexColor(TOKENS['colors']['text_secondary']))
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
                        fontName='Helvetica-Bold', fontSize=TOKENS['typography']['pdf']['title_pt'],
                        textColor=colors.HexColor(TOKENS['colors']['background_primary']))
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
                        fontName='Helvetica-Bold', fontSize=TOKENS['typography']['pdf']['heading_pt'],
                        textColor=colors.HexColor(TOKENS['colors']['background_primary']))
    cap = ParagraphStyle('Cap', parent=styles['BodyText'],
                         fontName='Helvetica', fontSize=TOKENS['typography']['pdf']['caption_pt'],
                         textColor=colors.HexColor(TOKENS['colors']['text_muted']))

    story = [
        Paragraph('Chef Design Style Guide', h1),
        Spacer(1, 0.15 * inch),
        Paragraph('This PDF summarizes the reusable design tokens, chart rules, and spacing constraints used by the generator skill.', body),
        Spacer(1, 0.2 * inch),
        Paragraph('Color Tokens', h2),
    ]
    data = [['Token', 'Hex']] + [[k, v] for k, v in TOKENS['colors'].items()]
    tbl = Table(data, colWidths=[2.8 * inch, 1.4 * inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(TOKENS['colors']['background_primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(TOKENS['colors']['support_blue'])),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor('#EEF2F8')]),
    ]))
    story.extend([tbl, Spacer(1, 0.2 * inch), Paragraph('Chart Rules', h2)])
    for note in TOKENS['charts']['notes']:
        story.append(Paragraph(f'• {note}', body))
    story.extend([
        Spacer(1, 0.15 * inch),
        Paragraph('Spacing Rules', h2),
        Paragraph(
            f"Use a minimum margin of {TOKENS['spacing']['min_margin_in']} in, a content gutter of {TOKENS['spacing']['content_gutter_in']} in, and paragraph spacing of {TOKENS['spacing']['paragraph_space_after_pt']} pt. Keep text boxes below {int(TOKENS['spacing']['max_textbox_fill_ratio']*100)}% fill to preserve whitespace and readability.",
            body
        ),
        Spacer(1, 0.1 * inch),
        Paragraph('Caption: The generator enforces simple anti-overlap rules by reserving text and visual bands instead of auto-fitting content into every free pixel.', cap)
    ])
    doc.build(story)


if __name__ == '__main__':
    make_docx()
    make_pptx()
    make_pdf()
    print('Generated:', *(str(p) for p in OUT.iterdir()), sep='\n- ')
