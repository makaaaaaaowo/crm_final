from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def html2pdf(html_content):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error al generar el PDF", status=500)