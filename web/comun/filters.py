#!/usr/bin/env python


def as_filesize(d):
    '''retorna una descripcion textual del tamaño del fichero, redondeaado
    a las unidades más cercanas.
    '''
    if d < 1024:
        return '{:d} Bytes'.format(d)
    elif d < 1048576:
        return '{:.2f} KB.'.format(round(d / 1024.0, 2))
    elif d < 1073741824:
        return '{:.2f} MB.'.format(round(d / 1048576.0, 2))
    else:
        return '{:.2f} GB.'.format(round(d / 1073741824.0, 2))

