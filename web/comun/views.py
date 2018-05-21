from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def homepage(request):
    from archivo.models import Archivador, Documento
    return render(request, 'homepage.html', {
        'title': 'Hipatia - Archivo documental',
        'archivadores': Archivador.objects.all().order_by('nombre'),
        'documentos': Documento.objects.all(),
        })
