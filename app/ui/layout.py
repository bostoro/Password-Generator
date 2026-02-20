from nicegui import ui
from .generate_password import render_generate_password
from .save_password import render_save_password
from .view_passwords import render_view_passwords
from .delete_password import render_delete_password
from .update_master import render_update_master
from .check_strength import render_check_strength
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

    with ui.tabs().classes('w-full mt-4') as tabs:
        tab_gen = ui.tab('1. Generate')
        tab_save = ui.tab('2. Save')
        tab_view = ui.tab('3. View')
        tab_del = ui.tab('4. Delete')
        tab_upd = ui.tab('5. Update Master')
        tab_chk = ui.tab('6. Check Strength')
        tab_ext = ui.tab('7. Exit')

    with ui.tab_panels(tabs, value=tab_gen).classes('w-full max-w-5xl mx-auto bg-transparent'):
        with ui.tab_panel(tab_gen):
            render_generate_password()
        with ui.tab_panel(tab_save):
            render_save_password()
        with ui.tab_panel(tab_view):
            render_view_passwords()
        with ui.tab_panel(tab_del):
            render_delete_password()
        with ui.tab_panel(tab_upd):
            render_update_master()
        with ui.tab_panel(tab_chk):
            render_check_strength()
        with ui.tab_panel(tab_ext):
            render_exit_app()

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
