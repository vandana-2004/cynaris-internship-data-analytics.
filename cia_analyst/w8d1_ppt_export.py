from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


NAVY = RGBColor(31, 45, 61)
BLUE = RGBColor(45, 105, 160)
DARK = RGBColor(55, 65, 75)
LIGHT = RGBColor(242, 246, 250)


def add_heading(slide, text):
    box = slide.shapes.add_textbox(
        Inches(0.7), Inches(0.45), Inches(8.5), Inches(0.8)
    )
    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(26)
    paragraph.font.bold = True
    paragraph.font.color.rgb = NAVY


def add_footer(slide, page_number):
    box = slide.shapes.add_textbox(
        Inches(0.7), Inches(7.05), Inches(8.5), Inches(0.25)
    )
    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = f"CIA Data Analyst | Executive Report | {page_number}"
    paragraph.font.size = Pt(9)
    paragraph.font.color.rgb = DARK


def add_body(slide, text, top=1.6, font_size=20):
    box = slide.shapes.add_textbox(
        Inches(0.9), Inches(top), Inches(8.1), Inches(4.9)
    )
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(0.15)
    frame.margin_right = Inches(0.15)
    frame.vertical_anchor = MSO_ANCHOR.TOP

    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(font_size)
    paragraph.font.color.rgb = DARK


def create_presentation(output_path, filename, summary, insights):
    if len(insights) != 5:
        raise ValueError("The presentation requires exactly five insights.")

    presentation = Presentation()
    presentation.slide_width = Inches(10)
    presentation.slide_height = Inches(7.5)

    # Slide 1: Title
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = LIGHT

    title = slide.shapes.add_textbox(
        Inches(0.8), Inches(2.1), Inches(8.4), Inches(1.2)
    )
    paragraph = title.text_frame.paragraphs[0]
    paragraph.text = "Executive Data Analysis"
    paragraph.alignment = PP_ALIGN.CENTER
    paragraph.font.size = Pt(34)
    paragraph.font.bold = True
    paragraph.font.color.rgb = NAVY

    subtitle = slide.shapes.add_textbox(
        Inches(1), Inches(3.4), Inches(8), Inches(0.8)
    )
    paragraph = subtitle.text_frame.paragraphs[0]
    paragraph.text = f"Dataset: {filename}"
    paragraph.alignment = PP_ALIGN.CENTER
    paragraph.font.size = Pt(19)
    paragraph.font.color.rgb = BLUE

    add_footer(slide, 1)

    # Slide 2: Executive summary
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )
    add_heading(slide, "Executive Summary")
    add_body(slide, summary, top=1.45, font_size=15)
    add_footer(slide, 2)

    # Slides 3–7: Five verified insights
    for index, insight in enumerate(insights, start=1):
        slide = presentation.slides.add_slide(
            presentation.slide_layouts[6]
        )
        add_heading(slide, f"Key Insight {index}")
        add_body(slide, insight, top=2.0, font_size=23)
        add_footer(slide, index + 2)

    # Slide 8: Recommendations
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )
    add_heading(slide, "Recommended Next Steps")

    recommendations = [
        "Investigate the drivers behind the observed numeric results.",
        "Compare available categories to identify meaningful differences.",
        "Review data quality regularly, including missing and duplicate records.",
    ]

    recommendation_text = "\n\n".join(
        f"{index}. {item}"
        for index, item in enumerate(recommendations, start=1)
    )

    add_body(slide, recommendation_text, top=1.8, font_size=19)
    add_footer(slide, 8)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(output_path)

    return str(output_path)