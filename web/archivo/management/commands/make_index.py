#!/usr/bin/env python

import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from whoosh.index import create_in
from whoosh.fields import ID, TEXT, Schema

class Command(BaseCommand):
    help = 'Crear índice whoosh'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creadon índice', ending=' ')
        schema = Schema(
            id_documento=ID(stored=True),
            name=TEXT(stored=True),
            labels=TEXT(stored=True),
            content=TEXT()
            )
        if not os.path.isdir(settings.INDEX_DIR):
            os.makedirs(settings.INDEX_DIR)
            self.stdout.write('D', ending='')
        index = create_in(settings.INDEX_DIR, schema)
        self.stdout.write('I', ending='')
        self.stdout.write(' [ok]')

        

