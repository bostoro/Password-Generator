from nicegui import ui
from .password_input import render_password_input


def render_save_password(service, on_cancel=None):
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Save a Password').classes('text-lg font-semibold mb-4')

        username = ui.input('Username or Email').classes('w-full mb-2')
        platform = ui.input('Website / Platform').classes('w-full mb-2')
        with ui.row().classes('w-full items-center gap-2 mb-2'):
            password = ui.input('Password', password=True,
                                password_toggle_button=True).classes('w-full')
            
            render_password_input(service, password)

        def on_save():
            u = username.value
            p_form = platform.value
            pwd = password.value

            if not u or not p_form or not pwd:
                ui.notify('All fields are required!', type='warning')
                return

            saved_id = service.save(u, p_form, pwd)
            if saved_id:
                ui.notify(
                    f'Password saved with ID: {saved_id}', type='positive')
                username.value = ''
                platform.value = ''
                password.value = ''
            else:
                ui.notify('Duplicate entry!', type='negative')

        with ui.row():
            ui.button('Cancel', on_click=lambda: on_cancel() if on_cancel else None)
            ui.button('Save', color='primary', on_click=on_save)
