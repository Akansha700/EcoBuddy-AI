from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
    carbon,
    water,
    energy,
    score,
    filename="reports/EcoBuddy_Report.pdf"
):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>EcoBuddy AI Sustainability Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Carbon Footprint:</b> {carbon} kg CO₂", styles["BodyText"]))

    story.append(Paragraph(f"<b>Water Usage:</b> {water} Litres", styles["BodyText"]))

    story.append(Paragraph(f"<b>Energy Usage:</b> {energy} kWh", styles["BodyText"]))

    story.append(Paragraph(f"<b>Eco Score:</b> {score}/100", styles["BodyText"]))

    story.append(Paragraph("<br/>Recommendations", styles["Heading2"]))

    story.append(Paragraph("• Use public transport", styles["BodyText"]))

    story.append(Paragraph("• Save electricity", styles["BodyText"]))

    story.append(Paragraph("• Save water", styles["BodyText"]))

    story.append(Paragraph("• Choose eco-friendly products", styles["BodyText"]))

    doc.build(story)

    return filename