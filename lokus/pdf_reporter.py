from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, red, orange, yellow, green

from lokus.lgpd_validator import LGPDIssue, LGPDIssueSeverity
from lokus.security_validator import SecurityIssue, SecurityIssueSeverity


def pdf_reporter(
    swagger_file_path: str,
    findings: List[Dict[str, Any]],
    security_issues: Optional[List[SecurityIssue]] = None,
    lgpd_issues: Optional[List[LGPDIssue]] = None,
):
    """
    Generates a PDF report based on provided security and LGPD issues,
    and general findings.

    Args:
        output_filename (str): The name of the output PDF file (e.g., "report.pdf").
        findings (List[Dict[str, Any]]): A list of general findings.
        security_issues (Optional[List[SecurityIssue]]): A list of security issues.
        lgpd_issues (Optional[List[LGPDIssue]]): A list of LGPD issues.
    """

    output_filename = (
        f"swagger_validator_report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles for different text elements
    h1 = styles["h1"]
    h2 = styles["h2"]
    normal_style = styles["Normal"]
    bold_style = ParagraphStyle("Bold", parent=normal_style, fontName="Helvetica-Bold")

    # Severity specific colors
    severity_colors = {
        SecurityIssueSeverity.CRITICAL: red,
        SecurityIssueSeverity.HIGH: orange,
        SecurityIssueSeverity.MEDIUM: yellow,
        SecurityIssueSeverity.LOW: green,
        LGPDIssueSeverity.HIGH: red,
        LGPDIssueSeverity.MEDIUM: yellow,
        LGPDIssueSeverity.LOW: green,
    }

    # --- Title Page ---
    story.append(Paragraph("Swagger Validator", h1))
    story.append(Spacer(1, 0.2 * inch))
    now = datetime.now()
    story.append(
        Paragraph(
            f"Generated on {now.strftime('%-m/%-d/%Y, %-I:%M:%S %p')} GMT-3",
            normal_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Swagger file analyzed: {swagger_file_path}"))

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Summary of Findings and Issues", normal_style))
    story.append(PageBreak())

    # --- General Findings Section ---
    story.append(Paragraph("General Findings", h2))
    story.append(Spacer(1, 0.2 * inch))
    if findings:
        for i, finding in enumerate(findings):
            story.append(
                Paragraph(
                    f"<b>Finding {i + 1}:</b> {finding.get('title', 'N/A')}",
                    bold_style,
                )
            )
            if "description" in finding:
                story.append(Paragraph(finding.get("description", "N/A"), normal_style))
            story.append(Spacer(1, 0.1 * inch))
    else:
        story.append(Paragraph("No general findings to report.", normal_style))
    story.append(PageBreak())

    # --- Security Issues Section ---
    story.append(Paragraph("Security Issues", h2))
    story.append(Spacer(1, 0.2 * inch))
    if security_issues:
        for issue in security_issues:
            severity_color = severity_colors.get(issue.severity, black)
            story.append(
                Paragraph(
                    f"<font color='{severity_color}'><b>Severity:</b> {issue.severity.value}</font>",
                    bold_style,
                )
            )
            story.append(Paragraph(f"<b>Rule ID:</b> {issue.rule_id}", bold_style))
            story.append(Paragraph(f"<b>Title:</b> {issue.title}", bold_style))
            story.append(
                Paragraph(
                    f"<b>Description:</b> {issue.description}",
                    normal_style,
                )
            )
            story.append(Paragraph(f"<b>Path:</b> {issue.path}", normal_style))
            story.append(
                Paragraph(
                    f"<b>Recommendation:</b> {issue.recommendation}",
                    normal_style,
                )
            )
            story.append(
                Paragraph(f"<b>Reference:</b> {issue.reference}", normal_style)
            )
            story.append(Spacer(1, 0.2 * inch))
    else:
        story.append(Paragraph("No security issues to report.", normal_style))
    story.append(PageBreak())

    # --- LGPD Issues Section ---
    story.append(Paragraph("LGPD Issues", h2))
    story.append(Spacer(1, 0.2 * inch))
    if lgpd_issues:
        for issue in lgpd_issues:
            severity_color = severity_colors.get(issue.severity, black)
            story.append(
                Paragraph(
                    f"<font color='{severity_color}'><b>Severity:</b> {issue.severity.value}</font>",
                    bold_style,
                )
            )
            story.append(Paragraph(f"<b>Rule ID:</b> {issue.rule_id}", bold_style))
            story.append(Paragraph(f"<b>Title:</b> {issue.title}", bold_style))
            story.append(
                Paragraph(
                    f"<b>Description:</b> {issue.description}",
                    normal_style,
                )
            )
            story.append(Paragraph(f"<b>Path:</b> {issue.path}", normal_style))
            story.append(
                Paragraph(
                    f"<b>Recommendation:</b> {issue.recommendation}",
                    normal_style,
                )
            )
            if issue.reference:
                story.append(
                    Paragraph(f"<b>Reference:</b> {issue.reference}", normal_style)
                )
            story.append(Spacer(1, 0.2 * inch))
    else:
        story.append(Paragraph("No LGPD issues to report.", normal_style))
    story.append(PageBreak())

    # --- Build the PDF ---
    try:
        doc.build(story)
        print(f"PDF report '{output_filename}' generated successfully!")
    except Exception as e:
        print(f"Error generating PDF: {e}")
