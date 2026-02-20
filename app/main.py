import os
import sys
import ui.layout as layout
import datastore

from dotenv import load_dotenv
from nicegui import ui


load_dotenv()

# Prepare styles dictionary for injection
custom_colors = {}
styles_path = os.getenv('STYLES_PATH')
if styles_path and os.path.exists(styles_path):
    try:
        import json
        with open(styles_path, 'r') as f:
            custom_colors = json.load(f)
    except Exception as e:
        print(f"Error loading styles from {styles_path}: {e}")

def inject_styles():
    if custom_colors:
        ui.colors(**custom_colors)
    else:
        ui.colors(primary='purple')

layout.set_styles_injector(inject_styles)

def main():
    datastore.init_database()
    ui.run(title='Password Manager', favicon='🔐')

if __name__ in {"__main__", "__mp_main__"}:
    main()
