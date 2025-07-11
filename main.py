# main.py
import flet as ft

from src.application.use_cases import PedidoUseCases
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
    page.title = "Pastelería Pepe - KioscoPP"

    db_path = r"/Users/omar/Github/KioscoFlet/config.db"
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

    pedido_use_cases = PedidoUseCases(
        pedido_repo, tamano_repo, categoria_repo,
        tipo_pan_repo, tipo_forma_repo, tipo_relleno_repo,
        tipo_cobertura_repo, finalizar_repo, imagen_galeria_repo,
        tipo_color_repo
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(views.vista_bienvenida(page))
        elif page.route == "/fecha":
            page.views.append(views.vista_fecha(page, pedido_use_cases))
        elif page.route == "/tamano":
            page.views.append(views.vista_tamano(page, pedido_use_cases))
        elif page.route == "/categorias":
            page.views.append(views.vista_categorias(page, pedido_use_cases))
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
            page.views.append(views.vista_confirmacion(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)