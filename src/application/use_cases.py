import datetime
import os.path
import logging

logger = logging.getLogger(__name__)

from .repositories import (
    PedidoRepository, TamanoRepository, CategoriaRepository, TipoCobertura,
    TipoPanRepository, TipoFormaRepository, TipoRellenoRepository,
    TipoCoberturaRepository, FinalizarPedidoRepository, Categoria, TipoPan,
    ImagenGaleriaRepository, TipoColorRepository, FormaPastel, TipoRelleno, Ticket,
    HorarioEntregaRepository, DiaFestivoRepository, PastelConfiguradoRepository,
    TamanoPastel, ExtraRepository, PastelConfigurado, ExtraChorreadoRepository, TamanoRectangularRepository
)
from src.domain.datos_entrega import DatosEntrega
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria
from src.infrastructure.printing_service import PrintingService



class AuthUseCases:
    def login(self, username: str, password: str) -> bool:

        if username.lower() == "admin" and password == "1234":
            logger.info("INFO: Credenciales correctas.")
            return True
        else:
            logger.error("ERROR: Credenciales incorrectas.")
            return False


class PedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, tamano_repo: TamanoRepository,
                 categoria_repo: CategoriaRepository, tipo_pan_repo: TipoPanRepository,
                 tipo_forma_repo: TipoFormaRepository, tipo_relleno_repo: TipoRellenoRepository,
                 tipo_cobertura_repo: TipoCoberturaRepository, finalizar_repo: FinalizarPedidoRepository,
                 imagen_galeria_repo: ImagenGaleriaRepository, tipo_color_repo: TipoColorRepository,
                 horario_repo: HorarioEntregaRepository, dia_festivo_repo: DiaFestivoRepository,
                 pastel_config_repo: PastelConfiguradoRepository, extra_repo: ExtraRepository,
                 extra_chorreado_repo: ExtraChorreadoRepository, tamano_rectangular_repo: TamanoRectangularRepository):
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
        self.extra_chorreado_repo = extra_chorreado_repo
        self.tamano_rectangular_repo = tamano_rectangular_repo

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
        logger.info(f"DIAGNÓSTICO: Buscando imagen con ID: {id_imagen}")
        imagen = self.imagen_galeria_repo.obtener_por_id(id_imagen)
        if imagen:
            logger.info(f"Imagen encontrada. URL: {imagen.ruta}")
            return imagen.ruta
        else:
            logger.info(f"DIAGNÓSTICO: No se encontró ninguna imagen con el ID {id_imagen}.")
            return None

    def buscar_imagenes_galeria(self, categoria: str | None, termino: str | None) -> list[ImagenGaleria]:
        return self.imagen_galeria_repo.buscar(categoria, termino)

    def seleccionar_imagen_decorado(self, id_imagen: int):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_imagen_id = id_imagen
        try:
            imagen = self.imagen_galeria_repo.obtener_por_id(id_imagen)
            if imagen and getattr(imagen, "ruta", None):
                img_file = os.path.basename(imagen.ruta)
                pedido.imagen_pastel = os.path.splitext(img_file)[0]
            else:
                pedido.imagen_pastel = None
        except Exception as e:
            logger.warning(f"ADVERTENCIA: No se pudo obtener la URL de la imagen con ID {id_imagen}: {e}")
            pedido.imagen_pastel = None
        self.pedido_repo.guardar(pedido)

    def seleccionar_extra(self, extra_descripcion: str | None):
        pedido = self.pedido_repo.obtener()
        nuevo_precio_extra = None

        if not extra_descripcion or extra_descripcion == "Ninguno":
            pedido.extra_seleccionado = None
            pedido.extra_precio = None
            pedido.extra_flor_cantidad = None
            logger.info("INFO: Ningún extra seleccionado.")

        elif extra_descripcion in ["Chorreado Dorado", "Chorreado Plateado"]:
            pedido.extra_seleccionado = extra_descripcion
            pedido.extra_flor_cantidad = None
            logger.info(f"INFO: Extra '{extra_descripcion}' seleccionado. Verificando forma y tamaño/peso...")

            if pedido.tipo_forma and "redonda" in pedido.tipo_forma.lower():
                logger.info("INFO: La forma es Redonda.")
                medidas = pedido.tamano_descripcion
                if medidas:
                    logger.info(f"INFO: Buscando precio de chorreado para tamaño redondo: '{medidas}'")
                    precio_chorreado = self.extra_chorreado_repo.obtener_precio_por_tamano(medidas)
                    if precio_chorreado is not None:
                        nuevo_precio_extra = precio_chorreado
                        logger.info(f"INFO: Precio encontrado en extra_chorreado (redondo): ${nuevo_precio_extra}")
                    else:
                        nuevo_precio_extra = 0.0
                        logger.warning(
                            f"WARN: Tamaño redondo '{medidas}' no encontrado en extra_chorreado. Precio establecido a 0.0")
                else:
                    nuevo_precio_extra = 0.0
                    logger.warning("WARN: No se encontraron 'medidas_pastel' para redondo. Precio de chorreado a 0.0")

            elif pedido.tipo_forma and "rectangular" in pedido.tipo_forma.lower():
                logger.info("INFO: La forma es Rectangular.")
                peso = pedido.tamano_peso
                if peso:
                    logger.info(f"INFO: Buscando precio de chorreado para peso rectangular: '{peso}'")
                    precio_rectangular = self.tamano_rectangular_repo.obtener_precio_por_peso(peso)
                    if precio_rectangular is not None:
                        nuevo_precio_extra = precio_rectangular
                        logger.info(f"INFO: Precio encontrado en tamano_rectangular (por peso): ${nuevo_precio_extra}")
                    else:
                        nuevo_precio_extra = 0.0
                        logger.warning(
                            f"WARN: Peso rectangular '{peso}' no encontrado en tamano_rectangular. Precio establecido a 0.0")
                else:
                    nuevo_precio_extra = 0.0
                    logger.warning("WARN: No se encontró 'peso_pastel' para rectangular. Precio de chorreado a 0.0")

            else:
                nuevo_precio_extra = 0.0
                logger.info(
                    f"INFO: La forma '{pedido.tipo_forma}' no es Redonda ni Rectangular. Precio de chorreado establecido a 0.0")

            pedido.extra_precio = nuevo_precio_extra

        else:
            logger.info(f"INFO: Buscando extra '{extra_descripcion}' en tabla 'extras' general.")
            extra_obj = self.extra_repo.obtener_por_descripcion(extra_descripcion)
            if extra_obj:
                pedido.extra_seleccionado = extra_obj.descripcion
                nuevo_precio_extra = extra_obj.costo
                logger.info(f"INFO: Extra general encontrado. Precio unitario: ${nuevo_precio_extra}")
            else:
                pedido.extra_seleccionado = None
                nuevo_precio_extra = None
                logger.warning(f"WARN: Extra '{extra_descripcion}' no encontrado en tabla 'extras'.")

            pedido.extra_precio = nuevo_precio_extra
            if extra_descripcion != "Flor Artificial":
                pedido.extra_flor_cantidad = None

        self.pedido_repo.guardar(pedido)
        logger.info(
            f"INFO: Estado final del extra guardado: Seleccionado='{pedido.extra_seleccionado}', Precio Unitario='{pedido.extra_precio}', Cant Flor='{pedido.extra_flor_cantidad}'")


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
        logger.info(f"INFO: Cobertura '{nombre_cobertura}' seleccionada. Estado del pedido: {pedido}")

    def obtener_rellenos_disponibles(self, id_categoria: int, id_tipo_pan: int) -> list[TipoRelleno]:
        return self.tipo_relleno_repo.obtener_por_categoria_y_pan(id_categoria, id_tipo_pan)

    def seleccionar_tipo_relleno(self, nombre_relleno: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_relleno = nombre_relleno
        self.pedido_repo.guardar(pedido)
        logger.info(f"INFO: Relleno '{nombre_relleno}' seleccionado. Estado del pedido: {pedido}")

    def obtener_formas_por_categoria(self, id_categoria: int) -> list[FormaPastel]:
        formas_disponibles = self.tipo_forma_repo.obtener_por_categoria(id_categoria)
        pedido = self.pedido_repo.obtener()

        if pedido.tamano_pastel:
            try:
                if pedido.tamano_pastel == "150 a 180":
                    tamano_personas = 180
                else:
                    tamano_personas = int(pedido.tamano_pastel)

                if tamano_personas > 10:
                    logger.info(f"INFO: Tamaño para {tamano_personas} personas detectado. Ocultando forma de corazón.")
                    formas_disponibles  = [forma for forma in formas_disponibles if "corazón" not in forma.nombre.lower()]

                tamanos_permitidos_redonda = [5, 10, 15, 18, 20]
                if tamano_personas not in tamanos_permitidos_redonda:
                    formas_disponibles = [f for f in formas_disponibles if 'redonda' not in f.nombre.lower()]
                    logger.info(f"INFO: Tamaño para {tamano_personas}. Se ha ocultado la forma 'Redonda'.")

                tamanos_permitidos_rectangular = [20, 40, 60, 80, 120, 150, 180]
                if tamano_personas not in tamanos_permitidos_rectangular:
                    formas_disponibles = [f for f in formas_disponibles if "rectangular" not in f.nombre.lower()]
                    logger.info(f"INFO: Tamaño para {tamano_personas}. Se oculta la forma rectangular.")

                tamanos_permitidos_altos = [15, 30, 35, 40]
                if tamano_personas not in tamanos_permitidos_altos:
                    formas_disponibles = [f for f in formas_disponibles if 'alto (3 o 4 capas)' not in f.nombre.lower()]
                    logger.info(f"INFO: Tamaño para {tamano_personas}. Se oculta la forma Altos.")

                tamanos_permitidos_pisos = [25, 30, 35, 40, 60, 70, 80, 100, 150,160, 200, 250]
                if tamano_personas not in tamanos_permitidos_pisos:
                    formas_disponibles = [f for f in formas_disponibles if 'pisos' not in f.nombre.lower()]
                    logger.info(f"INFO: Tamanño para {tamano_personas}. Se oculta la forma 'Pisos'.")

                return formas_disponibles
            except (ValueError, TypeError):
                logger.warning(f"ADVERTENCIA: El tamaño '{pedido.tamano_pastel}' no es un número válido.")
                pass
        return formas_disponibles


    def obtener_panes_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        panes_disponibles = self.tipo_pan_repo.obtener_por_categoria(id_categoria)
        pedido = self.pedido_repo.obtener()
        if pedido.tipo_forma and "pisos" in pedido.tipo_forma.lower():
            panes_filtrados = [
                pan for pan in panes_disponibles
                if "chocolate" not in pan.nombre.lower()
            ]
            logger.info(f"INFO: Forma 'Pisos' seleccionada. Se ha ocultado el pan de chocolate.")
            return panes_filtrados
        return panes_disponibles

    def reiniciar_detalles_decorado(self):
        logger.info("[DEBUG] UC: Ejecutando reiniciar_detalles_decorado...")
        pedido = self.pedido_repo.obtener()
        pedido.decorado_liso_color1 = None
        pedido.decorado_liso_color2 = None
        pedido.decorado_tematica_detalle = None
        self.pedido_repo.guardar(pedido)

    def seleccionar_tipo_pan(self, id_pan: int,  nombre_pan: str):
        pedido = self.pedido_repo.obtener()
        if pedido.tipo_pan != nombre_pan:
            pedido.tipo_relleno = None
            pedido.tipo_cobertura = None
        pedido.id_pan = id_pan
        pedido.tipo_pan = nombre_pan
        self.pedido_repo.guardar(pedido)
        logger.info(f"INFO: Pan '{nombre_pan}' seleccionado. Estado del pedido: {pedido}")

    def obtener_categorias(self) -> list[Categoria]:
        pedido = self.pedido_repo.obtener()
        if not pedido.id_tamano:
            return []
        return self.categoria_repo.obtener_todas(pedido.id_tamano)

    def seleccionar_categoria(self, id_categoria: int):
        pedido = self.pedido_repo.obtener()
        pedido.id_categoria = id_categoria
        pedido.tipo_pan = None
        pedido.tipo_forma = None
        pedido.tipo_relleno = None
        pedido.tipo_cobertura = None
        categoria_obj = self.categoria_repo.obtener_por_id(id_categoria)
        if categoria_obj:
            pedido.nombre_categoria = categoria_obj.nombre

        self.pedido_repo.guardar(pedido)
        logger.info(f"INFO: Categoría {id_categoria} seleccionada. Estado del pedido: {pedido}")

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
            self.tamanos_disponibles = self.tamano_repo.obtener_todos()

        pedido = self.pedido_repo.obtener()

        if not pedido.tamano_pastel and self.tamanos_disponibles:
            pedido.id_tamano = self.tamanos_disponibles[0].id
            pedido.tamano_pastel = self.tamanos_disponibles[0].nombre
            self.pedido_repo.guardar(pedido)

        return self.tamanos_disponibles

    def seleccionar_siguiente_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos:
            return

        try:
            nombres_tamanos = [t.nombre for t in tamanos]
            idx_actual = nombres_tamanos.index(pedido.tamano_pastel)

            nuevo_idx = (idx_actual + 1) % len(tamanos)

            pedido.id_tamano = tamanos[nuevo_idx].id
            pedido.tamano_pastel = tamanos[nuevo_idx].nombre
            self.pedido_repo.guardar(pedido)
        except ValueError:
            pedido.id_tamano = tamanos[0].id
            pedido.tamano_pastel = tamanos[0].nombre
            self.pedido_repo.guardar(pedido)

    def seleccionar_anterior_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos:
            return

        try:
            nombres_tamanos = [t.nombre for t in tamanos]
            idx_actual = nombres_tamanos.index(pedido.tamano_pastel)

            nuevo_idx = (idx_actual - 1 + len(tamanos)) % len(tamanos)

            pedido.id_tamano = tamanos[nuevo_idx].id
            pedido.tamano_pastel = tamanos[nuevo_idx].nombre
            self.pedido_repo.guardar(pedido)
        except ValueError:
            pedido.id_tamano = tamanos[0].id
            pedido.tamano_pastel = tamanos[0].nombre
            self.pedido_repo.guardar(pedido)

    def calcular_y_guardar_precios_finales(self):
        pedido = self.pedido_repo.obtener()

        if not all([pedido.id_categoria, pedido.id_pan, pedido.id_forma, pedido.id_tamano]):
            logger.warning("ADVERTENCIA: Faltan IDs para calcular el precio.")
            return

        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        precio_pastel = config.precio_base if config else 0.0
        precio_chocolate = config.precio_chocolate if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0
        extra_costo = pedido.extra_precio or 0.0

        if pedido.tipo_cobertura and "fondant" in pedido.tipo_cobertura.lower():
            logger.info(f"INFO: Cobertura de Fondant detectada. Duplicando precio base de ${precio_pastel}.")
            precio_pastel *= 2
            precio_chocolate *= 2

        total = precio_pastel + extra_costo

        if pedido.id_pan == 2 and precio_chocolate > 0.0:
            pedido.precio_pastel = precio_chocolate
        else:
            pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total

        if config:
            pedido.tamano_peso = getattr(config, 'peso_pastel', None)
            pedido.tamano_descripcion = getattr(config, 'medidas_pastel', None)

        self.pedido_repo.guardar(pedido)

    def reiniciar_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        pedido.tamano_pastel = tamanos[0] if tamanos else None
        self.pedido_repo.guardar(pedido)

    def guardar_edad_pastel(self, edad: int | None):
        pedido = self.pedido_repo.obtener()
        pedido.edad_pastel = edad
        self.pedido_repo.guardar(pedido)

    def guardar_mensaje_pastel(self, mensaje: str):
        pedido = self.pedido_repo.obtener()
        pedido.mensaje_pastel = mensaje
        self.pedido_repo.guardar(pedido)
        logger.info(f"INFO: Mensaje '{mensaje}' guardado.")


    def guardar_datos_y_finalizar(self, datos: dict) -> Pedido:
        pedido = self.pedido_repo.obtener()
        pedido.datos_entrega = DatosEntrega(**datos)
        self.pedido_repo.guardar(pedido)

        logger.info("INFO: Finalizando pedido y guardando en la base de datos...")
        self.finalizar_repo.guardar(pedido)
        logger.info("INFO: ¡Pedido guardado permanentemente!")

        return pedido

    def seleccionar_color_decorado_liso(self, color: str):
        pedido = self.pedido_repo.obtener()
        pedido.decorado_liso_color = color
        self.pedido_repo.guardar(pedido)
        logger.info(f"INFO: Color de decorado '{color}' seleccionado.")


    def obtener_todos_los_colores(self) -> list[str]:
        return self.tipo_color_repo.obtener_todos()

    def check_continuar_decorado(self) -> bool:
        pedido = self.pedido_repo.obtener()
        logger.info("\n[DEBUG] UC: ---- Verificando 'check_continuar_decorado' ----")
        logger.info(f"[DEBUG] UC: Tipo decorado: '{pedido.tipo_decorado}'")
        logger.info(f"[DEBUG] UC: Detalle liso: '{pedido.decorado_liso_detalle}'")
        logger.info(f"[DEBUG] UC: Detalle temática: '{pedido.decorado_tematica_detalle}'")
        logger.info(f"[DEBUG] UC: Color 1 seleccionado: '{pedido.decorado_liso_color1}'")

        if not pedido.tipo_decorado:
            logger.info("[DEBUG] UC: No hay tipo de decorado seleccionado. Resultado=False")
            logger.info("[DEBUG] UC: ------------------------------------------\n")
            return False

        listo = False
        if pedido.tipo_decorado == "Liso c/s Conchas de Betún":
            if not pedido.decorado_liso_detalle:
                logger.info("[DEBUG] UC: Decorado 'Liso...' seleccionado, pero falta detalle. Resultado=False")
            elif not pedido.decorado_liso_color1:
                logger.info(
                    "[DEBUG] UC: Decorado 'Liso...' con detalle seleccionado, pero falta Color 1. Resultado=False")
            else:
                listo = True
                logger.info("[DEBUG] UC: Decorado 'Liso...' con detalle y Color 1 seleccionados. Resultado=True")

        elif pedido.tipo_decorado == "Temática o Personaje":
            tiene_texto_tematica = bool(pedido.decorado_tematica_detalle and pedido.decorado_tematica_detalle.strip())
            logger.info(f"[DEBUG] UC: Decorado 'Temática'. ¿Tiene texto?: {tiene_texto_tematica}")
            listo = tiene_texto_tematica

        elif pedido.tipo_decorado == "Imágenes Prediseñadas":
            tiene_imagen = pedido.decorado_imagen_id is not None
            logger.info(f"[DEBUG] UC: Decorado 'Imágenes'. ¿Tiene ID?: {tiene_imagen}")
            listo = tiene_imagen

        logger.info(f"[DEBUG] UC: Resultado final de la validación: {listo}")
        logger.info("[DEBUG] UC: ------------------------------------------\n")
        return listo

    def seleccionar_colores_decorado(self, color1: str | None, color2: str | None):
        logger.info(f"[DEBUG] UC: Guardando colores: Color1='{color1}', Color2='{color2}'")
        pedido = self.pedido_repo.obtener()
        pedido.decorado_liso_color1 = color1
        pedido.decorado_liso_color2 = color2
        self.pedido_repo.guardar(pedido)

    def guardar_detalle_decorado(self, tipo_principal: str, detalle: str, texto_tematica: str | None = None):
        logger.info(f"[DEBUG] UC: Guardando detalle: {detalle}, Temática: {texto_tematica}")
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
        logger.info(f"\n[DEBUG] === Iniciando cálculo de rangos para fecha: {fecha_seleccionada} ===")

        horario = self.horario_repo.obtener_horario()
        if not horario:
            logger.info("[DEBUG] No se encontró un horario de entrega en la base de datos.")
            return []

        logger.info(f"[DEBUG] Horario de operación obtenido: {horario.hora_inicio.strftime('%H:%M')} a {horario.hora_fin.strftime('%H:%M')}")

        es_dia_festivo = self.dia_festivo_repo.es_festivo(fecha_seleccionada)

        intervalo_horas = 2 if es_dia_festivo else 1
        logger.info(f"[DEBUG] Intervalo de horas determinado: {intervalo_horas} hora(s)")

        rangos = []
        hora_actual = datetime.datetime.combine(fecha_seleccionada, horario.hora_inicio)
        hora_final = datetime.datetime.combine(fecha_seleccionada, horario.hora_fin)

        logger.info("[DEBUG] --- Generando rangos ---")
        while hora_actual < hora_final:
            hora_siguiente = hora_actual + datetime.timedelta(hours=intervalo_horas)
            if hora_siguiente > hora_final:
                hora_siguiente = hora_final

            rango_str = f"{hora_actual.strftime('%I:%M %p')} - {hora_siguiente.strftime('%I:%M %p')}"
            rangos.append(rango_str)
            logger.info(f"[DEBUG]   - Rango generado: {rango_str}")
            hora_actual = hora_siguiente

        logger.info(f"[DEBUG] === Cálculo finalizado. Se generaron {len(rangos)} rangos. ===\n")
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
        logger.info(f"INFO: Forma '{nombre_forma}' seleccionada. Estado del pedido: {pedido}")

    def obtener_precio_pastel_configurado(self) -> PastelConfigurado:
        pedido = self.pedido_repo.obtener()

        logger.info("\n[DEBUG] === Consultando Precio de Pastel Configurado ===")
        logger.info(f"[DEBUG] ID Categoría: {pedido.id_categoria}")
        logger.info(f"[DEBUG] ID Pan: {pedido.id_pan}")
        logger.info(f"[DEBUG] ID Forma: {pedido.id_forma}")
        logger.info(f"[DEBUG] ID Tamaño: {pedido.id_tamano}")

        if not all([pedido.id_categoria, pedido.id_pan, pedido.id_forma, pedido.id_tamano]):
            logger.info("[DEBUG] Faltan IDs para calcular el precio. Devolviendo 0.0")
            logger.info("[DEBUG] =============================================\n")
            return 0.0

        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        if config:
            logger.info(f"[DEBUG] Precio=${config.precio_base}, Precio Chocolate=${config.precio_chocolate}, Depósito=${config.monto_deposito}")
        else:
            logger.info("[DEBUG] No se encontró una configuración de pastel para esos IDs.")
        logger.info("[DEBUG] =============================================\n")

        precio_pastel = config.precio_base if config else 0.0
        precio_chocolate = config.precio_chocolate if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0
        peso_pastel = config.peso_pastel if config else ""
        medidas_pastel = config.medidas_pastel if config else ""
        incluye = config.incluye if config else ""

        if pedido.tipo_cobertura and "fondant" in pedido.tipo_cobertura.lower():
            logger.info(f"INFO: Cobertura de Fondant detectada. Duplicando precio base de ${precio_pastel}.")
            precio_pastel *= 2
            precio_chocolate *= 2

        extra_costo = pedido.extra_precio or 0.0
        total = precio_pastel + extra_costo

        pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.precio_chocolate = precio_chocolate
        pedido.total = total
        pedido.tamano_peso = peso_pastel
        pedido.tamano_descripcion = medidas_pastel
        pedido.incluye = incluye

        self.pedido_repo.guardar(pedido)

        return config

    def guardar_mensaje_y_edad(self, mensaje: str | None, edad: int | None):
        pedido = self.pedido_repo.obtener()
        pedido.mensaje_pastel = mensaje
        pedido.edad_pastel = edad
        self.pedido_repo.guardar(pedido)

    def reiniciar_mensaje_y_edad(self):
        pedido = self.pedido_repo.obtener()
        pedido.mensaje_pastel = None
        pedido.edad_pastel = None
        self.pedido_repo.guardar(pedido)

    def obtener_detalles_decorado_disponibles(self) -> list[dict]:
        """
        Devuelve la lista de opciones de detalle de decorado, aplicando las reglas
        de negocio basadas en la cobertura seleccionada.
        """
        pedido = self.pedido_repo.obtener()
        cobertura_seleccionada = pedido.tipo_cobertura.lower() if pedido.tipo_cobertura else ""

        # Opciones de detalle por defecto
        detalles = [
            {"nombre": "Chantilli", "imagen": "/assets/decorado/chantilli.png"},
            {"nombre": "Chorreado", "imagen": "/assets/decorado/chorreado.png"},
            {"nombre": "Diseño o Temática", "imagen": "/assets/decorado/tematica.png"},
        ]

        # --- APLICACIÓN DE REGLAS DE NEGOCIO ---

        # Regla 1: Si la cobertura es "chantilly", se oculta la opción de decorado "Chantilli"
        if "chantilly" in cobertura_seleccionada:
            print("[DEBUG] UC: Aplicando regla de CHANTILLY. Ocultando opción redundante.")
            detalles = [d for d in detalles if d["nombre"] != "Chantilli"]

        # Regla 2: Si la cobertura es "chorreado", no hay opciones de detalle
        if "chorreado" in cobertura_seleccionada:
            print("[DEBUG] UC: Aplicando regla de CHORREADO. No hay sub-opciones de decorado.")
            return []  # Devuelve una lista vacía

        return detalles


class FinalizarPedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, finalizar_repo: FinalizarPedidoRepository,
                 pastel_config_repo: PastelConfiguradoRepository, extra_repo: ExtraRepository, categoria_repo: CategoriaRepository):
        self.pedido_repo = pedido_repo
        self.finalizar_repo = finalizar_repo
        self.pastel_config_repo = pastel_config_repo
        self.extra_repo = extra_repo
        self.categoria_repo = categoria_repo
        self.printing_service = PrintingService()

    def obtener_nombre_categoria(self, id_categoria: int) -> str:
        categoria = self.categoria_repo.obtener_por_id(id_categoria)
        return categoria.nombre if categoria else "Desconocida"

    def finalizar_y_obtener_ticket(self) -> Ticket | None:
        pedido = self.pedido_repo.obtener()

        config = self.pastel_config_repo.obtener_configuracion(
            id_cat=pedido.id_categoria,
            id_pan=pedido.id_pan,
            id_forma=pedido.id_forma,
            id_tam=pedido.id_tamano
        )

        precio_pastel = config.precio_base if config else 0.0
        precio_chocolate = config.precio_chocolate if config else 0.0
        monto_deposito = config.monto_deposito if config else 0.0
        peso_pastel = config.peso_pastel if config else ""
        medidas_pastel = config.medidas_pastel if config else ""

        if pedido.tipo_cobertura and "fondant" in pedido.tipo_cobertura.lower():
            logger.info(f"INFO: Cobertura de Fondant detectada. Duplicando precio base de ${precio_pastel}.")
            precio_pastel *= 2
            precio_chocolate *= 2

        extra_costo = pedido.extra_precio or 0.0
        if pedido.extra_seleccionado == "Flor Artificial" and pedido.extra_flor_cantidad:
            extra_costo *= pedido.extra_flor_cantidad

        total = precio_pastel + extra_costo

        if pedido.id_pan == 2 and precio_chocolate > 0:
            pedido.precio_pastel = precio_chocolate
        else:
            pedido.precio_pastel = precio_pastel
        pedido.monto_deposito = monto_deposito
        pedido.extra_costo = extra_costo
        pedido.total = total

        pedido.tamano_peso = peso_pastel
        pedido.tamano_descripcion = medidas_pastel

        id_nuevo_pedido = self.finalizar_repo.guardar(pedido)
        if id_nuevo_pedido:
            return self.finalizar_repo.obtener_por_id(id_nuevo_pedido)
        return None
