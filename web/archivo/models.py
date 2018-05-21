import datetime
from django.db import models

# Create your models here.

class Etiqueta(models.Model):

    id_etiqueta = models.AutoField(primary_key=True)
    texto = models.SlugField(max_length=48, unique=True)

    def __str__(self):
        return self.texto


class Archivador(models.Model):

    class Meta:
        verbose_name = 'Archivador'
        verbose_name_plural = 'Archivadores'

    id_archivador = models.AutoField(primary_key=True)
    nombre = models.SlugField(max_length=32, unique=True)
    n_docs = models.IntegerField(default=0)
    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)
    f_acceso = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        )

    def __str__(self):
        return self.nombre


def get_upload_dir(instance, filename):
    return '{}/{}'.format(
        instance.archivador.nombre,
        filename,
        )


class Documento(models.Model):
    
    class Meta:
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        unique_together = ('archivador', 'nombre',)

    id_documento = models.AutoField(primary_key=True)
    archivador = models.ForeignKey(
        Archivador,
        related_name='documentos',
        on_delete=models.PROTECT,
        )
    nombre = models.CharField(max_length=64, unique=True)
    archivo = models.FileField(upload_to=get_upload_dir)
    n_paginas = models.PositiveIntegerField(
            default=0,
            editable=False,
            )
    etiquetas = models.ManyToManyField(Etiqueta)
    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)
    f_acceso = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        )

    def __str__(self):
        return '{} [{}]'.format(
            self.nombre.split('/')[-1],
            ', '.join([str(lbl) for lbl in self.etiquetas.all()]),
            )

    def lista_etiquetas(self):
        return list(self.etiquetas.all())



