# src/application/use_cases.py
import datetime
from .repositories import (
    PedidoRepository, TamanoRepository, CategoriaRepository, TipoCobertura,
    TipoPanRepository, TipoFormaRepository, TipoRellenoRepository,
    TipoCoberturaRepository, FinalizarPedidoRepository, Categoria, TipoPan,
    ImagenGaleriaRepository, TipoColorRepository, FormaPastel, TipoRelleno, Ticket
)
from src.domain.datos_entrega import DatosEntrega
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria
from src.infrastructure.printing_service import PrintingService
import subprocess
import os


class AuthUseCases:
    def login(self, username: str, password: str) -> bool:
        """
        Verifica las credenciales del usuario.
        TODO: Conectar a una base de datos de usuarios en el futuro.
        """
        # Por ahora, usamos credenciales fijas para la demostración
        if username.lower() == "admin" and password == "1234":
            print("INFO: Credenciales correctas.")
            return True
        else:
            print("ERROR: Credenciales incorrectas.")
            return False


class PedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, tamano_repo: TamanoRepository,
                 categoria_repo: CategoriaRepository, tipo_pan_repo: TipoPanRepository,
                 tipo_forma_repo: TipoFormaRepository, tipo_relleno_repo: TipoRellenoRepository,
                 tipo_cobertura_repo: TipoCoberturaRepository, finalizar_repo: FinalizarPedidoRepository,
                 imagen_galeria_repo: ImagenGaleriaRepository, tipo_color_repo: TipoColorRepository):
        self.pedido_repo = pedido_repo
        self.tamano_repo = tamano_repo
        self.categoria_repo = categoria_repo
        self.tipo_pan_repo = tipo_pan_repo
        self.tipo_forma_repo = tipo_forma_repo
        self.tipo_relleno_repo = tipo_relleno_repo
        self.tipo_cobertura_repo = tipo_cobertura_repo
        self.finalizar_repo = finalizar_repo
        self.tamanos_disponibles = []
        self.imagen_galeria_repo = imagen_galeria_repo
        self.tipo_color_repo = tipo_color_repo

    def guardar_datos_cliente(
            self, nombre, telefono, direccion, num_ext,
            entre_calles, cp, colonia, ciudad,
            municipio, estado, referencias
    ):
        """
        Guarda los datos del cliente en el objeto de pedido actual.
        """
        pedido = self.pedido_repo.obtener()

        pedido.nombre_cliente = nombre
        pedido.telefono_cliente = telefono
        pedido.direccion_cliente = direccion
        pedido.num_ext_cliente = num_ext
        pedido.entre_calles_cliente = entre_calles
        pedido.cp_cliente = cp
        pedido.colonia_cliente = colonia
        pedido.ciudad_cliente = ciudad
        pedido.municipio_cliente = municipio
        pedido.estado_cliente = estado
        pedido.referencias_cliente = referencias

        self.pedido_repo.guardar(pedido)

    def obtener_url_imagen_galeria_por_id(self, id_imagen: int) -> str | None:
        print(f"DIAGNÓSTICO: Buscando imagen con ID: {id_imagen}")
        imagen = self.imagen_galeria_repo.obtener_por_id(id_imagen)
        if imagen:
            print(f"DIAGNÓSTICO: Imagen encontrada. URL: {imagen.url}")
            return imagen.url
        else:
            print(f"DIAGNÓSTICO: No se encontró ninguna imagen con el ID {id_imagen}.")
            return None

    def buscar_imagenes_galeria(self, categoria: str | None, termino: str | None) -> list[ImagenGaleria]:
        return self.imagen_galeria_repo.buscar(categoria, termino)

    def seleccionar_imagen_decorado(self, id_imagen: int):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_imagen_id = id_imagen
        self.pedido_repo.guardar(pedido)

    def seleccionar_extra(self, extra: str | None):
        pedido = self.pedido_repo.obtener()
        pedido.extra_seleccionado = extra
        if extra != "Flor Artificial":
            pedido.extra_flor_cantidad = None
        self.pedido_repo.guardar(pedido)

    def guardar_cantidad_flor(self, cantidad: int | None):
        pedido = self.pedido_repo.obtener()
        pedido.extra_flor_cantidad = cantidad
        self.pedido_repo.guardar(pedido)


    def seleccionar_tipo_decorado(self, tipo_decorado: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_decorado = tipo_decorado
        # Reseteamos todos los detalles al cambiar la opción principal
        pedido.decorado_liso_detalle = None
        pedido.decorado_tematica_detalle = None
        pedido.decorado_imagen_id = None
        self.pedido_repo.guardar(pedido)

    def obtener_coberturas_disponibles(self, id_categoria: int, id_tipo_pan: int) -> list[TipoCobertura]:
        return self.tipo_cobertura_repo.obtener_por_categoria_y_pan(id_categoria, id_tipo_pan)

    def seleccionar_tipo_cobertura(self, nombre_cobertura: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_cobertura = nombre_cobertura
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Cobertura '{nombre_cobertura}' seleccionada. Estado del pedido: {pedido}")

    def obtener_rellenos_disponibles(self, id_categoria: int, id_tipo_pan: int) -> list[TipoRelleno]:
        return self.tipo_relleno_repo.obtener_por_categoria_y_pan(id_categoria, id_tipo_pan)

    def seleccionar_tipo_relleno(self, nombre_relleno: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_relleno = nombre_relleno
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Relleno '{nombre_relleno}' seleccionado. Estado del pedido: {pedido}")

    def obtener_formas_por_categoria(self, id_categoria: int) -> list[FormaPastel]:
        formas_disponibles = self.tipo_forma_repo.obtener_por_categoria(id_categoria)
        pedido = self.pedido_repo.obtener()
        if pedido.tamano_pastel:
            try:
                tamano_personas = int(pedido.tamano_pastel)

                if tamano_personas > 10:
                    print(f"INFO: Tamaño para {tamano_personas} personas detectado. Ocultando forma de corazón.")
                    formas_filtradas = [forma for forma in formas_disponibles if "corazón" not in forma.nombre.lower()]
                    return formas_filtradas
            except (ValueError, TypeError):
                print(f"ADVERTENCIA: El tamaño '{pedido.tamano_pastel}' no es un número válido.")
                pass
        return formas_disponibles

    def seleccionar_tipo_forma(self, nombre_forma: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_forma = nombre_forma
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Forma '{nombre_forma}' seleccionada. Estado del pedido: {pedido}")

    def obtener_panes_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        return self.tipo_pan_repo.obtener_por_categoria(id_categoria)

    def seleccionar_tipo_pan(self, nombre_pan: str):
        pedido = self.pedido_repo.obtener()
        if pedido.tipo_pan != nombre_pan:
            pedido.tipo_relleno = None
            pedido.tipo_cobertura = None
        pedido.tipo_pan = nombre_pan
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Pan '{nombre_pan}' seleccionado. Estado del pedido: {pedido}")

        pedido.tipo_pan = nombre_pan

        self.pedido_repo.guardar(pedido)
        print(f"INFO: Pan '{nombre_pan}' seleccionado. Estado del pedido: {pedido}")

    def obtener_categorias(self) -> list[Categoria]:
        return self.categoria_repo.obtener_todas()

    def seleccionar_categoria(self, id_categoria: int):
        pedido = self.pedido_repo.obtener()
        pedido.id_categoria = id_categoria
        pedido.tipo_pan = None
        pedido.tipo_forma = None
        pedido.tipo_relleno = None
        pedido.tipo_cobertura = None
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Categoría {id_categoria} seleccionada. Estado del pedido: {pedido}")

    def seleccionar_fecha(self, fecha: datetime.date):
        pedido = self.pedido_repo.obtener()
        pedido.fecha_entrega = fecha
        self.pedido_repo.guardar(pedido)

    def reiniciar_fecha(self):
        pedido = self.pedido_repo.obtener()
        pedido.fecha_entrega = None
        self.pedido_repo.guardar(pedido)

    def obtener_pedido_actual(self):
        return self.pedido_repo.obtener()

    def obtener_tamanos(self) -> list[str]:
        if not self.tamanos_disponibles:
            self.tamanos_disponibles = self.tamano_repo.obtener_todos()

        pedido = self.pedido_repo.obtener()
        if not pedido.tamano_pastel and self.tamanos_disponibles:
            pedido.tamano_pastel = self.tamanos_disponibles[0]
            self.pedido_repo.guardar(pedido)

        return self.tamanos_disponibles

    def seleccionar_siguiente_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos or not pedido.tamano_pastel:
            return

        try:
            idx = tamanos.index(pedido.tamano_pastel)
            nuevo_idx = (idx + 1) % len(tamanos)
            pedido.tamano_pastel = tamanos[nuevo_idx]
            self.pedido_repo.guardar(pedido)
        except ValueError:
            pedido.tamano_pastel = tamanos[0]
            self.pedido_repo.guardar(pedido)

    def seleccionar_anterior_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos or not pedido.tamano_pastel:
            return

        try:
            idx = tamanos.index(pedido.tamano_pastel)
            nuevo_idx = (idx - 1 + len(tamanos)) % len(tamanos)
            pedido.tamano_pastel = tamanos[nuevo_idx]
            self.pedido_repo.guardar(pedido)
        except ValueError:
            pedido.tamano_pastel = tamanos[0]
            self.pedido_repo.guardar(pedido)

    def reiniciar_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        pedido.tamano_pastel = tamanos[0] if tamanos else None
        self.pedido_repo.guardar(pedido)

    def guardar_mensaje_pastel(self, mensaje: str):
        pedido = self.pedido_repo.obtener()
        pedido.mensaje_pastel = mensaje
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Mensaje '{mensaje}' guardado.")


    def guardar_datos_y_finalizar(self, datos: dict) -> Pedido:
        pedido = self.pedido_repo.obtener()
        pedido.datos_entrega = DatosEntrega(**datos)
        self.pedido_repo.guardar(pedido)

        print("INFO: Finalizando pedido y guardando en la base de datos...")
        self.finalizar_repo.finalizar(pedido)
        print("INFO: ¡Pedido guardado permanentemente!")

        datos_qr = (
            f"Cliente: {pedido.datos_entrega.nombre_completo}\n"
            f"Telefono: {pedido.datos_entrega.telefono}\n"
            f"Fecha Entrega: {pedido.fecha_entrega.strftime('%d/%m/%Y') if pedido.fecha_entrega else 'N/A'}\n"
            f"Tamaño: {pedido.tamano_pastel}\n"
            f"Forma: {pedido.tipo_forma}\n"
            f"Pan: {pedido.tipo_pan}"
        )

        # 5. Devolver el pedido completo y el QR
        return pedido

    def seleccionar_color_decorado_liso(self, color: str):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_liso_color = color
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Color de decorado '{color}' seleccionado.")

    def obtener_colores_disponibles(self) -> list[str]:
        pedido = self.pedido_repo.obtener()
        if not pedido.id_categoria or not pedido.tipo_cobertura:
            return []
        return self.tipo_color_repo.obtener_por_categoria_y_cobertura(pedido.id_categoria, pedido.tipo_cobertura)

    def seleccionar_colores_decorado(self, color1: str | None, color2: str | None):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_liso_color1 = color1
        pedido.decorado_liso_color2 = color2
        self.pedido_repo.guardar(pedido)

    def guardar_detalle_decorado(self, tipo_principal: str, detalle: str, texto_tematica: str | None = None):
        pedido = self.pedido_repo.obtener()
        if tipo_principal == "Liso c/s Conchas de Betún":
            if pedido.decorado_liso_detalle != detalle:
                pedido.decorado_liso_color1 = None
                pedido.decorado_liso_color2 = None
            pedido.decorado_liso_detalle = detalle
            if detalle == "Diseño o Temática":
                pedido.decorado_tematica_detalle = texto_tematica
            else:
                pedido.decorado_tematica_detalle = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_componentes(self):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_forma = None
        pedido.tipo_pan = None
        pedido.tipo_relleno = None
        self.pedido_repo.guardar(pedido)

    def seleccionar_hora(self, hora: str):
        pedido = self.pedido_repo.obtener()
        pedido.hora_entrega = hora
        self.pedido_repo.guardar(pedido)

    def reiniciar_forma(self):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_forma = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_pan(self):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_pan = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_relleno(self):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_relleno = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_cobertura(self):
        """Resetea la selección de cobertura del pedido."""
        pedido = self.pedido_repo.obtener()
        pedido.tipo_cobertura = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_decorado(self):
        """Resetea todas las selecciones de la sección de decorado."""
        pedido = self.pedido_repo.obtener()
        pedido.tipo_decorado = None
        pedido.mensaje_pastel = None
        pedido.decorado_liso_detalle = None
        pedido.decorado_tematica_detalle = None
        pedido.decorado_imagen_id = None
        pedido.decorado_liso_color1 = None
        pedido.decorado_liso_color2 = None
        self.pedido_repo.guardar(pedido)


class FinalizarPedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, finalizar_repo: FinalizarPedidoRepository, categoria_repo: CategoriaRepository):
        self.pedido_repo = pedido_repo
        self.finalizar_repo = finalizar_repo
        self.categoria_repo = categoria_repo
        self.printing_service = PrintingService()


    def finalizar_e_imprimir_ticket(self):
        pedido_actual = self.pedido_repo.obtener()
        id_nuevo_pedido = self.finalizar_repo.guardar(pedido_actual)
        if id_nuevo_pedido:
            return self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
        return None

    def imprimir_ticket_por_folio(self, id_pedido: int):
        """
        Busca un ticket por su folio y lo manda a imprimir.
        """
        ticket = self.finalizar_repo.obtener_por_id(id_pedido)
        if ticket:
            try:
                ruta_pdf = self.printing_service.generar_ticket_pdf(ticket)
                subprocess.run(
                    [os.path.join("assets", "imprimir.exe"), ruta_pdf],
                    creationflags=subprocess.DETACHED_PROCESS
                )
            except Exception as e:
                print(f"ERROR: Falló el proceso de impresión: {e}")

        # if id_nuevo_pedido:
        #     ticket = self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
        #     if ticket:
        #         try:
        #             # Paso 1: Generar el PDF y obtener su ruta
        #             ruta_pdf = self.printing_service.generar_ticket_pdf(ticket)
        #
        #             # Paso 2: Enviar esa ruta a la impresora
        #             # self.printing_service.enviar_a_impresora(ruta_pdf)
        #
        #             # O si usas el CLI de Go:
        #             subprocess.run(
        #                 [os.path.join("assets", "imprimir.exe"), ruta_pdf],  # <-- Uso os.path.join para compatibilidad
        #                 creationflags=subprocess.DETACHED_PROCESS  # <-- Usa DETACHED_PROCESS para que no bloquee Flet
        #             )
        #
        #             return True
        #         except Exception as e:
        #             print(f"ERROR: Falló el proceso de impresión: {e}")
        #             return False
        #     return False

    def obtener_nombre_categoria(self, id_categoria: int) -> str:  # <-- NUEVO MÉTODO
        categoria = self.categoria_repo.obtener_por_id(id_categoria)
        return categoria.nombre if categoria else "Desconocida"

    def finalizar_y_obtener_ticket(self) -> Ticket | None:
        pedido_actual = self.pedido_repo.obtener()
        id_nuevo_pedido = self.finalizar_repo.guardar(pedido_actual)
        if id_nuevo_pedido:
            return self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
        return None

    def iniciar_nuevo_pedido(self):
        pedido_actual = self.pedido_repo.obtener()
        pedido_actual.reiniciar()
        self.pedido_repo.guardar(pedido_actual)
