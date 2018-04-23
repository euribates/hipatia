#!/usr/bin/env python

import os
import sys
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import csv
from collections import defaultdict 
from archivo.models import Archivador, Documento, Etiqueta

LABELS = ('2014', '2015', '2016', '2017', '2018', 'gastos', 'ingresos')

class Command(BaseCommand):
    help = 'Carga documentos a partir de una hoja csv'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def get_data(self, filename):
        data = defaultdict(list)
        with open(filename, 'r', encoding='iso-8859-1') as stream:
            reader = csv.reader(stream, dialect=csv.excel_tab)
            columns = [s.lower() for s in next(reader)]
            for (archivador, archivo) in reader:
                data[archivador].append(archivo)
        return data

    def make_media(self):
        if not os.path.isdir(settings.MEDIA_ROOT):
            self.stdout.write('Creando directorio MEDIA_ROOT {}'.format(settings.MEDIA_ROOT))
            os.mkdir(settings.MEDIA_ROOT)
        else:
            self.stdout.write('Directorio MEDIA_ROOT {} ya existe'.format(settings.MEDIA_ROOT))

    def make_labels(self):
        for label in LABELS:
            existe = Etiqueta.objects.filter(texto=label).count()
            if not existe:
                Etiqueta(texto=label).save()
   
    def copy_file(self, source, archivo, filename):
        target = os.path.join(settings.MEDIA_ROOT, archivo.nombre)
        if not os.path.isdir(target):
            os.mkdir(target)
        target = os.path.join(target, filename)
        if not os.path.exists(target):
            shutil.copyfile(source, target)


    def get_labels_from_filename(self, filename):
        patron = filename.lower()
        result = []
        if '-14-' in patron:
            result.append('2014')
        if '-15-' in patron:
            result.append('2015')
        if '-16-' in patron:
            result.append('2016')
        if '-17-' in patron:
            result.append('2017')
        if '-18-' in patron:
            result.append('2018')
        if 'gastos' in patron:
            result.append('gastos')
        if 'ingresos' in patron or 'ing-' in patron or 'ventas' in patron:
            result.append('ingresos')
        return set([
            Etiqueta.objects.get(texto=s)
            for s in result
            ])

    def handle(self, *args, **kwargs):
        self.make_media()
        self.make_labels()
        self.stdout.write('Bulk load', ending=' ')
        filename = kwargs.get('filename')
        self.stdout.write('from file {}'.format(filename))
        data = self.get_data(filename)
        for archivador in data: 
            archivos = data[archivador]
            self.stdout.write('A: {}'.format(archivador))
            if Archivador.objects.filter(nombre=archivador).count() == 0:
                arch = Archivador(nombre=archivador, n_docs=len(archivos))
                arch.save()
            else:
                arch = Archivador.objects.get(nombre=archivador)
            for filename in archivos:
                exists = Documento.objects  \
                    .filter(archivador=arch, nombre=filename) \
                    .count() > 0
                if exists:
                    doc = Documento.objects.get(archivador=arch, nombre=filename)
                    self.stdout.write(' - doc {} skipped (it exists)'.format(doc), ending=' ')
                else:
                    doc = Documento(
                        archivador=arch,
                        nombre=filename,
                        archivo='{}/{}'.format(arch.nombre, filename),
                        )
                    doc.save()
                    doc.etiquetas.set(self.get_labels_from_filename(filename))
                    doc.save()
                    self.stdout.write(' - save doc {} in archive {}'.format(filename, archivador), ending=' ')
                self.stdout.write('[copy file]', ending=' ')
                source = os.path.normpath(
                    os.path.join(settings.BASE_DIR, '..', 'data', arch.nombre, filename)
                    )
                self.copy_file(source, arch, filename)
                self.stdout.write('[Ok]')
