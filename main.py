# main.py
import flet as ft

from src.application.use_cases import PedidoUseCases, AuthUseCases
from src.infrastructure.persistence.memory_repository import PedidoRepositoryEnMemoria
from src.infrastructure.persistence.sqlite_repository import (
    TamanoRepositorySQLite, CategoriaRepositorySQLite,
    TipoPanRepositorySQLite, TipoFormaRepositorySQLite,
    TipoRellenoRepositorySQLite, TipoCoberturaRepositorySQLite,
    FinalizarPedidoRepositorySQLite, ImagenGaleriaRepositorySQLite,
    TipoColorRepositorySQLite
)
from src.infrastructure.flet_adapter import views


def main(page: ft.Page):
    page.title = "Pastelería Pepe"

    page.window.width = 900
    page.window.height = 1024
    page.padding = 0
    #page.window.resizable = False

    page.fonts = {
        "Bebas Neue": "fuentes/BebasNeue-Regular.ttf",
        "Be Vietnam Pro": "fuentes/BeVietnamPro-Regular.ttf"
    }

    db_path = r"C:/KioscoPP/config.db"
    pedido_repo = PedidoRepositoryEnMemoria()
    tamano_repo = TamanoRepositorySQLite(db_path)
    categoria_repo = CategoriaRepositorySQLite(db_path)
    tipo_pan_repo = TipoPanRepositorySQLite(db_path)
    tipo_forma_repo = TipoFormaRepositorySQLite(db_path)
    tipo_relleno_repo = TipoRellenoRepositorySQLite(db_path)
    tipo_cobertura_repo = TipoCoberturaRepositorySQLite(db_path)
    finalizar_repo = FinalizarPedidoRepositorySQLite(db_path)
    imagen_galeria_repo = ImagenGaleriaRepositorySQLite(db_path)
    tipo_color_repo = TipoColorRepositorySQLite(db_path)

    auth_use_cases = AuthUseCases()
    pedido_use_cases = PedidoUseCases(
        pedido_repo, tamano_repo, categoria_repo,
        tipo_pan_repo, tipo_forma_repo, tipo_relleno_repo,
        tipo_cobertura_repo, finalizar_repo, imagen_galeria_repo,
        tipo_color_repo
    )

    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE, size=24, font_family="Bebas Neue"
        )
    )
    # El "marco de teléfono" donde se mostrará el contenido de cada vista.
    marco_contenido = ft.Container(
        expand=True,
        # Usamos un gradiente sutil para el fondo del marco
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.WHITE, ft.Colors.GREY_200]
        ),
        border_radius=30,
        padding=20,
    )

    layout_centrado = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=30,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                banner_superior,
                ft.Container(
                    width=414, # Ancho típico de un teléfono (iPhone 11 Pro Max)
                    height=736, # Altura típica
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)),
                    border_radius=30,
                    content=marco_contenido
                )
            ]
        )
    )


    def route_change(route):
        print(f"Cambiando a la ruta: {page.route}")
        page.views.clear()

        if page.route == "/login":
            page.views.append(views.vista_login(page, auth_use_cases))
        elif page.route == "/":
            page.views.append(views.vista_bienvenida(page))
        elif page.route == "/seleccion":
            page.views.append(views.vista_seleccion(page))
        elif page.route == "/fecha":
            page.views.append(views.vista_fecha(page, pedido_use_cases))
        elif page.route == "/tamano":
            page.views.append(views.vista_tamano(page, pedido_use_cases))
        elif page.route == "/categorias":
            page.views.append(views.vista_categorias(page, pedido_use_cases))
        elif page.route == "/relleno":
            page.views.append(views.vista_relleno(page, pedido_use_cases))
        elif page.route == "/resumen":
            page.views.append(views.vista_resumen(page, pedido_use_cases))
        elif page.route == "/datos_cliente":
            page.views.append(views.vista_datos_cliente(page, pedido_use_cases))
        elif page.route == "/decorado":
            page.views.append(views.vista_decorado(page, pedido_use_cases))
        elif page.route == "/galeria":  # Nueva ruta
            page.views.append(views.vista_galeria(page, pedido_use_cases))
        elif page.route == "/extras":  # Nueva ruta
            page.views.append(views.vista_extras(page, pedido_use_cases))
        elif page.route == "/confirmacion":
            page.views.append(views.vista_confirmacion(page, pedido_use_cases))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.add(
        ft.Stack(
            [
                ft.Image(src="fondos/fondo1.png", fit=ft.ImageFit.COVER, expand=True),
                layout_centrado
            ]
        )
    )

    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
