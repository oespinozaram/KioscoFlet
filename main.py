# main.py
import flet as ft

from src.application.use_cases import PedidoUseCases, AuthUseCases, FinalizarPedidoUseCases
from src.infrastructure.persistence.memory_repository import PedidoRepositoryEnMemoria
from src.infrastructure.persistence.sqlite_repository import (
    TamanoRepositorySQLite, CategoriaRepositorySQLite,
    TipoPanRepositorySQLite, TipoFormaRepositorySQLite,
    TipoRellenoRepositorySQLite, TipoCoberturaRepositorySQLite,
    FinalizarPedidoRepositorySQLite, ImagenGaleriaRepositorySQLite,
    TipoColorRepositorySQLite
)
from src.infrastructure.flet_adapter import views
from src.infrastructure.persistence.api_repository import FinalizarPedidoRepositoryAPI
from src.infrastructure.persistence.composite_repository import FinalizarPedidoRepositoryComposite


def main(page: ft.Page):
    page.title = "Pastelería Pepe"

    page.window.width = 900
    page.window.height = 1024
    page.padding = 0
    #page.window.resizable = False

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
    finalizar_repo = FinalizarPedidoRepositorySQLite(db_path)
    imagen_galeria_repo = ImagenGaleriaRepositorySQLite(db_path)
    tipo_color_repo = TipoColorRepositorySQLite(db_path)

    API_URL_PEDIDOS = "https://pepesquioscodev-dze4d8gwgfcpgwaw.mexicocentral-01.azurewebsites.net/pedidos"  # <-- CAMBIA ESTO

    # --- ANTES ---
    # finalizar_repo = FinalizarPedidoRepositorySQLite(db_path)

    # --- AHORA ---
    finalizar_repo_api = FinalizarPedidoRepositoryAPI(api_url=API_URL_PEDIDOS, db_path=db_path)

    auth_use_cases = AuthUseCases()
    pedido_use_cases = PedidoUseCases(
        pedido_repo, tamano_repo, categoria_repo,
        tipo_pan_repo, tipo_forma_repo, tipo_relleno_repo,
        tipo_cobertura_repo, finalizar_repo, imagen_galeria_repo,
        tipo_color_repo
    )

    finalizar_pedido_repo = FinalizarPedidoRepositorySQLite(db_path)

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
        """Cierra el BottomSheet."""
        bs.open = False
        page.update()

    def restablecer_pedido(e):
        """Llama al caso de uso para reiniciar el pedido y cierra el resumen."""
        pedido_use_cases.iniciar_nuevo_pedido()
        cerrar_resumen(e)
        page.go("/") # Vuelve a la pantalla de bienvenida

    def crear_fila_resumen(icono, titulo, valor):
        """Función de ayuda para crear las filas del resumen."""
        return ft.Row(
            spacing=15,
            controls=[
                ft.Image(src=f"/assets/icons/{icono}", width=40, height=40),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(titulo, size=12, color=ft.Colors.GREY_600),
                        ft.Text(valor or "No seleccionado", size=16, weight=ft.FontWeight.BOLD),
                    ]
                )
            ]
        )

    bs = ft.BottomSheet(
        # Contenido se llenará dinámicamente
        content=ft.Container(padding=20),
        on_dismiss=cerrar_resumen,
    )

    def abrir_resumen(e):
        """Construye y muestra el resumen del pedido actual."""
        pedido = pedido_use_cases.obtener_pedido_actual()

        # Obtenemos el nombre de la categoría para mostrarlo
        categorias = {c.id: c.nombre for c in pedido_use_cases.obtener_categorias()}
        nombre_categoria = categorias.get(pedido.id_categoria, "N/A")

        # Construimos dinámicamente el contenido del resumen
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
                            crear_fila_resumen("tamano.png", "Tamaño", pedido.tamano_pastel),
                            crear_fila_resumen("pan.png", "Pan", pedido.tipo_pan),
                            crear_fila_resumen("cobertura.png", "Cobertura", pedido.tipo_cobertura),
                        ], expand=1),
                    ]
                ),
                ft.Divider(height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        # Aquí puedes añadir los datos de fecha y hora
                    ]
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Restablecer Pedido",
                    icon=ft.Icons.RESTART_ALT,
                    on_click=restablecer_pedido,
                    width=page.window.width
                )
            ]
        )
        bs.open = True
        page.update()

    page.open_summary = abrir_resumen
    page.overlay.append(bs)

    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE, size=24, font_family="Bebas Neue"
        )
    )
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
            # 1. Capturamos la vista y la función de animación
            vista, funcion_animacion = views.vista_confirmacion(page, finalizar_pedido_use_cases, pedido_use_cases)
            page.views.append(vista)
        page.update()

        if funcion_animacion:
            funcion_animacion()

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

    #boton_ver_resumen = ft.FloatingActionButton(
    #    icon=ft.Icons.RECEIPT_LONG,
    #    text="Ver Resumen",
    #    on_click=abrir_resumen,
    #    visible=False  # Empieza oculto y el router lo mostrará
    #)
    #page.add(boton_ver_resumen)  # Añadimos el botón a la página

    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
