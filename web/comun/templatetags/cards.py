#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from functools import partial
from django.urls import reverse
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


class CardNode(template.Node):
    
    def __init__(self, tag_name, title, klass='default', body=''):
        self.tag_name = tag_name
        self.klass = 'panel-{}'.format(klass)
        self.title = title
        self.body = body

    def render(self, context):
        title = self.title.resolve(context)
        buff = ['<div class="panel {}">'.format(self.klass)]
        buff.append(' <div class="panel-heading">')
        buff.append('  <h3 class="panel-title">{}</h3>'.format(title))
        buff.append(' </div>')
        buff.append(self.body_start_tag())
        buff.append(self.body.render(context))
        buff.append(self.body_end_tag())
        buff.append('</div>')
        return '\n'.join(buff)

    def body_start_tag(self):
        return {
            'card': ' <div class="panel-body">',
            'list_card': ' <ul class="list-group">',
            'table_card': ' <table class="table">',
            }.get(self.tag_name)

    def body_end_tag(self):
        return {
            'card': ' </div>',
            'list_card': ' </ul>',
            'table_card': ' </table>',
            }.get(self.tag_name)


def card(parser, token):
    try:
        args = token.split_contents()
        if len(args) == 2:
            tag_name, title = args
            klass = 'default'
        elif len(args) == 3:
            tag_name, title, klass = args
        else:
            raise ValueError('wrong number of arguments')
        nodelist = parser.parse(('endcard',))
        parser.delete_first_token()
        return CardNode(tag_name, template.Variable(title), klass, body=nodelist)
    except ValueError:
        raise template.TemplateSyntaxError("card tag requires one or two arguments")



register.tag('card', card)
register.tag('list_card', card)
register.tag('table_card', card)
