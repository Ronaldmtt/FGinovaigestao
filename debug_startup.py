import traceback
import sys

with open("debug_error.log", "w", encoding='utf-8') as f:
    try:
        import app
        f.write("Import successful\n")
    except Exception:
        f.write(traceback.format_exc())
