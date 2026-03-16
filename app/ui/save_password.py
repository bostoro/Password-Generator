from nicegui import ui
import datastore as datastore

def render_save_password():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Save a Password').classes('text-2xl font-bold mb-4 text-primary')
        
        username = ui.input('Username or Email').classes('w-full mb-2')
        platform = ui.input('Website / Platform').classes('w-full mb-2')
        password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-2')
        master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
        
        def on_save():
            u = username.value
            p_form = platform.value
            pwd = password.value
            m = master.value
            
            if not u or not p_form or not pwd or not m:
                ui.notify('All fields are required!', type='warning')
                return
                
            if not datastore.check_master_password(m):
                ui.notify('Wrong master password!', type='negative')
                return
                
            saved_id = datastore.save_password(u, p_form, pwd, m)
            if saved_id:
                ui.notify(f'Password saved with ID: {saved_id}', type='positive')
                username.value = ''
                platform.value = ''
                password.value = ''
                master.value = ''
            else:
                ui.notify('Could not save! Duplicate?', type='negative')
                
        ui.button('Save Manually', on_click=on_save).classes('w-full mt-2')
