from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(results):

    file_name = "report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Resume Shortlisting Report")

    c.setFont("Helvetica", 12)

    for r in results:

        text = f"{r['name']} | Score: {r['score']}% | ATS: {r['ats']}/100"
        c.drawString(50, y, text)
        y -= 30

        if y < 50:
            c.showPage()
            y = 750

    c.save()

    return file_name