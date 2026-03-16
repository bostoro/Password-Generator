from nicegui import ui
from nicegui import app

def render_exit_app():
    with ui.card().classes('w-full max-w-md mx-auto mt-8 p-6 shadow-lg rounded-xl text-center'):
        ui.label('Exit Application').classes('text-2xl font-bold mb-4 text-primary')
        ui.label('Are you sure you want to stop the server?').classes('text-lg mb-6')
        
        def on_exit():
            ui.notify('Shutting down server...', type='info')
            app.shutdown()
            
        ui.button('Yes, shut down', on_click=on_exit, color='red').classes('w-full')
