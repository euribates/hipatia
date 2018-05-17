#!/usr/bin/env python

import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from whoosh.index import open_dir 
from archivo.models import Documento

def load_text_from_pdf(path):
    cmd =['pdftotext', '-enc', 'UTF-8',  path, '-']
    result = subprocess.check_output(cmd)
    return result.decode('utf-8')

class Command(BaseCommand):

    help = 'índice whoosh'

    def handle(self, *args, **kwargs):
        self.stdout.write('Añadiendo contenidos al índice', ending=' ')
        ix = open_dir(settings.INDEX_DIR)
        writer = ix.writer()
        for d in Documento.objects.all():
            self.stdout.write(' - doc {}/{}'.format(d.id_documento, d.nombre), ending=' ')
            labels = '/'.join([str(l) for l in d.etiquetas.all()])
            content = load_text_from_pdf(d.archivo.path)
            self.stdout.write('({} bytes)'.format(len(content)), ending=' ')
            writer.add_document(
                id_documento=str(d.id_documento),
                name=d.nombre,
                labels=labels,
                content=content,
                )
            self.stdout.write('D', ending='')
            self.stdout.write(' [ok]')
            self.stdout.flush()
        writer.commit()
        
