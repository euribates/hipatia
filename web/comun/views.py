from django.shortcuts import render

# Create your views here.

def homepage(request):
    from archivo.models import Archivador, Documento
    return render(request, 'homepage.html', {
        'title': 'Hipatia - Archivo documental',
        'archivadores': Archivador.objects.all().order_by('nombre'),
        'documentos': Documento.objects.all(),
        })
