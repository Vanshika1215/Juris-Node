import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(analysis_data: dict) -> io.BytesIO:
    """Builds a formatted contract legal risk summary file using ReportLab."""
    buffer = io.BytesIO()
    
    # Establish document layout parameters
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Palette Styling
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    # Document Content Elements Allocation
    contract_name = analysis_data.get("contract_name", "Evaluated Document")
    story.append(Paragraph(f"Juris Node — Assessment Brief", title_style))
    story.append(Paragraph(f"Target Asset: {contract_name}", body_style))
    story.append(Paragraph(f"Overall Safety Rating: {analysis_data.get('overall_safety_score', 0)}/100", section_style))
    story.append(Spacer(1, 10))
    
    # Summary Node
    story.append(Paragraph("Executive Summary Breakdown", section_style))
    story.append(Paragraph(analysis_data.get("executive_summary", "No brief parsed."), body_style))
    story.append(Spacer(1, 10))
    
    # Recommendations Mapping Loop
    story.append(Paragraph("Arbiter Strategic Recommendations", section_style))
    for rec in analysis_data.get("recommendations", []):
        story.append(Paragraph(f"• {rec}", body_style))
    
    # Render Layout
    doc.build(story)
    buffer.seek(0)
    return buffer