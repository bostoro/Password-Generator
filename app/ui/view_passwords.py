from nicegui import ui
from services.password_service import PasswordService
from .save_password import render_save_password

service = PasswordService()

def render_view_passwords():
    with ui.card().classes('w-full mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('View Passwords').classes('text-2xl font-bold mb-4 text-primary')
        
        with ui.row().classes('w-full items-center gap-2 mb-4'):
            master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full max-w-md')
            with ui.dialog() as save_dialog, ui.card().classes('w-full max-w-md'):
                render_save_password()
            ui.button('+', on_click=lambda: save_dialog.open()).classes('text-xl font-bold ml-auto')
        
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

            with ui.dialog() as confirm_dialog, ui.card():
                confirm_label = ui.label('').classes('text-lg font-semibold mb-4')
                master_confirm = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
                error_label = ui.label('').classes('text-red-500 hidden')
                
                pending_row = {'id': None}
                
                def on_cancel():
                    confirm_dialog.close()
                    master_confirm.value = ''
                    error_label.classes(add='hidden')

                def on_confirm_delete():
                    if not service.check_master(master_confirm.value):
                        error_label.text = 'Wrong master password!'
                        error_label.classes(remove='hidden')
                        return
                    success = service.delete(pending_row['id'])
                    if success:
                        ui.notify('Password deleted!', type='positive')
                        table.rows[:] = [r for r in table.rows if r['id'] != pending_row['id']]
                        table.update()
                    confirm_dialog.close()
                    master_confirm.value = ''
                    error_label.classes(add='hidden')

                with ui.row():
                    ui.button('Cancel', on_click=on_cancel)
                    ui.button('Delete', color='red', on_click=on_confirm_delete)

            def on_delete(e):
                pending_row['id'] = e.args['id']
                confirm_label.text = f"Delete entry for '{e.args['username']}' on '{e.args['platform']}'?"
                master_confirm.value = ''
                error_label.classes(add='hidden')
                confirm_dialog.open()

            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn flat round icon="edit" color="primary"
                        @click="$parent.$emit('edit', props.row)" />
                    <q-btn flat round icon="delete" color="red"
                        @click="$parent.$emit('delete', props.row)" />
                </q-td>
            ''')
            table.on('delete', on_delete)

            with ui.dialog() as edit_dialog, ui.card():
                edit_label = ui.label('').classes('text-lg font-semibold mb-4')
                edit_username = ui.input('Username').classes('w-full mb-2')
                edit_platform = ui.input('Platform').classes('w-full mb-2')
                edit_password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-2')
                edit_master = ui.input('Master Password', password=True, password_toggle_button=True).classes('w-full mb-4')
                edit_error = ui.label('').classes('text-red-500 hidden')

                pending_edit = {'id': None}

                def on_edit_cancel():
                    edit_dialog.close()
                    edit_master.value = ''
                    edit_error.classes(add='hidden')

                def on_confirm_edit():
                    if not service.check_master(edit_master.value):
                        edit_error.text = 'Wrong master password!'
                        edit_error.classes(remove='hidden')
                        return
                    success = service.update_password(
                        pending_edit['id'],
                        edit_username.value,
                        edit_platform.value,
                        edit_password.value,
                        edit_master.value
                    )
                    if success:
                        ui.notify('Password updated!', type='positive')
                        for row in table.rows:
                            if row['id'] == pending_edit['id']:
                                row['username'] = edit_username.value
                                row['platform'] = edit_platform.value
                                row['password'] = '********'
                        table.update()
                    else:
                        edit_error.text = 'Update failed. Duplicate entry?'
                        edit_error.classes(remove='hidden')
                        return
                    edit_dialog.close()
                    edit_master.value = ''
                    edit_error.classes(add='hidden')

                with ui.row():
                    ui.button('Cancel', on_click=on_edit_cancel)
                    ui.button('Save', color='primary', on_click=on_confirm_edit)

            def on_edit(e):
                pending_edit['id'] = e.args['id']
                edit_label.text = f"Edit entry for '{e.args['username']}' on '{e.args['platform']}'"
                edit_username.value = e.args['username']
                edit_platform.value = e.args['platform']
                edit_password.value = ''
                edit_master.value = ''
                edit_error.classes(add='hidden')
                edit_dialog.open()

            table.on('edit', on_edit)
        
        def on_view():
            m = master.value
            if not m:
                ui.notify('Master password required to view actual passwords!', type='warning')
                show_real = False
            elif service.check_master(m):
                show_real = True
                ui.notify('Master password correct!', type='positive')
                master.value = ''
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
            
        master.on('keydown.enter', lambda: on_view())
        ui.button('Load Passwords', on_click=on_view).classes('mt-2')