# src/application/use_cases.py
import datetime
import os.path
import time

from .repositories import (
    PedidoRepository, TamanoRepository, CategoriaRepository, TipoCobertura,
    TipoPanRepository, TipoFormaRepository, TipoRellenoRepository,
    TipoCoberturaRepository, FinalizarPedidoRepository, Categoria, TipoPan,
    ImagenGaleriaRepository, TipoColorRepository, FormaPastel, TipoRelleno, Ticket,
    HorarioEntregaRepository, DiaFestivoRepository, PastelConfiguradoRepository,
    TamanoPastel, ExtraRepository, PastelConfigurado
)
from src.domain.datos_entrega import DatosEntrega
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria
from src.infrastructure.printing_service import PrintingService



class AuthUseCases:
    def login(self, username: str, password: str) -> bool:

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
                 imagen_galeria_repo: ImagenGaleriaRepository, tipo_color_repo: TipoColorRepository,
                 horario_repo: HorarioEntregaRepository, dia_festivo_repo: DiaFestivoRepository,
                 pastel_config_repo: PastelConfiguradoRepository, extra_repo: ExtraRepository,):
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
        self.horario_repo = horario_repo
        self.dia_festivo_repo = dia_festivo_repo
        self.pastel_config_repo = pastel_config_repo
        self.extra_repo = extra_repo

    def guardar_datos_cliente(
            self, nombre, telefono, direccion, num_ext,
            entre_calles, cp, colonia, ciudad,
            municipio, estado, referencias
    ):
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
            print(f"DIAGNÓSTICO: Imagen encontrada. URL: {imagen.ruta}")
            return imagen.ruta
        else:
            print(f"DIAGNÓSTICO: No se encontró ninguna imagen con el ID {id_imagen}.")
            return None

    def buscar_imagenes_galeria(self, categoria: str | None, termino: str | None) -> list[ImagenGaleria]:
        return self.imagen_galeria_repo.buscar(categoria, termino)

    def seleccionar_imagen_decorado(self, id_imagen: int):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_imagen_id = id_imagen
        self.pedido_repo.guardar(pedido)

    def seleccionar_extra(self, extra_descripcion: str | None):
        pedido = self.pedido_repo.obtener()

        if not extra_descripcion:
            pedido.extra_seleccionado = None
            pedido.extra_precio = None
            pedido.extra_flor_cantidad = None
        else:
            extra_obj = self.extra_repo.obtener_por_descripcion(extra_descripcion)
            if extra_obj:
                pedido.extra_seleccionado = extra_obj.descripcion
                pedido.extra_precio = extra_obj.costo
            else:
                # Si no se encuentra en la BD, se limpia (medida de seguridad)
                pedido.extra_seleccionado = None
                pedido.extra_precio = None

        # Si el extra no es 'Flor Artificial', reseteamos la cantidad
        if extra_descripcion != "Flor Artificial":
            pedido.extra_flor_cantidad = None

        self.pedido_repo.guardar(pedido)

    def guardar_cantidad_flor(self, cantidad: int | None):
        pedido = self.pedido_repo.obtener()
        pedido.extra_flor_cantidad = cantidad
        self.pedido_repo.guardar(pedido)


    def seleccionar_tipo_decorado(self, tipo_decorado: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_decorado = tipo_decorado
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


    def obtener_panes_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        return self.tipo_pan_repo.obtener_por_categoria(id_categoria)


    def seleccionar_tipo_pan(self, id_pan: int,  nombre_pan: str):
        pedido = self.pedido_repo.obtener()
        if pedido.tipo_pan != nombre_pan:
            pedido.tipo_relleno = None
            pedido.tipo_cobertura = None
        pedido.id_pan = id_pan
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
        categoria_obj = self.categoria_repo.obtener_por_id(id_categoria) # (Necesitarás este método en el repo)
        if categoria_obj:
            pedido.nombre_categoria = categoria_obj.nombre

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

    def obtener_tamanos(self) -> list[TamanoPastel]:
        if not self.tamanos_disponibles:
            # El repositorio ahora devuelve una lista de objetos TamanoPastel
            self.tamanos_disponibles = self.tamano_repo.obtener_todos()

        pedido = self.pedido_repo.obtener()

        # Si no hay un tamaño seleccionado Y la lista no está vacía
        if not pedido.tamano_pastel and self.tamanos_disponibles:
            # Asignamos el ID y el nombre del primer tamaño de la lista
            pedido.id_tamano = self.tamanos_disponibles[0].id
            pedido.tamano_pastel = self.tamanos_disponibles[0].nombre
            self.pedido_repo.guardar(pedido)

        return self.tamanos_disponibles

    def seleccionar_siguiente_tamano(self):
        """Busca el tamaño actual en la lista y selecciona el siguiente."""
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos:
            return

        try:
            # Buscamos el índice del tamaño actual por su nombre
            nombres_tamanos = [t.nombre for t in tamanos]
            idx_actual = nombres_tamanos.index(pedido.tamano_pastel)

            # Calculamos el nuevo índice
            nuevo_idx = (idx_actual + 1) % len(tamanos)

            # Guardamos el ID y el nombre del nuevo tamaño
            pedido.id_tamano = tamanos[nuevo_idx].id
            pedido.tamano_pastel = tamanos[nuevo_idx].nombre
            pedido.tamano_descripcion = tamanos[nuevo_idx].descripcion
            pedido.tamano_peso = tamanos[nuevo_idx].peso
            self.pedido_repo.guardar(pedido)
        except ValueError:
            # Si algo falla, asigna el primero por defecto
            pedido.id_tamano = tamanos[0].id
            pedido.tamano_pastel = tamanos[0].nombre
            self.pedido_repo.guardar(pedido)

    def seleccionar_anterior_tamano(self):
        """Busca el tamaño actual en la lista y selecciona el anterior."""
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos:
            return

        try:
            nombres_tamanos = [t.nombre for t in tamanos]
            idx_actual = nombres_tamanos.index(pedido.tamano_pastel)

            # Calculamos el nuevo índice
            nuevo_idx = (idx_actual - 1 + len(tamanos)) % len(tamanos)

            # Guardamos el ID y el nombre del nuevo tamaño
            pedido.id_tamano = tamanos[nuevo_idx].id
            pedido.tamano_pastel = tamanos[nuevo_idx].nombre
            self.pedido_repo.guardar(pedido)
        except ValueError:
            # Si algo falla, asigna el primero por defecto
            pedido.id_tamano = tamanos[0].id
            pedido.tamano_pastel = tamanos[0].nombre
            self.pedido_repo.guardar(pedido)



    def calcular_y_guardar_precios_finales(self):
        """
        Calcula el precio total del pedido y guarda los montos en el objeto Pedido.
        """
        pedido = self.pedido_repo.obtener()

        # Validar que tenemos todos los IDs necesarios
        if not all([pedido.id_categoria, pedido.id_pan, pedido.id_forma, pedido.id_tamano]):
            print("ADVERTENCIA: Faltan IDs para calcular el precio.")
            return

        # 1. Obtener precio del pastel y depósito desde la BD
        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        precio_pastel = config.precio_final if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0

        # 2. Obtener costo del extra (ya guardado en el pedido)
        extra_costo = pedido.extra_precio or 0.0

        # 3. Calcular el total
        total = precio_pastel + extra_costo  # El depósito puede o no sumarse al total final

        # 4. Guardar todos los precios en el pedido en memoria
        pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total
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
        self.finalizar_repo.guardar(pedido)
        print("INFO: ¡Pedido guardado permanentemente!")

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
        pedido = self.pedido_repo.obtener()
        pedido.tipo_cobertura = None
        self.pedido_repo.guardar(pedido)

    def reiniciar_decorado(self):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_decorado = None
        pedido.mensaje_pastel = None
        pedido.decorado_liso_detalle = None
        pedido.decorado_tematica_detalle = None
        pedido.decorado_imagen_id = None
        pedido.decorado_liso_color1 = None
        pedido.decorado_liso_color2 = None
        self.pedido_repo.guardar(pedido)

    def iniciar_nuevo_pedido(self):
        pedido_actual = self.pedido_repo.obtener()
        pedido_actual.reiniciar()
        self.pedido_repo.guardar(pedido_actual)

    def obtener_rangos_de_hora(self, fecha_seleccionada: datetime.date) -> list[str]:
        print(f"\n[DEBUG] === Iniciando cálculo de rangos para fecha: {fecha_seleccionada} ===")

        horario = self.horario_repo.obtener_horario()
        if not horario:
            print("[DEBUG] No se encontró un horario de entrega en la base de datos.")
            return []

        print(
            f"[DEBUG] Horario de operación obtenido: {horario.hora_inicio.strftime('%H:%M')} a {horario.hora_fin.strftime('%H:%M')}")

        # 1. Revisa si es día festivo (esto llamará a la función con sus propios prints)
        es_dia_festivo = self.dia_festivo_repo.es_festivo(fecha_seleccionada)

        # 2. Elige el intervalo de tiempo
        intervalo_horas = 2 if es_dia_festivo else 1
        print(f"[DEBUG] Intervalo de horas determinado: {intervalo_horas} hora(s)")

        # 3. "Corta" el día en rangos
        rangos = []
        hora_actual = datetime.datetime.combine(fecha_seleccionada, horario.hora_inicio)
        hora_final = datetime.datetime.combine(fecha_seleccionada, horario.hora_fin)

        print("[DEBUG] --- Generando rangos ---")
        while hora_actual < hora_final:
            hora_siguiente = hora_actual + datetime.timedelta(hours=intervalo_horas)
            if hora_siguiente > hora_final:
                hora_siguiente = hora_final

            # Formateamos a AM/PM como te gustó
            rango_str = f"{hora_actual.strftime('%I:%M %p')} - {hora_siguiente.strftime('%I:%M %p')}"
            rangos.append(rango_str)
            print(f"[DEBUG]   - Rango generado: {rango_str}")
            hora_actual = hora_siguiente

        print(f"[DEBUG] === Cálculo finalizado. Se generaron {len(rangos)} rangos. ===\n")
        return rangos

    def seleccionar_tamano(self, id_tamano: int, nombre_tamano: str, descripcion_tamano: str):
        pedido = self.pedido_repo.obtener()
        pedido.id_tamano = id_tamano
        pedido.tamano_pastel = nombre_tamano
        pedido.descripcion_pastel = descripcion_tamano
        self.pedido_repo.guardar(pedido)

    def seleccionar_tipo_forma(self, id_forma: int, nombre_forma: str):
        pedido = self.pedido_repo.obtener()
        pedido.id_forma = id_forma
        pedido.tipo_forma = nombre_forma
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Forma '{nombre_forma}' seleccionada. Estado del pedido: {pedido}")

    def obtener_precio_pastel_configurado(self) -> PastelConfigurado:
        pedido = self.pedido_repo.obtener()

        print("\n[DEBUG] === Consultando Precio de Pastel Configurado ===")
        print(f"[DEBUG] ID Categoría: {pedido.id_categoria}")
        print(f"[DEBUG] ID Pan: {pedido.id_pan}")
        print(f"[DEBUG] ID Forma: {pedido.id_forma}")
        print(f"[DEBUG] ID Tamaño: {pedido.id_tamano}")

        if not all([pedido.id_categoria, pedido.id_pan, pedido.id_forma, pedido.id_tamano]):
            print("[DEBUG] Faltan IDs para calcular el precio. Devolviendo 0.0")
            print("[DEBUG] =============================================\n")
            return 0.0

        # Llama al repositorio para obtener la configuración
        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        # --- DEBUG PRINT: Muestra lo que devolvió la base de datos ---
        if config:
            print(f"[DEBUG] Configuración encontrada: Precio=${config.precio_final}, Depósito=${config.monto_deposito}")
        else:
            print("[DEBUG] No se encontró una configuración de pastel para esos IDs.")
        print("[DEBUG] =============================================\n")

        precio_pastel = config.precio_final if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0

        extra_costo = pedido.extra_precio or 0.0
        total = precio_pastel + extra_costo

        # Guarda los precios en el pedido
        pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total
        self.pedido_repo.guardar(pedido)

        return config


class FinalizarPedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, finalizar_repo: FinalizarPedidoRepository,
                 pastel_config_repo: PastelConfiguradoRepository, extra_repo: ExtraRepository, categoria_repo: CategoriaRepository):
        self.pedido_repo = pedido_repo
        self.finalizar_repo = finalizar_repo
        self.pastel_config_repo = pastel_config_repo
        self.extra_repo = extra_repo
        self.categoria_repo = categoria_repo
        self.printing_service = PrintingService()


    def generar_y_guardar_codigo_imagen(self):
        """
        Crea un código único con los IDs de la configuración del pastel y lo guarda.
        """
        pedido = self.pedido_repo.obtener()
        if all([pedido.id_categoria, pedido.id_pan, pedido.id_forma, pedido.id_tamano]):
            # Combinamos los IDs para formar el nombre del archivo de imagen
            codigo = f"{pedido.id_categoria}-{pedido.id_pan}-{pedido.id_forma}-{pedido.id_tamano}"
            pedido.imagen_pastel = codigo
            self.pedido_repo.guardar(pedido)

    def finalizar_y_calcular_total(self):
        pedido = self.pedido_repo.obtener()
        ruta_impresion = None

        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        precio_pastel = config.precio_final if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0

        extra_costo = pedido.extra_precio or 0.0
        if pedido.extra_seleccionado == "Flor Artificial" and pedido.extra_flor_cantidad:
            extra_costo *= pedido.extra_flor_cantidad

        total = precio_pastel + extra_costo

        pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total

        #self.generar_y_guardar_codigo_imagen()

        id_nuevo_pedido = self.finalizar_repo.guardar(pedido)

        if id_nuevo_pedido:
            ticket = self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
            if ticket:
                try:
                    ruta_impresion = self.printing_service.generar_ticket_pdf(ticket)
                    self.printing_service.enviar_a_impresora(ruta_impresion)
                    return True
                except Exception as e:
                    print(f"ERROR: Falló el proceso de impresión: {e}")
        return False


    def obtener_nombre_categoria(self, id_categoria: int) -> str:
        categoria = self.categoria_repo.obtener_por_id(id_categoria)
        return categoria.nombre if categoria else "Desconocida"

    def finalizar_y_obtener_ticket(self) -> Ticket | None:
        pedido = self.pedido_repo.obtener()

        # Calcular precios y totales ANTES de guardar para que la API reciba los valores correctos
        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        precio_pastel = config.precio_final if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0

        extra_costo = pedido.extra_precio or 0.0
        if pedido.extra_seleccionado == "Flor Artificial" and pedido.extra_flor_cantidad:
            extra_costo *= pedido.extra_flor_cantidad

        total = precio_pastel + extra_costo

        pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total

        # Guardar una sola vez (local + API vía repositorio compuesto)
        id_nuevo_pedido = self.finalizar_repo.guardar(pedido)
        if id_nuevo_pedido:
            return self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
        return None
