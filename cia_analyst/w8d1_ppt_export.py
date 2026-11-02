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


def create_presentation(
    output_path,
    filename,
    summary,
    insights,
    recommendations,
):
    if not isinstance(insights, list) or len(insights) != 5:
        raise ValueError(
            "The presentation requires exactly five insights."
        )

    if not all(
        isinstance(item, str) and item.strip()
        for item in insights
    ):
        raise ValueError("All five insights must be non-empty strings.")

    if (
        not isinstance(recommendations, list)
        or len(recommendations) != 5
        or not all(
            isinstance(item, str) and item.strip()
            for item in recommendations
        )
    ):
        raise ValueError(
            "The presentation requires exactly five non-empty recommendations."
        )

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
    paragraph.text = f"Dataset: {Path(filename).name}"
    paragraph.alignment = PP_ALIGN.CENTER
    paragraph.font.size = Pt(19)
    paragraph.font.color.rgb = BLUE

    add_footer(slide, 1)

    # Slides 2-6: Five verified insights
    for index, insight in enumerate(insights, start=1):
        slide = presentation.slides.add_slide(
            presentation.slide_layouts[6]
        )

        add_heading(slide, f"Key Insight {index}")
        add_body(slide, insight, top=2.0, font_size=23)
        add_footer(slide, index + 1)

    # Slide 7: AI-generated business recommendations
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )

    add_heading(slide, "Business Recommendations")

    recommendation_text = "\n\n".join(
        f"{index}. {item}"
        for index, item in enumerate(recommendations, start=1)
    )

    box = slide.shapes.add_textbox(
        Inches(0.9), Inches(1.5), Inches(8.1), Inches(5.2)
    )

    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(0.15)
    frame.margin_right = Inches(0.15)
    frame.vertical_anchor = MSO_ANCHOR.TOP

    for index, item in enumerate(recommendations):
        paragraph = (
            frame.paragraphs[0]
            if index == 0
            else frame.add_paragraph()
        )
        paragraph.text = f"{index + 1}. {item}"
        paragraph.font.size = Pt(16)
        paragraph.font.color.rgb = DARK
        paragraph.space_after = Pt(15)

    add_footer(slide, 7)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    presentation.save(output_path)

    return str(output_path)
