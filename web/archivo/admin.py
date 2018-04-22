from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Etiqueta)

@admin.register(models.Archivador)
class ArchivadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'n_docs',)    

@admin.register(models.Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('archivador', 'nombre', 'archivo',)    


