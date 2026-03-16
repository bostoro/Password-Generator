import string
import random
from nicegui import ui
import datastore as datastore

def generate_pwd(length, use_upper, use_lower, use_numbers, use_symbols):
    all_chars = ''
    if use_upper: all_chars += string.ascii_uppercase
    if use_lower: all_chars += string.ascii_lowercase
    if use_numbers: all_chars += string.digits
    if use_symbols: all_chars += string.punctuation
    
    if not all_chars:
        all_chars = string.ascii_letters + string.digits + string.punctuation
        
    if length <= 0:
        return ""
        
    return ''.join(random.choice(all_chars) for _ in range(length))

def render_generate_password():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Generate Password').classes('text-2xl font-bold mb-4 text-primary')
        
        length_input = ui.number('Password Length', value=16, format='%.0f').classes('w-full mb-4')
        with ui.row().classes('w-full mb-4 justify-between'):
            upper_cb = ui.checkbox('Uppercase (A-Z)', value=True)
            lower_cb = ui.checkbox('Lowercase (a-z)', value=True)
        with ui.row().classes('w-full mb-4 justify-between'):
            num_cb = ui.checkbox('Numbers (0-9)', value=True)
            sym_cb = ui.checkbox('Symbols (!@#)', value=True)
            
        result_label = ui.label('').classes('text-xl font-mono bg-gray-200 p-2 rounded w-full text-center mt-4 hidden')
        
        save_container = ui.column().classes('w-full mt-4 hidden')
        with save_container:
            ui.label('Save this password?').classes('text-lg font-semibold')
            master_input = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full')
            username_input = ui.input('Username / Email').classes('w-full')
            platform_input = ui.input('Platform / Website').classes('w-full')
            
            def on_save():
                master = master_input.value
                username = username_input.value
                platform = platform_input.value
                pwd = result_label.text
                
                if not datastore.check_master_password(master):
                    ui.notify('Wrong master password!', type='negative')
                    return
                if not username or not platform:
                    ui.notify('Username and platform required', type='warning')
                    return
                    
                saved_id = datastore.save_password(username, platform, pwd, master)
                if saved_id:
                    ui.notify(f'Password saved! ID: {saved_id}', type='positive')
                    save_container.classes(add='hidden')
                    result_label.classes(add='hidden')
                    username_input.value = ''
                    platform_input.value = ''
                    master_input.value = ''
                else:
                    ui.notify('Save failed. Duplicate entry?', type='negative')

            ui.button('Save Password', on_click=on_save).classes('w-full mt-2')

        def on_generate():
            length = int(length_input.value or 0)
            pwd = generate_pwd(length, upper_cb.value, lower_cb.value, num_cb.value, sym_cb.value)
            if pwd:
                result_label.text = pwd
                result_label.classes(remove='hidden')
                save_container.classes(remove='hidden')
                ui.notify('Password generated!', type='positive')
            else:
                ui.notify('Invalid length', type='negative')
                
        ui.button('Generate', on_click=on_generate).classes('w-full text-white rounded-lg py-2')
