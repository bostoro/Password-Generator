from nicegui import ui
import datastore as datastore

def render_view_passwords():
    with ui.card().classes('w-full mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('📋 View Passwords').classes('text-2xl font-bold mb-4 text-primary')
        
        master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full max-w-md mb-4')
        
        table_container = ui.column().classes('w-full hidden')
        
        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
            {'name': 'username', 'label': 'Username', 'field': 'username', 'sortable': True},
            {'name': 'platform', 'label': 'Platform', 'field': 'platform', 'sortable': True},
            {'name': 'password', 'label': 'Password', 'field': 'password'},
            {'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True},
        ]
        
        with table_container:
            table = ui.table(columns=columns, rows=[], row_key='id').classes('w-full')
        
        def on_view():
            m = master.value
            if not m:
                ui.notify('Master password required to view actual passwords!', type='warning')
                show_real = False
            elif datastore.check_master_password(m):
                show_real = True
                ui.notify('Master password correct!', type='positive')
            else:
                show_real = False
                ui.notify('Wrong master password! Showing masked.', type='negative')
                
            passwords = datastore.get_all_passwords(m if show_real else "", show_real)
            
            rows = []
            for pwd in passwords:
                rows.append({
                    'id': pwd[0],
                    'username': pwd[1],
                    'platform': pwd[2],
                    'password': pwd[3],
                    'date': pwd[4]
                })
            
            table.rows[:] = rows
            table.update()
            table_container.classes(remove='hidden')
            
        ui.button('Load Passwords', on_click=on_view).classes('mt-2')
