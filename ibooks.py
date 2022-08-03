#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

from ibooks_highlights.models import BookList
from ibooks_highlights import ibooksdb

from random import choice

import os


def get_booklist(path: pathlib.Path) -> BookList:
    book_list = BookList(path)
    annos = ibooksdb.fetch_annotations()
    book_list.populate_annotations(annos)
    return book_list

TOP_LEFT = '┌'
TOP_RIGHT = '┐'
MIDDLE_LEFT = '├'
MIDDLE_RIGHT = '┤'
BOTTOM_LEFT = '└'
BOTTOM_RIGHT = '┘'

def fit_width(text, width = 40):
    words = text.split(' ')

    lines = []

    i = -1
    while i + 1 < len(words):
        line = words[i + 1]
        i += 1

        while i + 1 < len(words) and len(line + ' ' + words[i + 1]) < width:
            line += ' ' + words[i + 1]
            i += 1

        lines.append(line)

    return lines

def format_annotation(annotation, note, book_name, width = 60):
    # Split text with spaces into lines
    annotation = annotation.replace('\n', ' ')
    annotation = annotation.strip()

    fit_annotation = fit_width(annotation, width)
    fit_note = None

    if note is not None:
        note = note.replace('\n', ' ')
        note = note.strip()

        fit_note = fit_width(note, width)

    max_width = 0

    if fit_note is not None:
        max_width = max(max(len(s) for s in fit_annotation), max(len(s) for s in fit_note))
    else:
        max_width = max(len(s) for s in fit_annotation)

    size = max_width + 2

    res = [TOP_LEFT + '─' * size + TOP_RIGHT]

    for s in fit_annotation:
        res.append('│' + (' ' + s + ' ' * size)[:size] + '│')

    if fit_note is not None:
        res.append(MIDDLE_LEFT + '─' * size + MIDDLE_RIGHT)

        for s in fit_note:
            res.append('│' + (' ' + s + ' ' * size)[:size] + '│')

    res.append(BOTTOM_LEFT + '─' * size + BOTTOM_RIGHT)

    if book_name != 'None':
        res.append(' ' * (size - len(book_name)) + book_name)

    return '\n'.join(res)

def random(bookdir):
    book_list = get_booklist(bookdir)

    random_book = choice(list(book_list.books.keys()))

    book = book_list.books[random_book]

    book_name = book.title

    anno = choice(book.annotations)

    print(format_annotation(anno.selected_text, anno.note, book_name))


if __name__ == '__main__':
    bookdir = os.environ.get('IBOOKS_HIGHLIGHT_DIR')
    if bookdir is None:
        raise Exception('IBOOKS_HIGHLIGHT_DIR not set')

    random(pathlib.Path(bookdir))
