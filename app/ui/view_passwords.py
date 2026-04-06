from nicegui import ui
from services.password_service import PasswordService

service = PasswordService()

def render_view_passwords():
    with ui.card().classes('w-full mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('View Passwords').classes('text-2xl font-bold mb-4 text-primary')
        
        master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full max-w-md mb-4')
        
        table_container = ui.column().classes('w-full hidden')
        
        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
            {'name': 'username', 'label': 'Username', 'field': 'username', 'sortable': True},
            {'name': 'platform', 'label': 'Platform', 'field': 'platform', 'sortable': True},
            {'name': 'password', 'label': 'Password', 'field': 'password'},
            {'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True},
            {'name': 'actions', 'label': '', 'field': 'actions'},
        ]
        
        with table_container:
            table = ui.table(columns=columns, rows=[], row_key='id').classes('w-full')

            def on_delete(e):
                pwd_id = e.args['id']
                success = service.delete(pwd_id)
                if success:
                    ui.notify(f'Password {pwd_id} deleted!', type='positive')
                    table.rows[:] = [r for r in table.rows if r['id'] != pwd_id]
                    table.update()
                else:
                    ui.notify(f'Could not delete password {pwd_id}', type='negative')

            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn flat round icon="delete" color="red"
                        @click="$parent.$emit('delete', props.row)" />
                </q-td>
            ''')
            table.on('delete', on_delete)
        
        def on_view():
            m = master.value
            if not m:
                ui.notify('Master password required to view actual passwords!', type='warning')
                show_real = False
            elif service.check_master(m):
                show_real = True
                ui.notify('Master password correct!', type='positive')
            else:
                show_real = False
                ui.notify('Wrong master password! Showing masked.', type='negative')
                
            passwords = service.get_all(m if show_real else "", show_real)
            
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
