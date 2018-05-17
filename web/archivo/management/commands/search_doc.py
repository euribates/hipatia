#!/usr/bin/env python

import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from whoosh.index import open_dir 
from whoosh.qparser import QueryParser
from archivo.models import Documento

class Command(BaseCommand):

    help = 'Buscar documentos en hipatia'

    def add_arguments(self, parser):
        parser.add_argument('words', nargs='+')

    def handle(self, *args, **kwargs):
        words = kwargs['words'] 
        self.stdout.write('Buscado por: {}'.format(' '.join(words)))
        ix = open_dir(settings.INDEX_DIR)
        query_parser = QueryParser("content", schema=ix.schema)
        q = query_parser.parse(' '.join(words))
        with ix.searcher() as s:
            results = s.search(q)
            self.stdout.write('Encontrados {} documentos'.format(len(results)))
            for item in results:
                id_documento = int(item['id_documento'])
                doc = Documento.objects.get(pk=id_documento)
                print(id_documento, doc, file=self.stdout)
        
