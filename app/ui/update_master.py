from nicegui import ui
import datastore as datastore

def render_update_master():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('🔑 Update Master Password').classes('text-2xl font-bold mb-4 text-primary')
        
        old_master = ui.input('Old Master Password', password=True, password_toggle_button=True).classes('w-full mb-2')
        new_master = ui.input('New Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
        
        def on_update():
            old = old_master.value
            new = new_master.value
            if not old or not new:
                ui.notify('Both fields required', type='warning')
                return
            
            if datastore.update_master_password(old, new):
                ui.notify('Master password updated successfully!', type='positive')
                old_master.value = ''
                new_master.value = ''
            else:
                ui.notify('Failed to update. Wrong old password?', type='negative')
                
        ui.button('Update Password', on_click=on_update).classes('w-full')
