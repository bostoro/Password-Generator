from nicegui import ui

def render_password_input(service, target_input):
    with ui.dialog() as generate_dialog, ui.card():
        ui.label('Generate Password').classes('text-lg font-bold mb-2')
        length_input = ui.number('Length', value=16, min=1, format='%.0f').classes('w-full mb-2')
        with ui.expansion('Advanced options').classes('w-full mb-2'):
            upper_cb = ui.checkbox('Uppercase (A-Z)', value=True)
            lower_cb = ui.checkbox('Lowercase (a-z)', value=True)
            num_cb = ui.checkbox('Numbers (0-9)', value=True)
            sym_cb = ui.checkbox('Symbols (!@#)', value=True)
        def on_generate():
            pwd = service.generate(
                int(length_input.value or 16),
                upper_cb.value, lower_cb.value,
                num_cb.value, sym_cb.value
            )
            if pwd:
                target_input.value = pwd
                generate_dialog.close()
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
        pwd = target_input.value
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

    target_input.on('keyup', lambda: on_password_change())