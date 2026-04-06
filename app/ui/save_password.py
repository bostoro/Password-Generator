from nicegui import ui
from services.password_service import PasswordService

service = PasswordService()

def render_save_password():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Save a Password').classes('text-2xl font-bold mb-4 text-primary')
        
        username = ui.input('Username or Email').classes('w-full mb-2')
        platform = ui.input('Website / Platform').classes('w-full mb-2')
        with ui.row().classes('w-full items-center gap-2 mb-2'):
            password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full')
        with ui.dialog() as generate_dialog, ui.card():
            ui.label('Generate Password').classes('text-lg font-bold mb-2')
            length_input = ui.number('Length', value=16, format='%.0f').classes('w-full mb-2')
            
            with ui.expansion('Advanced options').classes('w-full mb-2'):
                upper_cb = ui.checkbox('Uppercase (A-Z)', value=True)
                lower_cb = ui.checkbox('Lowercase (a-z)', value=True)
                num_cb = ui.checkbox('Numbers (0-9)', value=True)
                sym_cb = ui.checkbox('Symbols (!@#)', value=True)

            def on_generate():
                import string, random
                length = int(length_input.value or 16)
                pwd = service.generate(
                    length,
                    upper_cb.value,
                    lower_cb.value,
                    num_cb.value,
                    sym_cb.value
                )
                if pwd:
                    password.value = pwd
                    on_password_change()
                    generate_dialog.close()
                else:
                    ui.notify('Invalid length', type='negative')

            ui.button('Generate', on_click=on_generate).classes('w-full mt-2')

        with ui.row().classes('items-center gap-1 mb-2 w-full justify-between'):
            with ui.dialog() as info_dialog, ui.card():
                ui.label('Password Strength Guide').classes('text-lg font-bold mb-2')
                ui.label('❌ Weak: <6 characters, or missing uppercase, lowercase, or numbers or symbols')
                ui.label('✅ Medium: >=6 characters with uppercase, lowercase and numbers and symbols')
                ui.label('🔐 Strong: >=12 characters with uppercase, lowercase, numbers and symbols')
                ui.button('Close', on_click=info_dialog.close).classes('mt-4')
            with ui.row().classes('items-center gap-0'):
                ui.icon('info').classes('text-gray-400 cursor-pointer text-sm').on('click', lambda: info_dialog.open())
                strength_label = ui.label('').classes('text-sm font-semibold')
            ui.button('Generate', on_click=lambda: generate_dialog.open()).classes('shrink-0')

        def on_password_change():
            pwd = password.value
            if not pwd:
                strength_label.text = ''
                return
            strength = service.check_strength(pwd)
            if strength == 'weak':
                strength_label.text = '❌ Weak'
                strength_label.style('color: #EF4444;')
            elif strength == 'strong':
                strength_label.text = '🔐 Strong'
                strength_label.style('color: #10B981;')
            else:
                strength_label.text = '✅ Medium'
                strength_label.style('color: #F59E0B;')

        password.on('keyup', lambda: on_password_change())

        master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
        
        def on_save():
            u = username.value
            p_form = platform.value
            pwd = password.value
            m = master.value
            
            if not u or not p_form or not pwd or not m:
                ui.notify('All fields are required!', type='warning')
                return
            
            if not service.check_master(m):
                ui.notify('Wrong master password!', type='negative')
                master.value = ''
                return
                
            saved_id = service.save(u, p_form, pwd, m)
            if saved_id:
                ui.notify(f'Password saved with ID: {saved_id}', type='positive')
                username.value = ''
                platform.value = ''
                password.value = ''
                master.value = ''
            else:
                ui.notify('Duplicate entry!', type='negative')
                
        ui.button('Save', on_click=on_save).classes('w-full mt-2')
