# src/infrastructure/persistence/sqlite_repository.py
import sqlite3
import datetime
from src.domain.pedido import Pedido
from src.application.repositories import (
    TamanoRepository, CategoriaRepository, TipoPanRepository,
    TipoFormaRepository, TipoRellenoRepository, TipoCoberturaRepository,
    FinalizarPedidoRepository, FormaPastel, TipoRelleno, TipoCobertura,
    Categoria, TipoPan, ImagenGaleriaRepository, ImagenGaleria, TipoColorRepository
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
                # El resultado es una lista de tuplas, ej: [('Chico',), ('Mediano',)]
                # Lo convertimos a una lista de strings.
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

    def finalizar(self, pedido: Pedido):
        """Inserta el pedido completo en la tabla 'pedidos' de la base de datos."""
        query = """
            INSERT INTO pedidos (
                fecha_creacion, fecha_entrega, tamano_pastel, id_categoria, tipo_pan, 
                tipo_forma, tipo_relleno, tipo_cobertura, mensaje_pastel, tipo_decorado,
                decorado_liso_detalle, decorado_liso_color, decorado_tematica_detalle,
                decorado_imagen_id, extra_seleccionado, decorado_liso_color1, decorado_liso_color2, 
                nombre_completo, telefono, direccion, numero_exterior, entre_calles, codigo_postal, colonia,
                ciudad, municipio, estado, referencias 
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Preparamos los datos en una tupla, en el orden correcto
        datos = (
            datetime.datetime.now().isoformat(),
            pedido.fecha_entrega.isoformat() if pedido.fecha_entrega else None,
            pedido.tamano_pastel,
            pedido.id_categoria,
            pedido.tipo_pan,
            pedido.tipo_forma,
            pedido.tipo_relleno,
            pedido.tipo_cobertura,
            pedido.mensaje_pastel,
            pedido.tipo_decorado,
            pedido.decorado_liso_detalle,
            pedido.decorado_liso_color,
            pedido.decorado_tematica_detalle,
            pedido.decorado_imagen_id,
            pedido.extra_seleccionado,
            pedido.decorado_liso_color1,
            pedido.decorado_liso_color2,
            # Datos de entrega (si existen)
            pedido.datos_entrega.nombre_completo if pedido.datos_entrega else None,
            pedido.datos_entrega.telefono if pedido.datos_entrega else None,
            pedido.datos_entrega.direccion if pedido.datos_entrega else None,
            pedido.datos_entrega.numero_exterior if pedido.datos_entrega else None,
            pedido.datos_entrega.entre_calles if pedido.datos_entrega else None,
            pedido.datos_entrega.codigo_postal if pedido.datos_entrega else None,
            pedido.datos_entrega.colonia if pedido.datos_entrega else None,
            pedido.datos_entrega.ciudad if pedido.datos_entrega else None,
            pedido.datos_entrega.municipio if pedido.datos_entrega else None,
            pedido.datos_entrega.estado if pedido.datos_entrega else None,
            pedido.datos_entrega.referencias if pedido.datos_entrega else None,
        )

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, datos)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al guardar el pedido final en la base de datos: {e}")


class ImagenGaleriaRepositorySQLite(ImagenGaleriaRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def buscar(self, categoria: str | None = None, termino: str | None = None) -> list[ImagenGaleria]:
        """Busca imágenes en la BD con filtros dinámicos."""
        base_query = "SELECT id_imagen, url_imagen, descripcion, categoria_imagen, tags FROM imagenes_galeria"
        conditions = []
        params = []

        if categoria:
            conditions.append("categoria_imagen = ?")
            params.append(categoria)

        if termino:
            # Busca en la descripción o en los tags
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
        """Ejecuta una consulta SQL para encontrar una imagen por su ID."""
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
        # Primero necesitamos el ID de la cobertura a partir de su nombre
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
                    return []  # No se encontró la cobertura

                id_cobertura = id_cobertura_row[0]
                cursor.execute(query_colores, (id_categoria, id_cobertura))
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al leer los colores por cobertura: {e}")
            return []
