# main.py
import flet as ft
import os
import sys
import threading
import time
from datetime import datetime
import msvcrt
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# === Watchdog integration flags (optional, defensive) ===
ENABLE_HEARTBEAT = os.getenv("ENABLE_HEARTBEAT", "1") == "1"
ENABLE_HEALTH_HTTP = os.getenv("ENABLE_HEALTH_HTTP", "1") == "1"
ENABLE_FS_WATCH = os.getenv("ENABLE_FS_WATCH", "0") == "1"  # off by default

HEARTBEAT_PATH = r"C:\\KioscoPP\\heartbeat.txt"
HEARTBEAT_INTERVAL_SEC = 10
_HEARTBEAT_STOP = threading.Event()

# Lockfile for single-instance
LOCKFILE_PATH = r"C:\\KioscoPP\\app.lock"
_lockfile_handle = None

def acquire_lock_or_exit():
    global _lockfile_handle
    try:
        os.makedirs(os.path.dirname(LOCKFILE_PATH), exist_ok=True)
        _lockfile_handle = open(LOCKFILE_PATH, "a+")
        msvcrt.locking(_lockfile_handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print("Otra instancia ya está corriendo. Saliendo sin error.")
        raise SystemExit(0)


def start_heartbeat():
    if not ENABLE_HEARTBEAT:
        return
    os.makedirs(os.path.dirname(HEARTBEAT_PATH), exist_ok=True)

    def _beat():
        while not _HEARTBEAT_STOP.is_set():
            try:
                with open(HEARTBEAT_PATH, "w", encoding="utf-8") as f:
                    f.write(datetime.now().isoformat())
            except Exception as e:
                print(f"[HB] Error escribiendo heartbeat: {e}")
            for _ in range(HEARTBEAT_INTERVAL_SEC):
                if _HEARTBEAT_STOP.is_set():
                    break
                time.sleep(1)

    threading.Thread(target=_beat, daemon=True).start()


def start_health_server(port: int = 35791):
    if not ENABLE_HEALTH_HTTP:
        return None

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            return  # silenciar logs por consola

    try:
        server = HTTPServer(("127.0.0.1", port), HealthHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"[HEALTH] Servidor de healthcheck en http://127.0.0.1:{port}/health")
        return server
    except OSError as e:
        print(f"[HEALTH] No se pudo iniciar en puerto {port}: {e}. Desactivado.")
        return None


def start_fs_watch(path: str, on_change):
    if not ENABLE_FS_WATCH:
        print("[FS] Watch de archivos desactivado por configuración.")
        return None
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except Exception:
        print("[FS] Librería 'watchdog' no instalada; watch desactivado.")
        return None

    class _Handler(FileSystemEventHandler):
        def __init__(self, cb):
            self.cb = cb
        def on_modified(self, event):
            try:
                self.cb(event.src_path)
            except Exception as e:
                print(f"[FS] Error en callback de cambio: {e}")

    try:
        observer = Observer()
        observer.schedule(_Handler(on_change), path, recursive=False)
        observer.start()
        print(f"[FS] Observando cambios en: {path}")
        return observer
    except Exception as e:
        print(f"[FS] No se pudo iniciar file watch: {e}")
        return None

from src.application.use_cases import PedidoUseCases, AuthUseCases, FinalizarPedidoUseCases
from src.infrastructure.persistence.memory_repository import PedidoRepositoryEnMemoria
from src.infrastructure.persistence.sqlite_repository import (
    TamanoRepositorySQLite, CategoriaRepositorySQLite,
    TipoPanRepositorySQLite, TipoFormaRepositorySQLite,
    TipoRellenoRepositorySQLite, TipoCoberturaRepositorySQLite,
    FinalizarPedidoRepositorySQLite, ImagenGaleriaRepositorySQLite,
    TipoColorRepositorySQLite, HorarioEntregaRepositorySQLite, DiaFestivoRepositorySQLite,
    PastelConfiguradoRepositorySQLite, ExtraRepositorySQLite,
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
    page.window.full_screen = True

    page.padding = 0

    # --- Watchdog integrations (optional, defensivas) ---
    # 1) Heartbeat a archivo para supervisores externos
    start_heartbeat()

    # 2) Servidor local de healthcheck HTTP
    health_server = start_health_server(35791)

    # 3) Observador de archivos opcional (desactivado por defecto)
    fs_observer = None
    def _on_fs_change(path_changed):
        try:
            page.snack_bar = ft.SnackBar(ft.Text(f"Actualizado: {os.path.basename(path_changed)}"))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(f"[FS] Error notificando cambio: {e}")

    if ENABLE_FS_WATCH:
        fs_observer = start_fs_watch(r"C:\\KioscoPP", _on_fs_change)

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
    pastel_config_repo = PastelConfiguradoRepositorySQLite(db_path)
    extra_repo = ExtraRepositorySQLite(db_path)

    config = {}
    default_api_url = "http://localhost:8000/api/pedidos"

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        API_URL_PEDIDOS = config.get("api_url_pedidos", default_api_url)
        print(f"INFO: URL de la API cargada desde config.json: {API_URL_PEDIDOS}")
    except FileNotFoundError:
        API_URL_PEDIDOS = default_api_url
        print(f"ADVERTENCIA: No se encontró config.json. Usando URL por defecto: {API_URL_PEDIDOS}")


    finalizar_repo_api = FinalizarPedidoRepositoryAPI(api_url=API_URL_PEDIDOS, db_path=db_path)
    finalizar_pedido_repo = FinalizarPedidoRepositorySQLite(db_path)

    auth_use_cases = AuthUseCases()
    pedido_use_cases = PedidoUseCases(
        pedido_repo, tamano_repo, categoria_repo,
        tipo_pan_repo, tipo_forma_repo, tipo_relleno_repo,
        tipo_cobertura_repo, finalizar_pedido_repo, imagen_galeria_repo,
        tipo_color_repo, horario_repo, dia_festivo_repo, pastel_config_repo,
        extra_repo
    )

    finalizar_repo_compuesto = FinalizarPedidoRepositoryComposite(
        sqlite_repo=finalizar_pedido_repo,
        api_repo=finalizar_repo_api
    )

    finalizar_pedido_use_cases = FinalizarPedidoUseCases(
        pedido_repo=pedido_repo,
        finalizar_repo=finalizar_repo_compuesto,
        categoria_repo=categoria_repo,
        extra_repo=extra_repo,
        pastel_config_repo=pastel_config_repo,
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
                ft.Image(src=f"C:/KioscoPP/img/iconos/{icono}", width=50, height=50),
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
        content=ft.Container(
            height=int(page.height * 0.90),
            padding=20,
            content=ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE),
        ),
        on_dismiss=cerrar_resumen,
        show_drag_handle=True
    )

    def abrir_resumen(e):
        pedido = pedido_use_cases.obtener_pedido_actual()

        config = pedido_use_cases.obtener_precio_pastel_configurado()
        precio_base = config.precio_base if config else 0.0
        precio_chocolate = config.precio_chocolate if config else 0.0
        precio_pastel = precio_chocolate if pedido.id_pan == 2 else precio_base

        if pedido.tipo_cobertura and "fondant" in pedido.tipo_cobertura.lower():
            precio_pastel *= 2

        def mxn(v):
            try:
                return f"${v:,.2f}"
            except Exception:
                return f"${v}"

        #precio_pastel = (config.precio_base if config else (pedido.precio_pastel or 0.0))

        extra_monto = pedido.extra_precio or 0.0
        extra_detalle = ""
        if pedido.extra_seleccionado:
            if pedido.extra_seleccionado == "Flor Artificial" and (pedido.extra_flor_cantidad or 0) > 0:
                unit = pedido.extra_precio or 0.0
                qty = pedido.extra_flor_cantidad or 0
                extra_monto = unit * qty
                extra_detalle = f"{pedido.extra_seleccionado} ({qty} x {mxn(unit)})"
            else:
                extra_detalle = pedido.extra_seleccionado

        total_mostrar = (precio_pastel or 0.0) + (extra_monto or 0.0)

        # 4) Nombre de la categoría
        categorias = {c.id: c.nombre for c in pedido_use_cases.obtener_categorias()}
        nombre_categoria = categorias.get(pedido.id_categoria, "N/A")

        # 5) Construir contenido del BottomSheet con montos e 'Incluye'
        bs.content.content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
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
                ft.Divider(height=15),

                # === Sección de montos ===
                ft.Text("Resumen de montos", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                    border_radius=10,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[ft.Text("Precio del pastel"), ft.Text(mxn(precio_pastel))]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Extra" + (f" – {extra_detalle}" if extra_detalle else "")),
                                    ft.Text(mxn(extra_monto))
                                ]
                            ),
                            ft.Divider(height=10),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[ft.Text("Total", weight=ft.FontWeight.W_700), ft.Text(mxn(total_mostrar), weight=ft.FontWeight.W_700)]
                            ),
                        ]
                    )
                ),

                # === Sección "Incluye" ===
                ft.Container(height=10),
                ft.Text("Incluye", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                    border_radius=10,
                    content=ft.Text((config.incluye if config else ""))
                ),

                ft.Divider(height=15),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        crear_fila_resumen("fecha.png", "Fecha de Entrega", pedido.fecha_entrega.strftime('%d/%m/%Y') if pedido.fecha_entrega else "N/A"),
                        crear_fila_resumen("hora.png", "Hora de Entrega", pedido.hora_entrega),
                    ]
                ),
                #ft.Container(height=20),
                #boton_restablecer_estilizado
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
        elif page.route == "/decorado1":
            page.views.append(views.vista_decorado1(page, pedido_use_cases))
        elif page.route == "/decorado2":
            page.views.append(views.vista_decorado2(page, pedido_use_cases))
        elif page.route == "/galeria":
            page.views.append(views.vista_galeria(page, pedido_use_cases))
        elif page.route == "/mensaje":
            page.views.append(views.vista_mensaje(page, pedido_use_cases))
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
            # Confirm before exiting to prevent accidental app closure
            def confirmar_salida(e):
                # Apagar integraciones de watchdog de forma limpia
                try:
                    _HEARTBEAT_STOP.set()
                except Exception:
                    pass
                try:
                    if health_server:
                        health_server.shutdown()
                except Exception:
                    pass
                try:
                    if fs_observer:
                        fs_observer.stop()
                        fs_observer.join(timeout=3)
                except Exception:
                    pass

                dlg.open = False
                page.update()
                page.window.destroy()

            def cancelar_salida(e):
                dlg.open = False
                page.update()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("¿Salir de la aplicación?"),
                content=ft.Text("Estás en la primera pantalla. ¿Deseas cerrar la aplicación?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar_salida),
                    ft.TextButton("Salir", on_click=confirmar_salida),
                ],
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/login")


if __name__ == "__main__":
    try:
        acquire_lock_or_exit()
    except SystemExit:
        raise
    try:
        ft.app(target=main, assets_dir="assets")
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"[FATAL] Error inesperado: {e}")
        sys.exit(1)



