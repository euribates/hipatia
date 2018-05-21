from django.shortcuts import render
from comun.searcher import index

from . import models

# Create your views here.

def search(request):
    query = request.GET.get('query')
    docs = index.look_for(query)
    return render(request, 'archivo/search_results.html', {
        'docs': docs,
        'num_docs': len(docs),
        'query': query,
        })

def archivador_detail(request, id_archivador):
    archivador = models.Archivador.objects.get(pk=id_archivador)
    documentos = models.Documento.objects.all().filter(archivador=id_archivador)
    return render(request, 'archivo/archivador_detail.html', {
        'archivador': archivador,
        'documentos': documentos,
        'num_docs': documentos.count(),
        })
