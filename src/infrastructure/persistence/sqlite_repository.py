# src/infrastructure/persistence/sqlite_repository.py
import sqlite3
import datetime
from src.domain.pedido import Pedido
from src.application.repositories import (
    TamanoRepository, CategoriaRepository, TipoPanRepository,
    TipoFormaRepository, TipoRellenoRepository, TipoCoberturaRepository,
    FinalizarPedidoRepository, FormaPastel, TipoRelleno, TipoCobertura,
    Categoria, TipoPan, ImagenGaleriaRepository, ImagenGaleria, TipoColorRepository, Ticket
)


class CategoriaRepositorySQLite(CategoriaRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_todas(self) -> list[Categoria]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_categoria, nombre_categoria, imagen_url FROM categorias ORDER BY id_categoria")
                # Convertimos las filas de la BD en objetos Categoria
                return [Categoria(id=row[0], nombre=row[1], imagen_url=row[2]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer la tabla de categorías: {e}")
            return []


class TipoPanRepositorySQLite(TipoPanRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        query = """
            SELECT tp.id_tipo_pan, tp.nombre_tipo_pan, ctd.imagen_quiosco  
            FROM categoria_tipos_pan_disponibles ctd, tipos_pan tp 
            WHERE ctd.id_tipo_pan = tp.id_tipo_pan AND ctd.id_categoria = ?
            ORDER BY tp.nombre_tipo_pan
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_categoria,))
                return [TipoPan(id=row[0], nombre=row[1], imagen_url=row[2]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los tipos de pan por categoría: {e}")
            return []


class TipoFormaRepositorySQLite(TipoFormaRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_por_categoria(self, id_categoria: int) -> list[FormaPastel]:
        query = """
            SELECT tf.nombre_tipo_forma, ctfd.imagen_quiosco  
            FROM categoria_tipos_forma_disponibles ctfd, tipos_forma tf 
            WHERE ctfd.id_tipo_forma = tf.id_tipo_forma AND ctfd.id_categoria = ?
            ORDER BY tf.nombre_tipo_forma
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_categoria,))
                return [FormaPastel(nombre=row[0], imagen_url=row[1]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los tipos de forma por categoría: {e}")
            return []

class TamanoRepositorySQLite(TamanoRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_todos(self) -> list[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nombre_tamano FROM tipos_tamano ORDER BY id_tipo_tamano")
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer la base de datos: {e}")
            return []


class TipoRellenoRepositorySQLite(TipoRellenoRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[TipoRelleno]:
        query = """
            SELECT tr.nombre_tipo_relleno, ctrd.imagen_quiosco 
            FROM categoria_tipos_relleno_disponibles ctrd, tipos_relleno tr 
            WHERE ctrd.id_tipo_relleno = tr.id_tipo_relleno 
            AND ctrd.id_categoria = ? AND ctrd.id_tipo_pan = ?
            ORDER BY tr.nombre_tipo_relleno
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_categoria, id_tipo_pan))
                return [TipoRelleno(nombre=row[0], imagen_url=row[1]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los tipos de relleno: {e}")
            return []


class TipoCoberturaRepositorySQLite(TipoCoberturaRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[TipoCobertura]:
        query = """
            SELECT tc.nombre_tipo_cobertura, ctcd.imagen_quiosco 
            FROM categoria_tipos_cobertura_disponibles ctcd, tipos_cobertura tc 
            WHERE ctcd.id_tipo_cobertura = tc.id_tipo_cobertura AND ctcd.id_categoria = ? AND ctcd.id_tipo_pan = ?
            ORDER BY tc.nombre_tipo_cobertura
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_categoria, id_tipo_pan))
                return [TipoCobertura(nombre=row[0], imagen_url=row[1]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los tipos de cobertura por categoría: {e}")
            return []


class FinalizarPedidoRepositorySQLite(FinalizarPedidoRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def guardar(self, pedido: Pedido) -> int:

        query = """
                INSERT INTO pedidos (fecha_creacion, fecha_entrega, hora_entrega, tamano_pastel, id_categoria, tipo_pan, \
                                     tipo_forma, tipo_relleno, tipo_cobertura, mensaje_pastel, tipo_decorado, \
                                     decorado_liso_detalle, decorado_tematica_detalle, decorado_imagen_id, \
                                     decorado_liso_color1, decorado_liso_color2, extra_seleccionado, \
                                     extra_flor_cantidad, nombre_completo, telefono, direccion, \
                                     numero_exterior, entre_calles, codigo_postal, colonia, ciudad, municipio, estado, \
                                     referencias, decorado_liso_color) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) \
                """

        datos = (
            datetime.datetime.now().isoformat(),
            pedido.fecha_entrega,
            pedido.hora_entrega,
            pedido.tamano_pastel,
            pedido.id_categoria,
            pedido.tipo_pan,
            pedido.tipo_forma,
            pedido.tipo_relleno,
            pedido.tipo_cobertura,
            pedido.mensaje_pastel,
            pedido.tipo_decorado,
            pedido.decorado_liso_detalle,
            pedido.decorado_tematica_detalle,
            pedido.decorado_imagen_id,
            pedido.decorado_liso_color1,
            pedido.decorado_liso_color2,
            pedido.extra_seleccionado,
            pedido.extra_flor_cantidad,
            pedido.nombre_cliente,
            pedido.telefono_cliente,
            pedido.direccion_cliente,
            pedido.num_ext_cliente,
            pedido.entre_calles_cliente,
            pedido.cp_cliente,
            pedido.colonia_cliente,
            pedido.ciudad_cliente,
            pedido.municipio_cliente,
            pedido.estado_cliente,
            pedido.referencias_cliente,
            pedido.decorado_liso_color,
        )

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, datos)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al guardar el pedido final en la base de datos: {e}")
            return 0

    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        query = """SELECT id_pedido, id_categoria, tipo_pan, tipo_forma, tipo_relleno, tipo_cobertura, 
                          tamano_pastel, fecha_entrega, hora_entrega, nombre_completo, telefono, direccion, 
                          numero_exterior, codigo_postal, colonia, ciudad, estado, fecha_creacion, entre_calles, 
                          municipio, referencias, decorado_liso_color1, decorado_liso_color2, mensaje_pastel, 
                          extra_flor_cantidad, tipo_decorado, decorado_liso_detalle, decorado_liso_color, 
                          decorado_tematica_detalle, decorado_imagen_id, extra_seleccionado
                   FROM pedidos WHERE id_pedido = ?"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_pedido,))
                row = cursor.fetchone()
                if row:
                    return Ticket(id_pedido=row[0],
                                  id_categoria=row[1],
                                  tipo_pan=row[2],
                                  tipo_forma=row[3],
                                  tipo_relleno=row[4],
                                  tipo_cobertura=row[5],
                                  tamano_pastel=row[6],
                                  fecha_entrega=row[7],
                                  hora_entrega=row[8],
                                  nombre_cliente=row[9],
                                  telefono_cliente=row[10],
                                  direccion_cliente=row[11],
                                  num_ext_cliente=row[12],
                                  cp_cliente=row[13],
                                  colonia_cliente=row[14],
                                  ciudad_cliente=row[15],
                                  estado_cliente=row[16],
                                  fecha_creacion=row[17],
                                  entre_calles_cliente=row[18],
                                  municipio_cliente=row[19],
                                  referencias_cliente=row[20],
                                  decorado_liso_color=row[27],
                                  decorado_liso_color1=row[21],
                                  decorado_liso_color2=row[22],
                                  mensaje_pastel=row[23],
                                  extra_flor_cantidad=row[24],
                                  tipo_decorado=row[25],
                                  decorado_liso_detalle=row[26],
                                  decorado_tematica_detalle=row[28],
                                  decorado_imagen_id=row[29],
                                  extra_seleccionado=row[30],)
        except sqlite3.Error as e:
            print(f"Error al obtener el pedido por ID: {e}")
        return None


class ImagenGaleriaRepositorySQLite(ImagenGaleriaRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def buscar(self, categoria: str | None = None, termino: str | None = None) -> list[ImagenGaleria]:
        base_query = "SELECT id_imagen, url_imagen, descripcion, categoria_imagen, tags FROM imagenes_galeria"
        conditions = []
        params = []

        if categoria:
            conditions.append("categoria_imagen = ?")
            params.append(categoria)

        if termino:
            conditions.append("(descripcion LIKE ? OR tags LIKE ?)")
            params.extend([f"%{termino}%", f"%{termino}%"])

        if conditions:
            query = f"{base_query} WHERE {' AND '.join(conditions)}"
        else:
            query = base_query

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [ImagenGaleria(id=row[0], url=row[1], descripcion=row[2], categoria=row[3], tags=row[4]) for row
                        in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al buscar en la galería de imágenes: {e}")
            return []

    def obtener_por_id(self, id_imagen: int) -> ImagenGaleria | None:
        query = "SELECT id_imagen, url_imagen, descripcion, categoria_imagen, tags FROM imagenes_galeria WHERE id_imagen = ?"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_imagen,))
                row = cursor.fetchone()
                if row:
                    return ImagenGaleria(id=row[0], url=row[1], descripcion=row[2], categoria=row[3], tags=row[4])
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener imagen por ID: {e}")
            return None


class TipoColorRepositorySQLite(TipoColorRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def obtener_por_categoria_y_cobertura(self, id_categoria: int, nombre_cobertura: str) -> list[str]:
        query_id = "SELECT id_tipo_cobertura FROM tipos_cobertura WHERE nombre_tipo_cobertura = ?"

        query_colores = """
                        SELECT TC.nombre_tipo_color \
                        FROM categorias_tipos_cobertura_colores CTCC, \
                             tipos_colores TC
                        WHERE CTCC.id_tipo_color = TC.id_tipo_color \
                          AND CTCC.id_categoria = ? \
                          AND CTCC.id_tipo_cobertura = ?
                        ORDER BY TC.nombre_tipo_color \
                        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query_id, (nombre_cobertura,))
                id_cobertura_row = cursor.fetchone()
                if not id_cobertura_row:
                    return []

                id_cobertura = id_cobertura_row[0]
                cursor.execute(query_colores, (id_categoria, id_cobertura))
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los colores por cobertura: {e}")
            return []





