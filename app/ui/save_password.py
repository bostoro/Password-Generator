from nicegui import ui
from services.password_service import PasswordService

service = PasswordService()

def render_save_password():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Save a Password').classes('text-2xl font-bold mb-4 text-primary')
        
        username = ui.input('Username or Email').classes('w-full mb-2')
        platform = ui.input('Website / Platform').classes('w-full mb-2')
        password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-2')
        with ui.row().classes('items-center gap-2 mb-2'):
            strength_label = ui.label('').classes('text-sm font-semibold')
            with ui.dialog() as info_dialog, ui.card():
                ui.label('Password Strength Guide').classes('text-lg font-bold mb-2')
                ui.label('❌ Weak: <6 chars, or missing uppercase, lowercase, or numbers')
                ui.label('✅ Medium: 6+ chars with uppercase, lowercase and numbers')
                ui.label('🔐 Strong: 12+ chars with uppercase, lowercase, numbers and symbols')
                ui.button('Close', on_click=info_dialog.close).classes('mt-4')
            ui.icon('info').classes('text-gray-400 cursor-pointer').on('click', lambda: info_dialog.open())

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
                
        ui.button('Save Manually', on_click=on_save).classes('w-full mt-2')
