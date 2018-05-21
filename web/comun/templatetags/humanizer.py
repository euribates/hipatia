#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from django import template
from comun import filters

register = template.Library()

register.filter('as_filesize', filters.as_filesize)
