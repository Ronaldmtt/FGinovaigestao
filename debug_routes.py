from app import app
import routes
import sys

print("DEBUG: Checking URL Map...")
print(app.url_map)

print("\nDEBUG: Checking if 'index' is in view_functions...")
if 'index' in app.view_functions:
    print("Index IS in view functions")
else:
    print("Index is NOT in view functions")
