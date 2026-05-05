from nicegui import ui
from .view_passwords import render_view_passwords
from .update_master import render_update_master
from .exit_app import render_exit_app
from services.password_service import PasswordService
import datastore as datastore

_current_service = None

def setup_master_password_ui(on_success):
    with ui.card().classes('absolute-center w-full max-w-md p-6 shadow-xl rounded-2xl'):
        ui.label('Welcome to Password Manager').classes('text-2xl font-bold mb-4 text-primary text-center w-full')
        username = ui.input('Username').classes('w-full mb-2')
        master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')

        def on_login():
            u = username.value
            pwd = master.value
            if not u or not pwd:
                ui.notify('All fields required', type='warning')
                return
            if not datastore.master_password_exists(u):
                ui.notify('Username not found', type='negative')
                return
            if datastore.check_master_password(u, pwd):
                meta = datastore.get_meta(u)
                on_success(meta, pwd)
            else:
                ui.notify('Wrong master password!', type='negative')
        
        def on_register():
            u = username.value
            pwd = master.value
            if not u or not pwd:
                ui.notify('All fields required', type='warning')
                return
            if datastore.master_password_exists(u):
                ui.notify('Username already exists', type='negative')
                return
            if datastore.set_master_password(u, pwd):
                meta = datastore.get_meta(u)
                on_success(meta, pwd)
            else:
                ui.notify('Error creating user', type='negative')

        master.on('keydown.enter', lambda: on_login())
        with ui.row().classes('w-full gap-2'):
            ui.button('Login', on_click=on_login).classes('w-full')
            ui.button('Register', on_click=on_register).classes('w-full')

def build_main_ui(service):
    def on_logout():
        global _current_service
        _current_service = None
        ui.navigate.to('/')
        
    with ui.header().classes('items-center bg-primary text-white justify-between px-6 py-2'):
        ui.label('PASSWORD MANAGER').classes('text-xl font-bold')
        with ui.row().classes('gap-2'):
            with ui.dialog() as update_master_dialog, ui.card():
                render_update_master(service)
            ui.icon('key', size='sm').classes('cursor-pointer').on('click', lambda: update_master_dialog.open())
            ui.icon('logout', size='sm').classes('cursor-pointer').on('click', on_logout)
            with ui.dialog() as exit_dialog, ui.card():
                render_exit_app()
            ui.icon('close', size='sm').classes('cursor-pointer').on('click', lambda: exit_dialog.open())

    render_view_passwords(service)

_styles_injector = None

def set_styles_injector(func):
    global _styles_injector
    _styles_injector = func

@ui.page('/')
def render_layout():
    global _current_service
    if _styles_injector:
        _styles_injector()

    if _current_service:
        build_main_ui(_current_service)
        return
        
    def on_setup_success(meta, pwd):
        global _current_service
        _current_service = PasswordService(meta.username, meta.id, pwd)
        ui.navigate.to('/')

    setup_master_password_ui(on_setup_success)