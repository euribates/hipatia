#!/usr/bin/env python

import sys
from django.core.management.base import BaseCommand, CommandError
import csv
from collections import defaultdict 
from archivo.models import Archivador, Documento

class Command(BaseCommand):
    help = 'Carga documentos a partir de una hoja csv'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **kwargs):
        self.stdout.write('Bulk load', ending=' ')
        filename = kwargs.get('filename')
        self.stdout.write('from file {}'.format(filename))
        data = defaultdict(list)
        with open(filename, 'r', encoding='iso-8859-1') as stream:
            reader = csv.reader(stream, dialect=csv.excel_tab)
            columns = next(reader)
            for (archivo, documento) in reader:
                data[archivo].append(documento)
        for key in data:
            if Archivador.objects.filter(nombre=key).count == 0:
                arch = Archivador(nombre=nombre, n_docs=len(data[key]))
                arch.save()
            else:
                arch = Archivador.objects.get(nombre=nombre)
            for f in data[key]:
                exists = Archivo.objects  \
                    .filter(archivador=arch, nombre=f) \
                    .count() > 0
                if not exists:

                self.stdout.write('{} --> {}'.format(
                    key, len(data[key])
                ))
