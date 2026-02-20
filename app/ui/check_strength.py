from nicegui import ui
import utils.password_utils as password_utils

def render_check_strength():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('💪 Check Strength').classes('text-2xl font-bold mb-4 text-primary')
        
        pwd_input = ui.input('Type password to check').classes('w-full mb-4')
        result_label = ui.label('').classes('text-lg font-semibold mt-2 hidden')
        
        def on_check():
            pwd = pwd_input.value
            if not pwd:
                ui.notify('Enter a password', type='warning')
                return
                
            strength = password_utils.get_password_strength(pwd)
            result_label.classes(remove='hidden')
            
            if strength == 'weak':
                result_label.text = '❌ Weak Password'
                result_label.style('color: #EF4444;')
            elif strength == 'strong':
                result_label.text = '🔐 Strong Password!!'
                result_label.style('color: #10B981;')
            else:
                result_label.text = '✅ Fine (could be stronger)'
                result_label.style('color: #F59E0B;')
                
        ui.button('Check Strength', on_click=on_check).classes('w-full')
