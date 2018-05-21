#!/usr/bin/env python

from django.conf import settings
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from archivo.models import Documento

class Searcher:

    def __init__(self):
        self.ix = open_dir(settings.INDEX_DIR)
        self.query_parser = QueryParser("content", schema=self.ix.schema)

    def look_for(self, s):
        s = str(s)
        q = self.query_parser.parse(s)
        with self.ix.searcher() as s:
            return [
                Documento.objects.get(pk=int(item['id_documento']))
                for item in s.search(q)
                ]


index = Searcher()
        

    
