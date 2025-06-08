import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import (
    HexColor,
    white,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from svglib.svglib import svg2rlg

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
        swagger_file_path (str): Path to the analyzed Swagger file.
        findings (List[Dict[str, Any]]): A list of general findings.
        security_issues (Optional[List[SecurityIssue]]): A list of security issues.
        lgpd_issues (Optional[List[LGPDIssue]]): A list of LGPD issues.
    """

    output_filename = f"lokus_report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Document setup with custom margins
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    # Define color scheme
    primary_color = HexColor("#9000a5")  # Deep purple for primary elements
    secondary_color = HexColor("#5a007a")  # Darker purple for secondary elements
    header_background = HexColor("#B594B6")  # Light purple for header background
    header_border = HexColor("#9000a5")  # Matching border color for headers
    accent_color = HexColor("#3498db")  # Bright blue for accents and highlights

    # Define severity issue colors
    success_color = HexColor("#2ecc71")  # Green for low severity or success
    warning_color = HexColor("#f39c12")  # Yellow for medium severity or warning
    danger_color = HexColor("#e67e22")  # Orange for high severity or danger
    critical_color = HexColor("#e74c3c")  # Red for critical severity

    # Custom styles for different text elements
    title_style = ParagraphStyle(
        name="CustomTitle",
        parent=styles["Title"],
        fontSize=28,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    subtitle_style = ParagraphStyle(
        name="CustomSubtitle",
        parent=styles["Normal"],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName="Helvetica",
    )

    header_style = ParagraphStyle(
        name="CustomHeader",
        parent=styles["Heading1"],
        fontSize=20,
        spaceBefore=20,
        spaceAfter=20,
        fontName="Helvetica-Bold",
        borderWidth=2,
        borderColor=header_border,
        borderPadding=6,
        backColor=header_background,
    )

    subheader_style = ParagraphStyle(
        name="CustomSubHeader",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )

    normal_style = ParagraphStyle(
        name="CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    )

    bold_style = ParagraphStyle(
        name="CustomBold",
        parent=normal_style,
        fontName="Helvetica-Bold",
    )

    # Severity colors mapping
    severity_colors = {
        SecurityIssueSeverity.CRITICAL: critical_color,
        SecurityIssueSeverity.HIGH: danger_color,
        SecurityIssueSeverity.MEDIUM: warning_color,
        SecurityIssueSeverity.LOW: success_color,
        LGPDIssueSeverity.HIGH: danger_color,
        LGPDIssueSeverity.MEDIUM: warning_color,
        LGPDIssueSeverity.LOW: success_color,
    }

    def scale(drawing: Drawing, scaling_factor):
        """Scale a reportlab.graphics.shapes.Drawing() object while maintaining aspect ratio."""

        scaling_x = scaling_factor
        scaling_y = scaling_factor

        drawing.width = drawing.minWidth() * scaling_x
        drawing.height = drawing.height * scaling_y

        drawing.scale(scaling_x, scaling_y)
        return drawing

    def add_image(image_path, scaling_factor):
        """Add a centered SVG image file to the Flowable story."""

        try:
            if os.path.exists(image_path):
                drawing = svg2rlg(image_path)

                if drawing:
                    scaled_drawing = scale(drawing, scaling_factor=scaling_factor)

                    # Create a table with the drawing to center it
                    table = Table([[scaled_drawing]], colWidths=[None])
                    table.setStyle(
                        TableStyle(
                            [
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                            ]
                        )
                    )

                    story.append(table)
                    story.append(Spacer(1, 0.5 * inch))

        except Exception:
            story.append("")

    def create_summary_table():
        """Create a summary statistics table"""
        security_count = len(security_issues) if security_issues else 0
        lgpd_count = len(lgpd_issues) if lgpd_issues else 0
        findings_count = len(findings) if findings else 0

        # Count by severity
        critical_count = sum(
            1
            for issue in (security_issues or [])
            if issue.severity == SecurityIssueSeverity.CRITICAL
        )
        high_count = sum(
            1
            for issue in (security_issues or [])
            if issue.severity == SecurityIssueSeverity.HIGH
        )
        high_count += sum(
            1
            for issue in (lgpd_issues or [])
            if issue.severity == LGPDIssueSeverity.HIGH
        )

        summary_data = [
            ["Analysis Summary", ""],
            ["Total Security Issues", str(security_count)],
            ["Total LGPD Issues", str(lgpd_count)],
            ["General Findings", str(findings_count)],
            ["Critical Issues", str(critical_count)],
            ["High Severity Issues", str(high_count)],
        ]

        summary_table = Table(summary_data, colWidths=[3 * inch, 1.5 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (1, 0), accent_color),
                    ("TEXTCOLOR", (0, 0), (1, 0), white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("GRID", (0, 0), (-1, -1), 1, primary_color),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F8F9FA")),
                ]
            )
        )

        return summary_table

    def create_issue_card(issue, issue_type="Security"):
        """Create a professional card for each issue"""
        severity_color = severity_colors.get(issue.severity, primary_color)

        # Create issue data for table
        issue_data = [
            [Paragraph(f"{issue_type} Issue", bold_style), ""],
            [
                Paragraph("Severity", bold_style),
                Paragraph(
                    f'<font color="{severity_color}"><b>{issue.severity.value.upper()}</b></font>',
                    bold_style,
                ),
            ],
            [Paragraph("Rule ID", bold_style), Paragraph(issue.rule_id, normal_style)],
            [Paragraph("Title", bold_style), Paragraph(issue.title, bold_style)],
            [
                Paragraph("Description", bold_style),
                Paragraph(issue.description, normal_style),
            ],
            [Paragraph("Path", bold_style), Paragraph(issue.path, normal_style)],
            [
                Paragraph("Recommendation", bold_style),
                Paragraph(issue.recommendation, normal_style),
            ],
        ]

        if hasattr(issue, "reference") and issue.reference:
            issue_data.append(
                [
                    Paragraph("Reference", bold_style),
                    Paragraph(issue.reference, normal_style),
                ]
            )

        issue_table = Table(issue_data, colWidths=[1.5 * inch, 5 * inch])
        issue_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (1, 0), severity_color),
                    ("TEXTCOLOR", (0, 0), (1, 0), white),
                    ("FONTNAME", (0, 0), (1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (1, 0), 12),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("GRID", (0, 0), (-1, -1), 1, primary_color),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FDFDFE")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#F8F9FA")]),
                ]
            )
        )

        return KeepTogether([issue_table, Spacer(1, 0.3 * inch)])

    # --- Title Page ---
    add_image("static/logo-name.svg", 0.2)

    story.append(Paragraph("API Security & Compliance Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    now = datetime.now()
    story.append(
        Paragraph(
            f"Generated on {now.strftime('%B %d, %Y at %I:%M %p')} (GMT-3)",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    # File info table
    file_info_data = [
        ["Analyzed File", os.path.basename(swagger_file_path)],
        ["Full Path", swagger_file_path],
        ["Analysis Date", now.strftime("%Y-%m-%d")],
        ["Generated By", "Lokus Security & Compliance Analyzer"],
    ]

    file_info_table = Table(file_info_data, colWidths=[2 * inch, 4 * inch])
    file_info_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8F9FA")),
                ("GRID", (0, 0), (-1, -1), 1, primary_color),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ]
        )
    )

    story.append(file_info_table)
    story.append(Spacer(1, 0.5 * inch))

    # Summary section
    story.append(Paragraph("Results", header_style))
    story.append(create_summary_table())
    story.append(PageBreak())

    # --- General Findings Section ---
    story.append(Paragraph("General Findings", header_style))
    if findings:
        story.append(Paragraph("Detailed Analysis Results", subheader_style))
        for i, finding in enumerate(findings):
            finding_data = [
                [Paragraph(f"Finding #{i + 1}", bold_style), ""],
                [
                    Paragraph("Title", bold_style),
                    Paragraph(finding.get("type", "N/A"), normal_style),
                ],
                [
                    Paragraph("Description", bold_style),
                    Paragraph(finding.get("message", "N/A"), normal_style),
                ],
            ]

            finding_table = Table(finding_data, colWidths=[1.5 * inch, 5 * inch])
            finding_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (1, 0), secondary_color),
                        ("TEXTCOLOR", (0, 0), (1, 0), white),
                        ("FONTNAME", (0, 0), (1, 0), "Helvetica-Bold"),
                        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 1, primary_color),
                        ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F8F9FA")),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("WORDWRAP", (0, 0), (-1, -1), True),
                    ]
                )
            )

            story.append(finding_table)
            story.append(Spacer(1, 0.2 * inch))
    else:
        story.append(Paragraph("✅ No general findings identified.", normal_style))
        story.append(Spacer(1, 0.2 * inch))

    story.append(PageBreak())

    # --- Security Issues Section ---
    story.append(Paragraph("Security Issues", header_style))
    if security_issues:
        for issue in security_issues:
            story.append(create_issue_card(issue, "Security"))
    else:
        story.append(Paragraph("✅ No security issues identified.", normal_style))
        story.append(Spacer(1, 0.2 * inch))

    story.append(PageBreak())

    # --- LGPD Issues Section ---
    story.append(Paragraph("LGPD Compliance Issues", header_style))
    if lgpd_issues:
        for issue in lgpd_issues:
            story.append(create_issue_card(issue, "LGPD"))
    else:
        story.append(
            Paragraph("✅ No LGPD compliance issues identified.", normal_style)
        )
        story.append(Spacer(1, 0.2 * inch))

    # --- Build ththe resized SVG on the PDF at position e PDF ---
    try:
        doc.build(story)
        print(f"✅ PDF report '{output_filename}' generated successfully!")
        print(f"📄 Report saved to: {os.path.abspath(output_filename)}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
