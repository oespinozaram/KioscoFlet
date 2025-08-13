# src/infrastructure/flet_adapter/controles_comunes.py
import flet as ft

def crear_boton_navegacion(texto: str, on_click_handler, es_primario: bool = True, **kwargs):
    """
    Crea un botón de navegación estilizado.
    Acepta argumentos adicionales (kwargs) como ref, disabled, etc.
    """
    return ft.Container(
        width=150,
        height=45,
        bgcolor="#E5ADAD" if es_primario else ft.Colors.BLUE_GREY_300,
        border_radius=ft.border_radius.all(10),
        content=ft.Text(
            texto,
            color=ft.Colors.WHITE,
            size=20,
            font_family="Bebas Neue"
        ),
        alignment=ft.alignment.center,
        on_click=on_click_handler,
        **kwargs  # <-- Se pasan los argumentos extra aquí
    )