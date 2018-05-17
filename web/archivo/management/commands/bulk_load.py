#!/usr/bin/env python

import os
import sys
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from collections import defaultdict 
from archivo.models import Archivador, Documento, Etiqueta

LABELS = ('2014', '2015', '2016', '2017', '2018', 'gastos', 'ingresos')
DATA_DIR = os.path.normpath(os.path.join(settings.BASE_DIR, '..', 'data'))

class Command(BaseCommand):
    help = 'Carga documentos a partir de una hoja csv'

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
   
    def get_data(self):
        data = defaultdict(list)
        for archivador in os.listdir(DATA_DIR):
            archivador_full_path = os.path.join(DATA_DIR, archivador)
            if os.path.isdir(archivador_full_path):
                archivador = archivador.upper()
                for (dir_path, dir_names, file_names) in os.walk(archivador_full_path):
                    for file_name in file_names:
                        if file_name.lower().endswith('.pdf'):
                            full_name = os.path.join(dir_path, file_name)
                            data[archivador].append(full_name)
        return data

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
        data = self.get_data()
        
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
