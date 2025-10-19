"""
Convert Part A Technical Design Document from TXT to PDF
Uses reportlab for PDF generation with professional formatting
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def create_pdf_from_txt(txt_file_path, pdf_file_path):
    """
    Convert text document to formatted PDF

    Args:
        txt_file_path: Path to input text file
        pdf_file_path: Path to output PDF file
    """

    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for PDF elements
    story = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=5,
        backColor=colors.HexColor('#ecf0f1')
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#c0392b'),
        fontName='Courier',
        backColor=colors.HexColor('#f8f9fa'),
        borderWidth=1,
        borderColor=colors.HexColor('#dee2e6'),
        borderPadding=8,
        leftIndent=20,
        rightIndent=20
    )

    separator_style = ParagraphStyle(
        'Separator',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#95a5a6'),
        spaceAfter=6,
        spaceBefore=6
    )

    # Read text file
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process lines
    in_code_block = False
    code_block = []

    for line in lines:
        line = line.rstrip()

        # Skip separator lines
        if line.startswith('======='):
            story.append(Spacer(1, 0.1*inch))
            continue

        # Empty line
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue

        # Detect code blocks
        if line.startswith('```') or line.strip() == '':
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_block)
                if code_text.strip():
                    # Escape special characters for reportlab
                    code_text = code_text.replace('&', '&amp;')
                    code_text = code_text.replace('<', '&lt;')
                    code_text = code_text.replace('>', '&gt;')
                    para = Paragraph(f'<font face="Courier" size="8">{code_text}</font>', code_style)
                    story.append(para)
                    story.append(Spacer(1, 0.1*inch))
                code_block = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_block.append(line)
            continue

        # Detect headings based on formatting
        if line.startswith('PART A:') or line.startswith('ML Production System'):
            para = Paragraph(line, title_style)
            story.append(para)
        elif line.endswith(':') and len(line.split()) <= 10 and not line.startswith(' ') and not line.startswith('-'):
            # Section heading
            if any(x in line for x in ['OVERVIEW', 'SELECTION', 'STRATEGY', 'PIPELINE', 'MONITORING', 'CONSIDERATIONS', 'OPTIMIZATION', 'FEEDBACK', 'SECURITY', 'CONCLUSION']):
                para = Paragraph(line, heading1_style)
                story.append(para)
            else:
                para = Paragraph(line, heading2_style)
                story.append(para)
        elif line.startswith('Author:') or line.startswith('Date:') or line.startswith('Version:'):
            para = Paragraph(line, separator_style)
            story.append(para)
        elif line.startswith('-') or line.startswith('*') or line.startswith('•'):
            # Bullet point
            line = line.lstrip('-*• ').strip()
            if line:
                para = Paragraph(f'• {line}', body_style)
                story.append(para)
        elif line.startswith('  ') or line.startswith('\t'):
            # Indented text (code or sub-bullet)
            line = line.strip()
            if line:
                # Escape special characters
                line = line.replace('&', '&amp;')
                line = line.replace('<', '&lt;')
                line = line.replace('>', '&gt;')
                para = Paragraph(f'<font face="Courier" size="9">{line}</font>', body_style)
                story.append(para)
        else:
            # Normal paragraph
            if line.strip():
                # Escape special characters
                line = line.replace('&', '&amp;')
                line = line.replace('<', '&lt;')
                line = line.replace('>', '&gt;')
                para = Paragraph(line, body_style)
                story.append(para)

    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {pdf_file_path}")


def main():
    """Main function to convert TXT to PDF"""

    # File paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_file = os.path.join(base_dir, "Part_A_Technical_Design.txt")
    pdf_file = os.path.join(base_dir, "Part_A_Technical_Design.pdf")

    # Check if text file exists
    if not os.path.exists(txt_file):
        print(f"Error: Text file not found: {txt_file}")
        return

    print(f"Converting {txt_file} to PDF...")
    print(f"Output: {pdf_file}")

    try:
        create_pdf_from_txt(txt_file, pdf_file)

        # Get file size
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"PDF size: {size_kb:.2f} KB")
        print(f"\nSuccess! PDF created at: {pdf_file}")

    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
