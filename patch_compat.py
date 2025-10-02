# patch_compat.py
import sys

# Python 3.13 removed 'cgi', some packages like googletrans/httpx still import it
if sys.version_info >= (3, 13):
    import types
    sys.modules['cgi'] = types.ModuleType('cgi')

    # Optional: add dummy functions/classes to prevent AttributeError
    setattr(sys.modules['cgi'], 'FieldStorage', object)
    setattr(sys.modules['cgi'], 'parse_qs', lambda x: x)
    setattr(sys.modules['cgi'], 'parse_qsl', lambda x: x)
    setattr(sys.modules['cgi'], 'escape', lambda x: x)
