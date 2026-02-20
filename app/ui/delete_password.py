from nicegui import ui
import datastore as datastore

def render_delete_password():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('🗑️ Delete Password').classes('text-2xl font-bold mb-4 text-primary')
        
        pwd_id_input = ui.number('Password ID to delete', format='%.0f').classes('w-full mb-4')
        
        def on_delete():
            pwd_id = pwd_id_input.value
            if pwd_id is None:
                ui.notify('Please provide an ID', type='warning')
                return
            
            success = datastore.delete_password(int(pwd_id))
            if success:
                ui.notify(f'Password {int(pwd_id)} deleted successfully!', type='positive')
                pwd_id_input.value = None
            else:
                ui.notify(f'No password found with ID {int(pwd_id)}', type='negative')
                
        ui.button('Delete', on_click=on_delete, color='red').classes('w-full')
