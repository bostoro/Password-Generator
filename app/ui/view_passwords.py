from nicegui import ui
from .save_password import render_save_password
from .password_input import render_password_input


ui.add_head_html('''
<style>

.password-scroll {
    width: 100%;
    overflow-x: auto;
    white-space: nowrap;
    display: block;
}

.actions-cell {
    position: sticky;
    right: 0;
    background: white;
    z-index: 2;
}
</style>
''', shared=True)


def render_view_passwords(service):
    with ui.card().classes('w-full mx-auto mt-8 p-6 shadow-lg rounded-xl'):
        ui.label('Passwords').classes(
            'text-2xl font-bold mb-4 text-primary')

        with ui.dialog() as save_dialog, ui.card().classes('w-full max-w-md'):
            render_save_password(service, on_cancel=lambda: save_dialog.close())

        with ui.row().classes('w-full items-center gap-2 mb-4'):
            ui.button('+', on_click=lambda: save_dialog.open()
                    ).classes('text-xl font-bold ml-auto')

        table_container = ui.column().classes('w-full hidden')

        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True,
                'classes': 'hidden', 'headerClasses': 'hidden'},
            {'name': 'username', 'label': 'Username', 'field': 'username',
                'sortable': True, 'align': 'left', 'style': 'width: 15%'},
            {'name': 'platform', 'label': 'Platform', 'field': 'platform',
                'sortable': True, 'align': 'left', 'style': 'width: 15%'},
            {'name': 'password', 'label': 'Password', 'field': 'password',
                'align': 'left', 'style': 'width: 40%; max-width: 0; overflow: hidden'},
            {'name': 'date', 'label': 'Date', 'field': 'date',
                'sortable': True, 'align': 'left', 'style': 'width: 8%'},
            {'name': 'actions', 'label': '',
                'field': 'actions', 'style': 'width: 8%'},
        ]

        with table_container:
            table = ui.table(columns=columns, rows=[], row_key='id').classes(
                'w-full').props('separator=cell')

            def on_delete(e):
                success = service.delete(e.args['id'])
                if success:
                    ui.notify('Password deleted!', type='positive')
                    table.rows[:] = [r for r in table.rows if r['id'] != e.args['id']]
                    table.update()

            table.add_slot('body-cell-actions', '''
    <q-td :props="props" class="actions-cell">
        <q-btn flat round
            :icon="props.row.password !== '********' ? 'visibility_off' : 'visibility'"
            color="grey"
            @click="$parent.$emit('reveal', props.row)" />
        <q-btn flat round icon="edit" color="primary"
            @click="$parent.$emit('edit', props.row)" />
        <q-btn flat round icon="delete" color="red"
            @click="$parent.$emit('delete', props.row)" />
    </q-td>
''')
            
            table.add_slot('body-cell-password', '''
    <q-td :props="props">
        <div style="display: flex; align-items: center; width: 100%;">
            <span class="password-scroll" style="flex: 1; min-width: 0;">{{ props.row.password }}</span>
            <q-btn v-if="props.row.password !== '********'" flat round dense icon="content_copy" color="grey" size="sm"
                @click="$parent.$emit('copy', props.row)" />
        </div>
    </q-td>
''')

            table.on('delete', on_delete)

            with ui.dialog() as edit_dialog, ui.card().classes('w-full max-w-md'):
                edit_label = ui.label('').classes('text-lg font-semibold mb-4')
                edit_username = ui.input('Username').classes('w-full mb-2')
                edit_platform = ui.input('Platform').classes('w-full mb-2')
                edit_password = ui.input(
                    'Password', password=True, password_toggle_button=True).classes('w-full mb-2')
                render_password_input(service, edit_password)
                    
                pending_edit = {'id': None}

                def on_edit_cancel():
                    edit_dialog.close()

                def on_confirm_edit():
                    success = service.update_password(
                        pending_edit['id'],
                        edit_username.value,
                        edit_platform.value,
                        edit_password.value,
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
                        ui.notify('Update failed. Duplicate entry?', type='negative')

                with ui.row():
                    ui.button('Cancel', on_click=on_edit_cancel)
                    ui.button('Save', color='primary',
                              on_click=on_confirm_edit)


            def on_reveal(e):
                for row in table.rows:
                    if row['id'] == e.args['id']:
                        if row['password'] != '********':
                            row['password'] = '********'
                            table.update()
                            return
                        pwd = service.get_password(e.args['id'])
                        if pwd:
                            row['password'] = pwd
                            table.update()
                        return

            table.on('reveal', on_reveal)

            def on_copy(e):
                ui.clipboard.write(e.args['password'])
                ui.notify('Copied!', type='positive')

            table.on('copy', on_copy)

            def on_edit(e):
                pending_edit['id'] = e.args['id']
                edit_label.text = f"Edit entry for '{e.args['username']}' on '{e.args['platform']}'"
                edit_username.value = e.args['username']
                edit_platform.value = e.args['platform']
                edit_password.value = ''
                edit_dialog.open()

            table.on('edit', on_edit)

            passwords = service.get_all(show_real=False)

            rows = []
            for pwd in passwords:
                rows.append({
                    'id': pwd[0],
                    'username': pwd[1],
                    'platform': pwd[2],
                    'password': pwd[3],
                    'date': pwd[4].strftime('%d %b %Y  %H:%M') if pwd[4] else ''
                })

            table.rows[:] = rows
            table.update()
            table_container.classes(remove='hidden')
