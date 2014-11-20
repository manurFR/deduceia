from contextlib import contextmanager
from StringIO import StringIO
import sys
from Sheet import Sheet


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def sheet_table(**kwargs):
    sheet = Sheet('test')
    sheet.exclude_cards(kwargs.get('excluded', []))
    sheet.own_cards(kwargs.get('owned', []))
    return sheet.table
