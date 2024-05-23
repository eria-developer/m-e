from reportlab.pdfgen import canvas
import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from.models import DataOne  # Make sure to import your model correctly

def generate_report(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Set up fonts and colors
    p.setFont("Courier", 18)
    p.setFillColorRGB(0.14, 0.59, 0.74)
    p.drawString(60, 750, "List of all these")

    p.setFont("Helvetica", 16)
    p.setFillColorRGB(0, 0, 0)

    # Query the database for video games
    videogames = DataOne.objects.all()  # Adjusted to match your model

    position_y = 700
    for videogame in videogames:
        p.drawString(60, position_y, videogame.name)
        position_y -= 25

    # Finalize the PDF
    p.showPage()
    p.save()

    # Return the PDF as a response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="videogames.pdf"'
    return response
