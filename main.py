# main.py
import flet as ft

from src.application.use_cases import PedidoUseCases, AuthUseCases, FinalizarPedidoUseCases
from src.infrastructure.persistence.memory_repository import PedidoRepositoryEnMemoria
from src.infrastructure.persistence.sqlite_repository import (
    TamanoRepositorySQLite, CategoriaRepositorySQLite,
    TipoPanRepositorySQLite, TipoFormaRepositorySQLite,
    TipoRellenoRepositorySQLite, TipoCoberturaRepositorySQLite,
    FinalizarPedidoRepositorySQLite, ImagenGaleriaRepositorySQLite,
    TipoColorRepositorySQLite, HorarioEntregaRepositorySQLite, DiaFestivoRepositorySQLite
)
from src.infrastructure.flet_adapter import views
from src.infrastructure.persistence.api_repository import FinalizarPedidoRepositoryAPI
from src.infrastructure.persistence.composite_repository import FinalizarPedidoRepositoryComposite
from src.infrastructure.flet_adapter.controles_comunes import crear_boton_navegacion


def main(page: ft.Page):
    page.title = "Pastelería Pepe"

    page.window.width = 1920
    page.window.height = 1080
    page.window.resizable = True
    #page.window.full_screen = True

    page.padding = 0

    page.fonts = {
        "Bebas Neue": "fuentes/BebasNeue-Regular.ttf",
        "Be Vietnam Pro": "fuentes/BeVietnamPro-Regular.ttf",
        "Montserrat Alternates": "fuentes/Montserrat-Alternates-Regular.ttf",
    }

    db_path = r"C:/KioscoPP/config.db"
    pedido_repo = PedidoRepositoryEnMemoria()
    tamano_repo = TamanoRepositorySQLite(db_path)
    categoria_repo = CategoriaRepositorySQLite(db_path)
    tipo_pan_repo = TipoPanRepositorySQLite(db_path)
    tipo_forma_repo = TipoFormaRepositorySQLite(db_path)
    tipo_relleno_repo = TipoRellenoRepositorySQLite(db_path)
    tipo_cobertura_repo = TipoCoberturaRepositorySQLite(db_path)
    imagen_galeria_repo = ImagenGaleriaRepositorySQLite(db_path)
    tipo_color_repo = TipoColorRepositorySQLite(db_path)
    horario_repo = HorarioEntregaRepositorySQLite(db_path)
    dia_festivo_repo = DiaFestivoRepositorySQLite(db_path)

    API_URL_PEDIDOS = "https://pepesquioscodev-dze4d8gwgfcpgwaw.mexicocentral-01.azurewebsites.net/pedidos"  # <-- CAMBIA ESTO

    finalizar_repo_api = FinalizarPedidoRepositoryAPI(api_url=API_URL_PEDIDOS, db_path=db_path)
    finalizar_pedido_repo = FinalizarPedidoRepositorySQLite(db_path)

    auth_use_cases = AuthUseCases()
    pedido_use_cases = PedidoUseCases(
        pedido_repo, tamano_repo, categoria_repo,
        tipo_pan_repo, tipo_forma_repo, tipo_relleno_repo,
        tipo_cobertura_repo, finalizar_pedido_repo, imagen_galeria_repo,
        tipo_color_repo, horario_repo, dia_festivo_repo
    )

    finalizar_repo_compuesto = FinalizarPedidoRepositoryComposite(
        sqlite_repo=finalizar_pedido_repo,
        api_repo=finalizar_repo_api
    )

    finalizar_pedido_use_cases = FinalizarPedidoUseCases(
        pedido_repo=pedido_repo,
        finalizar_repo=finalizar_repo_compuesto,
        categoria_repo=categoria_repo,
    )

    def cerrar_resumen(e):
        bs.open = False
        page.update()

    def restablecer_pedido(e):
        pedido_use_cases.iniciar_nuevo_pedido()
        cerrar_resumen(e)
        page.go("/")

    def crear_fila_resumen(icono, titulo, valor):
        return ft.Row(
            spacing=15,
            controls=[
                ft.Image(src=f"iconos/{icono}", width=50, height=50),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(titulo, size=12, color=ft.Colors.GREY_600),
                        ft.Text(valor or "No seleccionado", size=16, weight=ft.FontWeight.BOLD),
                    ]
                )
            ]
        )

    boton_restablecer_estilizado = crear_boton_navegacion(
        texto="Restablecer Pedido",
        on_click_handler=restablecer_pedido,
        es_primario=True
    )
    boton_restablecer_estilizado.width = page.width

    bs = ft.BottomSheet(
        content=ft.Container(padding=20),
        on_dismiss=cerrar_resumen,
    )

    def abrir_resumen(e):
        pedido = pedido_use_cases.obtener_pedido_actual()

        categorias = {c.id: c.nombre for c in pedido_use_cases.obtener_categorias()}
        nombre_categoria = categorias.get(pedido.id_categoria, "N/A")

        bs.content.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[ft.IconButton(icon=ft.Icons.CLOSE, on_click=cerrar_resumen)]
                ),
                ft.Row(
                    controls=[
                        ft.Column([
                            crear_fila_resumen("categoria.png", "Categoría", nombre_categoria),
                            crear_fila_resumen("forma.png", "Forma", pedido.tipo_forma),
                            crear_fila_resumen("relleno.png", "Relleno", pedido.tipo_relleno),
                        ], expand=1),
                        ft.Column([
                            crear_fila_resumen("tamano2.png", "Tamaño (Personas)", pedido.tamano_pastel),
                            crear_fila_resumen("pan.png", "Pan", pedido.tipo_pan),
                            crear_fila_resumen("cobertura.png", "Cobertura", pedido.tipo_cobertura),
                        ], expand=1),
                    ]
                ),
                ft.Divider(height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        crear_fila_resumen("fecha.png", "Fecha de Entrega", pedido.fecha_entrega.strftime(
                            '%d/%m/%Y') if pedido.fecha_entrega else "N/A"),
                        crear_fila_resumen("hora.png", "Hora de Entrega", pedido.hora_entrega),
                    ]
                ),
                ft.Container(height=20),
                boton_restablecer_estilizado
            ]
        )
        bs.open = True
        page.update()

    page.open_summary = abrir_resumen
    page.overlay.append(bs)

    def route_change(route):
        print(f"Cambiando a la ruta: {page.route}")
        page.views.clear()
        funcion_animacion = None

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
        elif page.route == "/forma":
            page.views.append(views.vista_forma(page, pedido_use_cases))
        elif page.route == "/pan":
            page.views.append(views.vista_pan(page, pedido_use_cases))
        elif page.route == "/relleno":
            page.views.append(views.vista_relleno(page, pedido_use_cases))
        elif page.route == "/cobertura":
            page.views.append(views.vista_cobertura(page, pedido_use_cases))
        elif page.route == "/decorado":
            page.views.append(views.vista_decorado(page, pedido_use_cases))
        elif page.route == "/galeria":
            page.views.append(views.vista_galeria(page, pedido_use_cases))
        elif page.route == "/extras":
            page.views.append(views.vista_extras(page, pedido_use_cases))
        elif page.route == "/datos_cliente":
            page.views.append(views.vista_datos_cliente(page, pedido_use_cases, finalizar_pedido_use_cases))
        elif page.route == "/confirmacion":
            vista, funcion_animacion = views.vista_confirmacion(page, finalizar_pedido_use_cases, pedido_use_cases)
            page.views.append(vista)
        page.update()

        if funcion_animacion:
            funcion_animacion()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.window.destroy()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")



