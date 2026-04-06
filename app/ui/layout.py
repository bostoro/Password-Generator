from nicegui import ui
from .view_passwords import render_view_passwords
from .update_master import render_update_master
from .exit_app import render_exit_app
import datastore as datastore

def setup_master_password_ui(on_success):
    with ui.card().classes('absolute-center w-full max-w-md p-6 shadow-xl rounded-2xl'):
        ui.label('Welcome to Password Manager').classes('text-2xl font-bold mb-4 text-primary text-center w-full')
        ui.label('Please set up your master password').classes('mb-4 text-center w-full')
        master = ui.input('New Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
        
        def on_set():
            pwd = master.value
            if not pwd:
                ui.notify('Password cannot be empty', type='warning')
                return
            if datastore.set_master_password(pwd):
                ui.notify('Master password set!', type='positive')
                on_success()
            else:
                ui.notify('Error setting master password', type='negative')
                
        ui.button('Set Password', on_click=on_set).classes('w-full')

def build_main_ui():
    with ui.header().classes('items-center bg-primary text-white justify-between px-6 py-2'):
        ui.label('PASSWORD MANAGER').classes('text-xl font-bold')
        with ui.row().classes('gap-2'):
            with ui.dialog() as update_master_dialog, ui.card():
                render_update_master()
            ui.icon('key', size='sm').classes('cursor-pointer').on('click', lambda: update_master_dialog.open())
            with ui.dialog() as exit_dialog, ui.card():
                render_exit_app()
            ui.icon('close', size='sm').classes('cursor-pointer').on('click', lambda: exit_dialog.open())

    render_view_passwords()

_styles_injector = None

def set_styles_injector(func):
    global _styles_injector
    _styles_injector = func

@ui.page('/')
def render_layout():
    if _styles_injector:
        _styles_injector()
        
    if not datastore.master_password_exists():
        def on_setup_success():
            ui.navigate.to('/')
        setup_master_password_ui(on_setup_success)
    else:
        build_main_ui()
