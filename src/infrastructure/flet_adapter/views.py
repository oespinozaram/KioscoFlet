# src/infrastructure/flet_adapter/views.py
import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
from src.application.use_cases import PedidoUseCases
from .keyboard import VirtualKeyboard
from .controles_comunes import crear_boton_navegacion


# --- Vista de Bienvenida ---
def vista_bienvenida(page: ft.Page):
    """
    Crea la vista de bienvenida con un diseño responsivo, adaptando
    los elementos a diferentes tamaños de pantalla.
    """

    # --- Contenido de la pantalla ---

    # El banner superior se adapta al ancho y centra su texto.
    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        padding=15,
        alignment=ft.alignment.center, # Centra el texto horizontalmente
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE,
            size=24,
            font_family="Bebas Neue",
        )
    )

    # La imagen del pastel, que será parte del flujo responsivo.
    imagen_pastel = ft.Image(
        src="Logo Pepe.png",
        fit=ft.ImageFit.CONTAIN,
        height=250,  # Altura máxima para la imagen
    )

    # Textos principales
    texto_bienvenida = ft.Text(
        '¡ Bienvenido a nuestra pastelería !',
        color=ft.Colors.WHITE,
        size=50,  # Ajustamos el tamaño para que se vea bien en móviles
        font_family="Bebas Neue",
        text_align=ft.TextAlign.CENTER,
        opacity=0.90,
    )

    texto_subtitulo = ft.Text(
        'Disfruta de nuestra amplia variedad de pasteles o si lo prefieres\nármalo y personalízalo a tu gusto.',
        color=ft.Colors.WHITE,
        size=22,  # Tamaño ajustado
        font_family="Bebas Neue",
        text_align=ft.TextAlign.CENTER,
        opacity=0.80,
    )

    # Botón para comenzar
    boton_comenzar = ft.Container(
        bgcolor="#DC6262",
        border_radius=ft.border_radius.all(20),
        padding=ft.padding.symmetric(vertical=15, horizontal=40),
        content=ft.Text(
            'comenzar',
            color=ft.Colors.WHITE,
            size=36,
            font_family="Bebas Neue",
        ),
        on_click=lambda _: page.go("/seleccion")
    )

    # El contenido que irá por encima del fondo.
    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),  # Espaciador flexible para empujar el contenido
            ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        # Esta columna contendrá el contenido principal
                        # y su ancho se ajustará según el tamaño de la pantalla.
                        col={"sm": 11, "md": 8, "lg": 6},
                        controls=[
                            imagen_pastel,
                            texto_bienvenida,
                            texto_subtitulo,
                            ft.Container(height=20),  # Espacio
                            boton_comenzar,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    )
                ]
            ),
            ft.Container(expand=True),  # Espaciador flexible
        ]
    )

    # Usamos Stack para el fondo y el contenido superpuesto.
    layout_final = ft.Stack(
        controls=[
            # Capa 1: Imagen de fondo
            ft.Image(
                src="fondo.png",
                fit=ft.ImageFit.FILL,
                expand=True,
            ),
            # Capa 2: Filtro oscuro
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.50, ft.Colors.BLACK),
                expand=True,
            ),
            # Capa 3: contenido interactivo
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/",
        controls=[
            layout_final
        ],
        padding=0,
    )


def vista_seleccion(page: ft.Page):
    """
    Muestra las dos opciones principales usando el mismo patrón de diseño
    responsivo que la pantalla de bienvenida.
    """

    # --- Componente reutilizable para las tarjetas de opción (sin cambios) ---
    def crear_tarjeta_opcion(titulo: str, imagen_src: str, on_click_handler):
        return ft.Container(
            col={"sm": 12, "md": 5},
            height=300,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(40),
            shadow=ft.BoxShadow(
                spread_radius=2, blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(6, 6)
            ),
            content=ft.Column(
                [
                    ft.Container(
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        expand=2,
                        content=ft.Image(src=imagen_src, fit=ft.ImageFit.COVER),
                        border_radius=ft.border_radius.only(top_left=40, top_right=40),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    ),
                    ft.Container(
                        expand=1,
                        alignment=ft.alignment.center,
                        padding=10,
                        content=ft.Text(titulo, text_align=ft.TextAlign.CENTER, size=24, font_family="Be Vietnam Pro")
                    )
                ]
            ),
            on_click=on_click_handler,
            on_hover=lambda e: setattr(
                e.control,
                "shadow",
                ft.BoxShadow(
                    spread_radius=5,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.5,
                                                 "#DC6262")
                ) if e.data == "true" else ft.BoxShadow(
                spread_radius=2, blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(6, 6))) or page.update()
        )

    # --- Contenido principal ---
    # Se mantiene el ResponsiveRow para que las tarjetas se coloquen horizontalmente
    contenido_principal = ft.ResponsiveRow(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
        controls=[
            crear_tarjeta_opcion(
                titulo="Conoce nuestro catálogo\ny promociones",
                imagen_src="seleccion/promos.png",
                on_click_handler=lambda _: print("Navegando a promociones...")
            ),
            crear_tarjeta_opcion(
                titulo="Arma y personaliza\ntu pastel",
                imagen_src="seleccion/arma.png",
                on_click_handler=lambda _: page.go("/fecha")
            ),
        ]
    )

    # Banner superior
    banner_superior = ft.Container(
        bgcolor="#89C5B0", padding=15, alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=24,
                        font_family="Bebas Neue")
    )

    # La imagen del pastel, que será parte del flujo responsivo.
    imagen_pastel = ft.Image(
        src="Logo Pepe.png",
        fit=ft.ImageFit.CONTAIN,
        height=180,  # Altura máxima para la imagen
    )

    # Botón para volver
    boton_volver = crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/"),
                            es_primario=False
                        )
    #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/"))

    # --- CAMBIO PRINCIPAL: Se aplica el mismo patrón de layout que en bienvenida ---
    # Usamos una Columna con espaciadores para centrar verticalmente el contenido.
    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),  # Espaciador flexible superior
            imagen_pastel,
            ft.Container(expand=True),
            contenido_principal,  # El ResponsiveRow con las tarjetas
            ft.Container(height=40),  # Espacio fijo
            boton_volver,  # Botón de volver
            ft.Container(height=40),  # Espacio fijo
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # El Stack final para el fondo y el contenido
    layout_final = ft.Stack(
        controls=[
            ft.Image(src="fondos/fondo2.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/seleccion",
        controls=[layout_final],
        padding=0
    )

def vista_fecha(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Lógica y Manejadores de Eventos (Sin cambios) ---
    texto_del_boton = ft.Text(
        value=f"Fecha: {use_cases.obtener_pedido_actual().fecha_entrega.strftime('%d/%m/%Y')}" if use_cases.obtener_pedido_actual().fecha_entrega else "Elige la fecha de entrega",
        color=ft.Colors.WHITE, size=40, font_family="Bebas Neue", weight=ft.FontWeight.W_400,
    )
    #boton_continuar = ft.ElevatedButton("Continuar", disabled=not use_cases.obtener_pedido_actual().fecha_entrega)
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_date_change(e):
        fecha_seleccionada = e.control.value.date()
        use_cases.seleccionar_fecha(fecha_seleccionada)
        texto_del_boton.value = f"Fecha: {fecha_seleccionada.strftime('%d/%m/%Y')}"
        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False
        page.update()

    fecha_hoy = datetime.date.today()
    fecha_inicial_valida = fecha_hoy + datetime.timedelta(days=4)
    fecha_final_valida = fecha_hoy + relativedelta(months=+6)

    def open_date_picker(e):
        page.open(
            ft.DatePicker(
                first_date=fecha_inicial_valida, last_date=fecha_final_valida,
                on_change=on_date_change,
                value=use_cases.obtener_pedido_actual().fecha_entrega or fecha_inicial_valida
            )
        )

    def continuar(e):
        if not use_cases.obtener_pedido_actual().fecha_entrega:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona una fecha para continuar."),
                                         bgcolor=ft.Colors.RED_ACCENT_700)
            page.snack_bar.open = True
            page.update()
        else:
            page.go("/tamano")

    #boton_continuar.on_click = continuar

    # --- 2. Construcción de los Componentes ---
    banner_superior = ft.Container(
        bgcolor="#89C5B0", padding=15, alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=24,
                        font_family="Bebas Neue")
    )

    boton_fecha = ft.Container(
        width=480, height=100, bgcolor="#89C5B0", border_radius=ft.border_radius.all(20),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                            offset=ft.Offset(4, 4)),
        content=texto_del_boton, alignment=ft.alignment.center,
        on_click=open_date_picker,
        animate_scale=ft.Animation(600, ft.AnimationCurve.EASE_OUT_BACK)
    )

    panel_derecho = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(20),
        padding=30,
        content=ft.Column(
            [
                # ft.Text("Paso 1", size=20, color=ft.Colors.BLACK),
                ft.Text("Fecha de Entrega", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK,
                        font_family="Bebas Neue"),
                ft.Container(expand=True),
                boton_fecha,
                ft.Container(expand=True),
                ft.Row(
                    [
                        #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/seleccion")),
                        crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/seleccion"),
                            es_primario=False
                        ),
                        crear_boton_navegacion(
                            texto="Continuar",
                            on_click_handler=continuar,
                            ref=ref_boton_continuar,  # Le pasamos la referencia
                            disabled=not use_cases.obtener_pedido_actual().fecha_entrega  # Estado inicial
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
    )

    # El contenido principal ahora es una Fila
    contenido_principal = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Image(src="Logo Pepe.png", fit=ft.ImageFit.CONTAIN, expand=1),
            ft.Container(content=panel_derecho, expand=1, padding=20)
        ]
    )

    # --- 3. Construcción del Layout Final ---
    # Se aplica el mismo patrón que en la vista de bienvenida.
    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),  # Espaciador flexible
            contenido_principal,  # Contenido centrado
            ft.Container(expand=True),  # Espaciador flexible
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(
                src="fondo.png",
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            # Usamos un filtro de color rojo semitransparente, como en tu diseño original
            ft.Container(bgcolor=ft.Colors.with_opacity(0.2, "#DC6262"), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/fecha",
        controls=[layout_final],
        padding=0
    )

def vista_tamano(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Lógica y Manejadores de Eventos (Sin cambios) ---
    use_cases.obtener_tamanos()
    pedido_actual = use_cases.obtener_pedido_actual()

    texto_tamano = ft.Text(
        value=pedido_actual.tamano_pastel or "N/A",
        size=48,
        font_family="Bebas Neue",
        color="#623F19",
        text_align=ft.TextAlign.CENTER
    )

    def anterior(e):
        use_cases.seleccionar_anterior_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    def siguiente(e):
        use_cases.seleccionar_siguiente_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    # --- 2. Construcción de los Componentes ---

    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        height=67,
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE,
            size=36,
            font_family="Bebas Neue",
        )
    )

    panel_interactivo = ft.Container(
        width=660,
        height=404,
        margin=100,
        bgcolor=ft.Colors.with_opacity(0.90, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(50),
        shadow=ft.BoxShadow(
            spread_radius=8, blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(4, 4),
        ),
        padding=10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    '¿Para cuántas personas es tu pastel?',
                    size=42,
                    font_family="Bebas Neue",
                    color="#815E43",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.Container(
                    width=333,
                    height=95,
                    border=ft.border.all(5, color=ft.Colors.with_opacity(0.77, "#623F19")),
                    border_radius=ft.border_radius.all(20),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=anterior),
                            ft.Container(content=texto_tamano, expand=True, alignment=ft.alignment.center),
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, icon_size=40, on_click=siguiente),
                        ]
                    )
                ),
                ft.Container(height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/fecha")),
                        crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/fecha"),
                            es_primario=False
                        ),
                        crear_boton_navegacion(
                            texto="Continuar",
                            on_click_handler=lambda _: page.go("/categorias")
                        ),
                    ]
                ),
            ]
        )
    )

    contenido_principal = ft.ResponsiveRow(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,  # Centra las columnas horizontalmente
        controls=[
            # Columna 1: Contiene la imagen y el panel interactivo.
            ft.Column(
                col={"sm": 12, "md": 6},
                # --- CLAVE DEL CENTRADO VERTICAL ---
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Image(
                        src="Logo Pepe 50.png",
                        fit=ft.ImageFit.CONTAIN,
                        height=250
                    ),
                    panel_interactivo,
                ]
            ),

            # Columna 2: Ahora es un Container para mejor control del centrado.
            ft.Container(
                col={"sm": 12, "md": 6},
                alignment=ft.alignment.center,  # Centra la imagen dentro de la columna
                content=ft.Image(
                    src="https://placehold.co/813x1117",
                    fit=ft.ImageFit.COVER,
                    height=600,
                    border_radius=ft.border_radius.all(20)
                )
            )
        ]
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),
            contenido_principal,
            ft.Container(expand=True),
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="Sin título-2_Mesa de trabajo 1.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.2, "#DC6262"), expand=True),
            ft.Row(
                controls=[ft.Container(bgcolor=ft.Colors.with_opacity(0.3, "#DC6262"), expand=1) for _ in range(8)],
                spacing=10,
                expand=True
            ),
            ft.Image(
                src="5cfc8f887f97645860409428bc94c92cd53abcd4.png",
                fit=ft.ImageFit.COVER,
                height=page.window.height,
                top=0,
                right=0,
            ),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.17, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/tamano",
        controls=[layout_final],
        padding=0
    )


def vista_categorias(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Lógica y Manejadores de Eventos ---
    # La lógica para obtener y seleccionar categorías no cambia.

    def seleccionar_y_avanzar(id_categoria: int):
        use_cases.seleccionar_categoria(id_categoria)
        page.go("/relleno")

    # --- 2. Construcción de los Componentes ---

    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        height=67,
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE,
            size=36,
            font_family="Bebas Neue",
        )
    )

    # Creamos las tarjetas interactivas para cada categoría
    lista_categorias = use_cases.obtener_categorias()
    tarjetas_categorias = []

    for categoria in lista_categorias:
        tarjeta = ft.Container(
            width=226,
            height=314,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(30),
            shadow=ft.BoxShadow(
                spread_radius=2, blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(6, 6)
            ),
            on_click=lambda _, cat_id=categoria.id: seleccionar_y_avanzar(cat_id),
            content=ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=176,
                        height=119,
                        margin=ft.margin.only(top=25),
                        border_radius=ft.border_radius.all(10),
                        # Puedes añadir imágenes a tus categorías en la BD y cargarlas aquí
                        content=ft.Image(src="categorias/{}".format(categoria.imagen_url), fit=ft.ImageFit.COVER)
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Text(
                        categoria.nombre,
                        text_align=ft.TextAlign.CENTER,
                        size=20,
                        font_family="Bebas Neue"
                    ),
                    ft.Container(
                        width=105,
                        height=23,
                        bgcolor="#E5ADAD",
                        border_radius=ft.border_radius.all(5),
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            "Seleccionar",
                            color=ft.Colors.WHITE,
                            size=16,
                            font_family="Bebas Neue"
                        )
                    )
                ]
            )
        )
        tarjetas_categorias.append(tarjeta)

    # --- 3. Construcción del Layout Final ---

    # El contenido principal es una fila responsiva que mostrará las tarjetas
    contenido_principal = ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                col={"sm": 12},
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True,  # Permite que las tarjetas se ajusten en varias líneas
                spacing=30,
                run_spacing=30,
                controls=tarjetas_categorias
            )
        ]
    )

    # La columna que centra el contenido verticalmente
    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True, content=contenido_principal),
            ft.Container(  # Espacio para el botón de volver
                padding=20,
                alignment=ft.alignment.center,
                content=crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/tamano"),
                            es_primario=False
                        )
            )
        ]
    )

    # El Stack final que une todas las capas visuales
    layout_final = ft.Stack(
        controls=[
            ft.Image(src="fondo_rr.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.2, "#DC6262"), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/categorias",
        controls=[layout_final],
        padding=0
    )

# def vista_relleno(page: ft.Page, use_cases: PedidoUseCases):
#     # --- 1. Lógica y Manejadores de Eventos ---
#     def check_continuar():
#         pedido = use_cases.obtener_pedido_actual()
#         if pedido.tipo_forma and pedido.tipo_pan and pedido.tipo_relleno:
#             boton_continuar.visible = True
#             page.update()
#
#     def on_relleno_selected(e):
#         # El 'data' de la tarjeta de relleno es solo el nombre.
#         use_cases.seleccionar_tipo_relleno(e.control.data)
#         for card in relleno_cards.controls:
#             card.visible = (card == e.control) # Solo al control que se dio click es visible
#             card.border = ft.border.all(2, ft.Colors.GREEN) if card.visible else None
#         check_continuar()
#         page.update()
#
#     def on_pan_selected(e):
#         # --- CAMBIO IMPORTANTE: Desempacamos el ID y el nombre desde 'data' ---
#         id_pan_seleccionado, nombre_pan_seleccionado = e.control.data
#
#         use_cases.seleccionar_tipo_pan(nombre_pan_seleccionado)
#         for card in pan_cards.controls:
#             card.visible = (card == e.control)
#             card.border = ft.border.all(2, ft.Colors.GREEN) if card.visible else None
#
#         relleno_cards.controls.clear()
#         id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria
#         lista_rellenos = use_cases.obtener_rellenos_disponibles(id_categoria_actual, id_pan_seleccionado)
#
#         if not lista_rellenos:
#             relleno_cards.controls.append(ft.Text("No hay rellenos para esta combinación."))
#         else:
#             for relleno in lista_rellenos:
#                 relleno_cards.controls.append(
#                     crear_tarjeta_seleccion(
#                         relleno.nombre,
#                         "rellenos/{}".format(relleno.imagen_url),
#                         on_relleno_selected
#                     )
#                 )
#
#         seccion_rellenos.visible = True
#         check_continuar()
#         page.update()
#
#     def on_forma_selected(e):
#         # El 'data' de la tarjeta de forma es solo el nombre.
#         use_cases.seleccionar_tipo_forma(e.control.data)
#         for card in forma_cards.controls:
#             card.visible = (card == e.control)
#             card.border = ft.border.all(2, ft.Colors.GREEN) if card.visible else None
#         seccion_panes.visible = True
#         check_continuar()
#         page.update()
#
#     def restablecer_selecciones(e):
#         # Limpiamos el estado en la lógica de negocio
#         use_cases.reiniciar_componentes()
#
#         # Restauramos la visibilidad y el borde de todos los botones
#         for card in forma_cards.controls:
#             card.visible = True
#             card.border = None
#         for card in pan_cards.controls:
#             card.visible = True
#             card.border = None
#         for card in relleno_cards.controls:
#             card.visible = True
#             card.border = None
#
#         # Ocultamos las secciones dinámicas y el botón de continuar
#         seccion_panes.visible = False
#         seccion_rellenos.visible = False
#         boton_continuar.visible = False
#         page.update()
#
#     # --- 2. Construcción de Componentes ---
#     def crear_tarjeta_seleccion(texto, imagen_src, on_click_handler):
#         return ft.Container(
#             width=226, height=314, bgcolor=ft.Colors.WHITE,
#             border_radius=ft.border_radius.all(30),
#             data=texto,  # Por defecto, 'data' es el texto. Lo sobrescribiremos para los panes.
#             on_click=on_click_handler,
#             content=ft.Column(
#                 spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 controls=[
#                     ft.Container(
#                         width=176, height=119, margin=ft.margin.only(top=25),
#                         border_radius=ft.border_radius.all(10),
#                         content=ft.Image(src=imagen_src, fit=ft.ImageFit.COVER)
#                     ),
#                     ft.Divider(height=2, color=ft.Colors.GREY_300),
#                     ft.Text(texto, text_align=ft.TextAlign.CENTER, size=20, font_family="Bebas Neue"),
#                 ]
#             )
#         )
#
#     id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria
#
#     forma_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)
#
#     for forma in use_cases.obtener_formas_por_categoria(id_categoria_actual):
#         forma_cards.controls.append(crear_tarjeta_seleccion(
#             forma.nombre,
#             "formas/{}".format(forma.imagen_url),
#             on_forma_selected)
#         )
#
#     pan_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)
#     for pan in use_cases.obtener_panes_por_categoria(id_categoria_actual):
#         # --- CAMBIO IMPORTANTE: Pasamos una tupla (id, nombre) a la propiedad 'data' ---
#         tarjeta_pan = crear_tarjeta_seleccion(
#             pan.nombre,
#             "panes/{}".format(pan.imagen_url),
#             on_pan_selected
#         )
#         tarjeta_pan.data = (pan.id, pan.nombre)
#         pan_cards.controls.append(tarjeta_pan)
#
#     relleno_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)
#
#     seccion_formas = ft.Column(
#         [ft.Text("1. Elige la forma", size=25, font_family="Bebas Neue", color="#673C1C"), forma_cards],
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
#     seccion_panes = ft.Column(
#         [ft.Text("2. Elige el pan", size=25, font_family="Bebas Neue", color="#673C1C"), pan_cards],
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, visible=False)
#     seccion_rellenos = ft.Column(
#         [ft.Text("3. Elige el relleno", size=25, font_family="Bebas Neue", color="#673C1C"), relleno_cards],
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, visible=False)
#
#     boton_continuar = ft.ElevatedButton("Elegir Decorado", on_click=lambda _: page.go("/decorado"), visible=False)
#     boton_restablecer = ft.ElevatedButton("Restablecer", on_click=restablecer_selecciones)
#     # --- 3. Construcción del Layout Final (Sin cambios) ---
#     return ft.View(
#         route="/relleno",
#         controls=[
#             ft.Text("Paso 3.1: Componentes del Pastel", size=30, weight=ft.FontWeight.BOLD),
#             seccion_formas,
#             seccion_panes,
#             seccion_rellenos,
#             ft.Divider(height=20),
#             ft.Row(
#                 [
#                     ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
#                     boton_restablecer,
#                     boton_continuar,
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER
#             )
#         ],
#         vertical_alignment=ft.MainAxisAlignment.START,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         spacing=20,
#         padding=20,
#         scroll=ft.ScrollMode.ADAPTIVE
#     )

def vista_relleno(page: ft.Page, use_cases: PedidoUseCases):
    # --- Manejadores de Eventos ---
    def check_continuar():
        pedido = use_cases.obtener_pedido_actual()
        if pedido.tipo_forma and pedido.tipo_pan and pedido.tipo_relleno:
            boton_continuar.visible = True
        else:
            boton_continuar.visible = False
        page.update()

    def on_relleno_selected(e):
        use_cases.seleccionar_tipo_relleno(e.control.data)
        for card in relleno_cards.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None
        check_continuar()
        page.update()

    def on_pan_selected(e):
        id_pan_seleccionado, nombre_pan_seleccionado = e.control.data
        use_cases.seleccionar_tipo_pan(nombre_pan_seleccionado)
        for card in pan_cards.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        seccion_rellenos.visible = False
        relleno_cards.controls.clear()

        id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria
        lista_rellenos = use_cases.obtener_rellenos_disponibles(id_categoria_actual, id_pan_seleccionado)

        if not lista_rellenos:
            relleno_cards.controls.append(ft.Text("No hay rellenos para esta combinación."))
        else:
            for nombre_relleno in lista_rellenos:
                relleno_cards.controls.append(
                    crear_tarjeta_seleccion(nombre_relleno.nombre, "rellenos/{}".format(nombre_relleno.imagen_url),
                                            on_relleno_selected))

        seccion_rellenos.visible = True
        check_continuar()
        page.update()

    def on_forma_selected(e):
        use_cases.seleccionar_tipo_forma(e.control.data)
        for card in forma_cards.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        seccion_panes.visible = True
        seccion_rellenos.visible = False
        for card in pan_cards.controls: card.border = None
        for card in relleno_cards.controls: card.border = None

        check_continuar()
        page.update()

    def restablecer_selecciones(e):
        use_cases.reiniciar_componentes()
        for card_row in [forma_cards, pan_cards, relleno_cards]:
            for card in card_row.controls:
                card.border = None
        seccion_panes.visible = False
        seccion_rellenos.visible = False
        check_continuar()
        page.update()

    # --- Componente de Tarjeta ---
    def crear_tarjeta_seleccion(texto, imagen_src, on_click_handler):
        return ft.Container(
            width=226, height=314, bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(30),
            data=texto,
            on_click=on_click_handler,
            content=ft.Column(
                spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=176, height=119, margin=ft.margin.only(top=25),
                        border_radius=ft.border_radius.all(10),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=imagen_src, fit=ft.ImageFit.COVER)
                    ),
                    ft.Divider(height=2, color=ft.Colors.GREY_300),
                    ft.Text(texto, text_align=ft.TextAlign.CENTER, size=20, font_family="Bebas Neue"),
                ]
            )
        )

    # --- Carga inicial de datos ---
    id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria

    forma_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)
    for forma in use_cases.obtener_formas_por_categoria(id_categoria_actual):
        forma_cards.controls.append(crear_tarjeta_seleccion(forma.nombre, "formas/{}".format(forma.imagen_url), on_forma_selected))

    pan_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)
    for pan in use_cases.obtener_panes_por_categoria(id_categoria_actual):
        tarjeta_pan = crear_tarjeta_seleccion(pan.nombre, "panes/{}".format(pan.imagen_url),
                                              on_pan_selected)
        tarjeta_pan.data = (pan.id, pan.nombre)
        pan_cards.controls.append(tarjeta_pan)

    relleno_cards = ft.Row(wrap=True, spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER)

    # Definición de las secciones de la UI
    seccion_formas = ft.Column(
        [ft.Text("1. Elige la forma", size=25, font_family="Bebas Neue", color="#673C1C"), forma_cards],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    seccion_panes = ft.Column(
        [ft.Text("2. Elige el pan", size=25, font_family="Bebas Neue", color="#673C1C"), pan_cards],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, visible=False)
    seccion_rellenos = ft.Column(
        [ft.Text("3. Elige el relleno", size=25, font_family="Bebas Neue", color="#673C1C"), relleno_cards],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, visible=False)

    boton_continuar = ft.ElevatedButton("Elegir Decorado", on_click=lambda _: page.go("/decorado"), visible=False)
    boton_restablecer = ft.ElevatedButton("Restablecer", on_click=restablecer_selecciones)

    # --- Layout Final ---
    return ft.View(
        route="/relleno",
        scroll=ft.ScrollMode.ADAPTIVE,
        padding=20,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Text("Paso 3.1: Componentes del Pastel", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            seccion_formas,
            seccion_panes,
            seccion_rellenos,
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
                    boton_restablecer,
                    boton_continuar,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ]
    )


def vista_decorado(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Componente Reutilizable para Tarjetas ---
    def crear_tarjeta_decorado(texto: str, on_click_handler, data=None):
        """Crea una tarjeta de selección estilizada y clickeable."""
        return ft.Container(
            width=280,
            height=80,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(20),
            shadow=ft.BoxShadow(
                spread_radius=1, blur_radius=8,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(4, 4)
            ),
            content=ft.Text(
                texto,
                size=20,
                font_family="Bebas Neue",
                text_align=ft.TextAlign.CENTER
            ),
            alignment=ft.alignment.center,
            on_click=on_click_handler,
            data=data or texto
        )

    # --- 2. Definición de Controles Dinámicos ---
    campo_mensaje = ft.TextField(
        label="Mensaje en el pastel (opcional)",
        value=use_cases.obtener_pedido_actual().mensaje_pastel or ""
    )
    sub_opciones_container = ft.Row(wrap=True, spacing=15, run_spacing=15, alignment=ft.MainAxisAlignment.CENTER)
    tematica_container = ft.Column(
        visible=False,
        controls=[
            ft.TextField(label="Escribe la temática o personaje"),
            ft.Text("El material que se usará será acetato y no es comestible.", italic=True, size=12,
                    color=ft.Colors.GREY_600)
        ]
    )
    dd_color1 = ft.Dropdown(label="Color Principal", expand=True)
    dd_color2 = ft.Dropdown(label="Color Secundario (opcional)", expand=True)
    contenedor_colores = ft.Row(controls=[dd_color1, dd_color2], visible=False)

    boton_continuar = ft.ElevatedButton("Continuar a Extras", on_click=lambda _: page.go("/extras"), visible=False)

    panel_decorado = ft.Column(
        visible=False,
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # --- 3. Lógica y Manejadores de Eventos ---
    def check_continuar():
        pedido = use_cases.obtener_pedido_actual()
        listo = False
        if pedido.tipo_cobertura:
            if pedido.tipo_decorado == "Liso c/s Conchas de Betún":
                if pedido.decorado_liso_detalle and pedido.decorado_liso_color1:
                    if pedido.decorado_liso_detalle == "Diseño o Temática":
                        if pedido.decorado_tematica_detalle:
                            listo = True
                    else:
                        listo = True
            elif pedido.tipo_decorado == "Imágenes Predeterminadas" and pedido.decorado_imagen_id:
                pass
        boton_continuar.visible = listo
        page.update()

    def on_color_change(e):
        use_cases.seleccionar_colores_decorado(dd_color1.value, dd_color2.value)
        check_continuar()

    dd_color1.on_change = on_color_change
    dd_color2.on_change = on_color_change

    def on_sub_opcion_liso_click(e):
        detalle = e.control.data
        use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle)

        for btn in sub_opciones_container.controls:
            btn.border = ft.border.all(2, ft.Colors.GREEN) if btn == e.control else None

        colores_disponibles = use_cases.obtener_colores_disponibles()
        opciones_color = [ft.dropdown.Option(color) for color in colores_disponibles] or [
            ft.dropdown.Option(key="no-color", text="No hay opciones", disabled=True)]

        dd_color1.options = opciones_color
        dd_color2.options = opciones_color
        dd_color1.value = None
        dd_color2.value = None
        contenedor_colores.visible = True

        if detalle == "Diseño o Temática":
            def on_text_tematica_change(e_text):
                use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle, e_text.control.value)
                check_continuar()

            tematica_container.controls[0].on_change = on_text_tematica_change
            tematica_container.visible = True
        else:
            tematica_container.visible = False

        check_continuar()
        page.update()

    def on_decorado_principal_click(e):
        tipo_decorado = e.control.data
        use_cases.seleccionar_tipo_decorado(tipo_decorado)
        use_cases.guardar_mensaje_pastel(campo_mensaje.value)

        for btn in panel_decorado.controls[2].controls:
            btn.border = ft.border.all(2, ft.Colors.GREEN) if btn == e.control else None

        if tipo_decorado == "Imágenes Predeterminadas":
            page.go("/galeria")
            return

        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        tematica_container.visible = False
        boton_continuar.visible = False

        opciones = ["Chantilli", "Chorreado", "Diseño o Temática"]
        for opcion in opciones:
            sub_opciones_container.controls.append(
                crear_tarjeta_decorado(opcion, on_sub_opcion_liso_click)
            )
        page.update()

    def on_cobertura_click(e):
        #use_cases.seleccionar_tipo_cobertura(e.control.text)
        cobertura_seleccionada = e.control.data
        use_cases.seleccionar_tipo_cobertura(cobertura_seleccionada)

        for btn in contenedor_coberturas.controls:
            if isinstance(btn, ft.FilledButton): btn.selected = (btn == e.control)

        use_cases.seleccionar_tipo_decorado(None)
        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        tematica_container.visible = False
        boton_continuar.visible = False

        panel_decorado.visible = True
        page.update()

    # --- 4. Construcción del Layout ---
    contenedor_coberturas = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    pedido_actual = use_cases.obtener_pedido_actual()
    if pedido_actual.id_categoria and pedido_actual.tipo_pan:
        panes_disponibles = use_cases.obtener_panes_por_categoria(pedido_actual.id_categoria)
        pan_obj = next((p for p in panes_disponibles if p.nombre == pedido_actual.tipo_pan), None)

        if pan_obj:
            lista_coberturas = use_cases.obtener_coberturas_disponibles(pedido_actual.id_categoria, pan_obj.id)
            if lista_coberturas:
                for cobertura in lista_coberturas:
                    contenedor_coberturas.controls.append(
                        crear_tarjeta_decorado(cobertura.nombre, on_cobertura_click)
                    )
            else:
                contenedor_coberturas.controls.append(ft.Text("No hay coberturas disponibles para esta selección."))
        else:
            contenedor_coberturas.controls.append(ft.Text("Error al cargar coberturas.", color=ft.Colors.RED))
    else:
        contenedor_coberturas.controls.append(ft.Text("Selección de categoría o pan inválida.", color=ft.Colors.RED))

    panel_decorado.controls = [
        ft.Divider(height=10),
        ft.Text("Después, elige un estilo de decoración:"),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                crear_tarjeta_decorado("Liso c/s Conchas de Betún", on_decorado_principal_click),
                crear_tarjeta_decorado("Imágenes Predeterminadas", on_decorado_principal_click),
            ]
        ),
        ft.Divider(height=15),
        sub_opciones_container,
        tematica_container,
        contenedor_colores,
        ft.Divider(height=10),
        campo_mensaje,
    ]

    return ft.View(
        route="/decorado",
        controls=[
            ft.Text("Paso 4: Cobertura y Decorado", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Primero, elige la cobertura:"),
            contenedor_coberturas,
            panel_decorado,
            ft.Divider(height=15),
            ft.Row(
                [
                    ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
                    boton_continuar,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15, padding=20,
        scroll=ft.ScrollMode.ADAPTIVE
    )

# def vista_decorado(page: ft.Page, use_cases: PedidoUseCases):
#     # --- 1. Componente Reutilizable para Tarjetas de Selección ---
#     def crear_tarjeta_decorado(texto: str, on_click_handler, data=None):
#         """Crea una tarjeta de selección estilizada y clickeable."""
#         return ft.Container(
#             width=280,
#             height=80,
#             bgcolor=ft.Colors.WHITE,
#             border_radius=ft.border_radius.all(20),
#             shadow=ft.BoxShadow(
#                 spread_radius=1, blur_radius=8,
#                 color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
#                 offset=ft.Offset(4, 4)
#             ),
#             content=ft.Text(
#                 texto,
#                 size=20,
#                 font_family="Bebas Neue",
#                 text_align=ft.TextAlign.CENTER
#             ),
#             alignment=ft.alignment.center,
#             on_click=on_click_handler,
#             data=data or texto # Guardamos el texto o un dato específico
#         )
#
#     contenedor_coberturas = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
#
#     campo_mensaje = ft.TextField(
#         label="Mensaje en el pastel (opcional)",
#         value=use_cases.obtener_pedido_actual().mensaje_pastel or ""
#     )
#
#     # Contenedores para las opciones que aparecen y desaparecen
#     sub_opciones_container = ft.Column(wrap=True, spacing=15, run_spacing=15, alignment=ft.MainAxisAlignment.CENTER)
#
#     tematica_container = ft.Column(
#         visible=False,
#         controls=[
#             ft.TextField(label="Escribe la temática o personaje"),
#             ft.Text(
#                 "El material que se usará será acetato y no es comestible.",
#                 italic=True,
#                 size=12,
#                 color=ft.Colors.GREY_600  # Sintaxis correcta: ft.colors
#             )
#         ]
#     )
#
#     dd_color1 = ft.Dropdown(label="Color Principal", expand=True)
#     dd_color2 = ft.Dropdown(label="Color Secundario (opcional)", expand=True)
#     contenedor_colores = ft.Row(controls=[dd_color1, dd_color2], visible=False)
#
#     boton_continuar = ft.ElevatedButton(
#         "Continuar a Extras",
#         on_click=lambda _: page.go("/extras"),
#         visible=False
#     )
#
#     # Panel principal para las opciones de decorado, inicialmente oculto
#     panel_decorado = ft.Column(
#         visible=False,
#         spacing=15,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER
#     )
#
#     # --- 2. Lógica y Manejadores de Eventos ---
#
#     def check_continuar():
#         """Verifica si se debe mostrar el botón de continuar basado en las selecciones."""
#         pedido = use_cases.obtener_pedido_actual()
#         listo_para_continuar = False
#
#         if pedido.tipo_cobertura:
#             if pedido.tipo_decorado == "Liso c/s Conchas de Betún":
#                 if pedido.decorado_liso_detalle and pedido.decorado_liso_color1:
#                     if pedido.decorado_liso_detalle == "Diseño o Temática":
#                         if pedido.decorado_tematica_detalle:
#                             listo_para_continuar = True
#                     else:
#                         listo_para_continuar = True
#
#         boton_continuar.visible = listo_para_continuar
#         page.update()
#
#     def on_color_change(e):
#         """Guarda los colores seleccionados y verifica si se puede continuar."""
#         use_cases.seleccionar_colores_decorado(dd_color1.value, dd_color2.value)
#         check_continuar()
#
#     dd_color1.on_change = on_color_change
#     dd_color2.on_change = on_color_change
#
#     def on_sub_opcion_liso_click(e):
#         """Manejador para 'Chantilli', 'Chorreado' y 'Diseño'."""
#         detalle = e.control.text
#         use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle)
#
#         for btn in sub_opciones_container.controls:
#             if isinstance(btn, ft.ElevatedButton): btn.selected = (btn == e.control)
#
#         # Siempre muestra los selectores de color
#         colores_disponibles = use_cases.obtener_colores_disponibles()
#         opciones_color = [ft.dropdown.Option(color) for color in colores_disponibles] or [
#             ft.dropdown.Option(key="no-color", text="No hay opciones", disabled=True)]
#
#         dd_color1.options = opciones_color
#         dd_color2.options = opciones_color
#         dd_color1.value = None
#         dd_color2.value = None
#         contenedor_colores.visible = True
#
#         # Muestra el campo de texto de temática solo si es necesario
#         if detalle == "Diseño o Temática":
#             def on_text_tematica_change(e_text):
#                 use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle, e_text.control.value)
#                 check_continuar()
#
#             tematica_container.controls[0].on_change = on_text_tematica_change
#             tematica_container.visible = True
#         else:
#             tematica_container.visible = False
#
#         check_continuar()
#         page.update()
#
#     def on_decorado_principal_click(e):
#         """Manejador para 'Liso...' o 'Imágenes...'."""
#         tipo_decorado = e.control.text
#         use_cases.seleccionar_tipo_decorado(tipo_decorado)
#         use_cases.guardar_mensaje_pastel(campo_mensaje.value)
#
#         if tipo_decorado == "Imágenes Predeterminadas":
#             page.go("/galeria")
#             return
#
#         sub_opciones_container.controls.clear()
#         contenedor_colores.visible = False
#         tematica_container.visible = False
#         boton_continuar.visible = False
#
#         opciones = ["Chantilli", "Chorreado", "Diseño o Temática"]
#         for opcion in opciones:
#             sub_opciones_container.controls.append(
#                 crear_tarjeta_decorado(opcion, on_sub_opcion_liso_click)
#             )
#         # sub_opciones_container.controls.extend([
#         #     ft.ElevatedButton("Chantilli", on_click=on_sub_opcion_liso_click),
#         #     ft.ElevatedButton("Chorreado", on_click=on_sub_opcion_liso_click),
#         #     ft.ElevatedButton("Diseño o Temática", on_click=on_sub_opcion_liso_click),
#         # ])
#         page.update()
#
#     def on_cobertura_click(e):
#         """Manejador principal que activa el resto de las opciones de la pantalla."""
#         use_cases.seleccionar_tipo_cobertura(e.control.text)
#
#         for btn in contenedor_coberturas.controls:
#             if isinstance(btn, ft.FilledButton): btn.selected = (btn == e.control)
#
#         # Resetea las opciones de decorado para una nueva selección
#         use_cases.seleccionar_tipo_decorado(None)
#         sub_opciones_container.controls.clear()
#         contenedor_colores.visible = False
#         tematica_container.visible = False
#         boton_continuar.visible = False
#
#         panel_decorado.visible = True
#         page.update()
#
#     # --- 3. Construcción del Layout ---
#
#     # # Se define el contenido estático del panel de decorado
#     # panel_decorado.controls = [
#     #     ft.Divider(height=10),
#     #     ft.Text("Después, elige un estilo de decoración:"),
#     #     ft.Row(
#     #         alignment=ft.MainAxisAlignment.CENTER,
#     #         controls=[
#     #             ft.ElevatedButton("Liso c/s Conchas de Betún", on_click=on_decorado_principal_click),
#     #             ft.ElevatedButton("Imágenes Predeterminadas", on_click=on_decorado_principal_click),
#     #         ]
#     #     ),
#     #     ft.Divider(height=15),
#     #     sub_opciones_container,
#     #     tematica_container,
#     #     contenedor_colores,
#     # ]
#     # Se define el contenido del panel de decorado usando las nuevas tarjetas
#     panel_decorado.controls = [
#         ft.Divider(height=10),
#         ft.Text("Elige un estilo de decoración:"),
#         ft.Row(
#             alignment=ft.MainAxisAlignment.CENTER,
#             spacing=20,
#             controls=[
#                 crear_tarjeta_decorado("Liso c/s Conchas de Betún", on_decorado_principal_click),
#                 crear_tarjeta_decorado("Imágenes Predeterminadas", on_decorado_principal_click),
#             ]
#         ),
#         ft.Divider(height=15),
#         sub_opciones_container,
#         tematica_container,
#         contenedor_colores,
#         campo_mensaje,
#     ]
#
#     # Carga inicial de las coberturas al entrar a la vista
#     pedido_actual = use_cases.obtener_pedido_actual()
#
#     if pedido_actual.id_categoria and pedido_actual.tipo_pan:
#         panes_disponibles = use_cases.obtener_panes_por_categoria(pedido_actual.id_categoria)
#         pan_obj = next((p for p in panes_disponibles if p.nombre == pedido_actual.tipo_pan), None)
#
#         if pan_obj:
#             lista_coberturas = use_cases.obtener_coberturas_disponibles(pedido_actual.id_categoria, pan_obj.id)
#             if lista_coberturas:
#                 for cobertura in lista_coberturas:
#                     contenedor_coberturas.controls.append(ft.FilledButton(text=cobertura, on_click=on_cobertura_click))
#             else:
#                 contenedor_coberturas.controls.append(ft.Text("No hay coberturas disponibles para esta selección."))
#         else:
#             contenedor_coberturas.controls.append(ft.Text("Error al cargar coberturas.", color=ft.Colors.RED))
#     else:
#         contenedor_coberturas.controls.append(ft.Text("Selección de categoría o pan inválida.", color=ft.Colors.RED))
#
#     # Se retorna la vista final ensamblada
#     # return ft.View(
#     #     route="/decorado",
#     #     controls=[
#     #         ft.Text("Paso 4: Cobertura y Decorado", size=30, weight=ft.FontWeight.BOLD),
#     #         ft.Text("Elige la cobertura:"),
#     #         contenedor_coberturas,
#     #
#     #         # El campo de mensaje se sitúa después de la cobertura
#     #         campo_mensaje,
#     #
#     #         # Panel con el resto de opciones de decorado
#     #         panel_decorado,
#     #
#     #         ft.Divider(height=15),
#     #         ft.Row(
#     #             [
#     #                 ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
#     #                 boton_continuar,
#     #             ],
#     #             alignment=ft.MainAxisAlignment.CENTER
#     #         )
#     #     ],
#     #     vertical_alignment=ft.MainAxisAlignment.START,
#     #     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#     #     spacing=15, padding=20,
#     #     scroll=ft.ScrollMode.ADAPTIVE
#     # )
#     # Se retorna la vista final ensamblada
#     return ft.View(
#         route="/decorado",
#         controls=[
#             ft.Text("Paso 4: Cobertura y Decorado", size=30, weight=ft.FontWeight.BOLD),
#             ft.Text("Primero, elige la cobertura:"),
#             contenedor_coberturas,
#             panel_decorado,
#             ft.Divider(height=15),
#             ft.Row(
#                 [
#                     ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
#                     boton_continuar,
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER
#             )
#         ],
#         vertical_alignment=ft.MainAxisAlignment.START,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         spacing=15, padding=20,
#         scroll=ft.ScrollMode.ADAPTIVE
#     )

# --- NUEVA VISTA DE GALERÍA ---
def vista_galeria(page: ft.Page, use_cases: PedidoUseCases):
    # --- Controles de la Interfaz ---
    grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=180,  # Un poco más de espacio para las imágenes
        child_aspect_ratio=0.8,  # Ajustado para imagen + texto
        spacing=10,
        run_spacing=10
    )

    # --- Manejadores de Eventos ---
    def on_image_click(e):
        id_imagen_seleccionada = e.control.data
        use_cases.seleccionar_imagen_decorado(id_imagen_seleccionada)
        page.go("/extras")

    def actualizar_galeria(e=None):  # Ahora acepta el evento 'e'
        categoria_filtro = filtro_categoria.value if filtro_categoria.value != "Todas" else None
        termino_busqueda = campo_busqueda.value

        grid.controls.clear()

        imagenes = use_cases.buscar_imagenes_galeria(categoria_filtro, termino_busqueda)
        for img in imagenes:
            grid.controls.append(
                ft.Container(
                    data=img.id,
                    on_click=on_image_click,
                    tooltip=f"Seleccionar {img.descripcion}",
                    border_radius=ft.border_radius.all(10),
                    content=ft.Stack(
                        # --- CÓDIGO CORREGIDO AQUÍ ---
                        # Reemplazamos el '...' con los controles de imagen y texto reales.
                        [
                            ft.Image(
                                src=img.url,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(10)
                            ),
                            ft.Container(
                                content=ft.Text(img.descripcion, color="white", weight=ft.FontWeight.BOLD),
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                                padding=8,
                                alignment=ft.alignment.bottom_center,
                                border_radius=ft.border_radius.all(10),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_center,
                                    end=ft.alignment.bottom_center,
                                    colors=[ft.Colors.TRANSPARENT, ft.Colors.BLACK],
                                )
                            )
                        ]
                        # -----------------------------
                    )
                )
            )
        page.update()

    # --- Controles de Filtro y Búsqueda ---
    filtro_categoria = ft.Dropdown(
        label="Filtrar por categoría",
        options=[ft.dropdown.Option("Todas"), ft.dropdown.Option("Infantil"), ft.dropdown.Option("Floral")],
        value="Todas",
        on_change=actualizar_galeria,
        expand=True
    )
    campo_busqueda = ft.TextField(
        label="Buscar...",
        on_change=actualizar_galeria,
        expand=True
    )

    # Carga inicial de la galería
    actualizar_galeria()

    # --- Construcción de la Vista ---
    return ft.View(
        route="/galeria",
        controls=[
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/decorado"), tooltip="Volver"),
                ft.Text("Galería de Imágenes", size=24, weight=ft.FontWeight.BOLD)
            ]),
            ft.Row([filtro_categoria, campo_busqueda]),
            # El GridView se expandirá para usar el espacio restante
            grid
        ]
    )


def vista_extras(page: ft.Page, use_cases: PedidoUseCases):
    def on_radio_change(e):
        use_cases.seleccionar_extra(e.control.value)

    opciones_extra = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Ninguno", label="Ninguno"),
            ft.Radio(value="Flor Artificial", label="Flor Artificial"),
            ft.Radio(value="Chorreado dorado", label="Chorreado dorado"),
            ft.Radio(value="Chorreado plateado", label="Chorreado plateado"),
        ]),
        on_change=on_radio_change,
        value=use_cases.obtener_pedido_actual().extra_seleccionado
    )

    return ft.View(
        route="/extras",
        controls=[
            ft.Text("Paso 5: ¿Deseas algún Extra?", size=30, weight=ft.FontWeight.BOLD),
            opciones_extra,
            ft.Row([
                ft.ElevatedButton("Volver", on_click=lambda _: page.go("/decorado")),
                ft.ElevatedButton("Ver Resumen", on_click=lambda _: page.go("/resumen"))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )


# def vista_resumen(page: ft.Page, use_cases: PedidoUseCases):
#     # 1. Obtenemos el estado final del pedido desde los casos de uso
#     pedido_actual = use_cases.obtener_pedido_actual()
#
#     # Para mostrar el nombre de la categoría en lugar de solo el ID
#     categorias = {c.id: c.nombre for c in use_cases.obtener_categorias()}
#     nombre_categoria = categorias.get(pedido_actual.id_categoria, "No seleccionada")
#
#     # --- 2. Función de Ayuda para Crear Filas ---
#     def create_summary_row(title: str, value: str | None):
#         """
#         Crea una fila de resumen consistente. Si el valor es None o está vacío,
#         muestra 'No especificado' para mayor claridad.
#         """
#         return ft.Row(
#             [
#                 ft.Text(f"{title}:", weight=ft.FontWeight.BOLD, width=150),
#                 ft.Text(value if value else "No especificado", expand=True),
#             ]
#         )
#
#     # --- 3. Construcción de la Lista de Controles del Resumen ---
#     # Creamos una lista para añadir dinámicamente solo los detalles relevantes.
#
#     controles_resumen = [
#         # --- Detalles Generales ---
#         create_summary_row("Categoría", nombre_categoria),
#         create_summary_row("Fecha de Entrega",
#                            pedido_actual.fecha_entrega.strftime('%d/%m/%Y') if pedido_actual.fecha_entrega else None),
#         create_summary_row("Tamaño (personas)", pedido_actual.tamano_pastel),
#         create_summary_row("Forma", pedido_actual.tipo_forma),
#         create_summary_row("Pan", pedido_actual.tipo_pan),
#         create_summary_row("Relleno", pedido_actual.tipo_relleno),
#         create_summary_row("Cobertura", pedido_actual.tipo_cobertura),
#         create_summary_row("Extra", pedido_actual.extra_seleccionado),
#         ft.Divider(),
#
#         # --- Detalles del Decorado ---
#         ft.Text("Detalles del Decorado:", weight=ft.FontWeight.BOLD, size=18),
#         create_summary_row("Mensaje en Pastel", pedido_actual.mensaje_pastel),
#         create_summary_row("Estilo Principal", pedido_actual.tipo_decorado),
#     ]
#
#     # --- Lógica Condicional para mostrar solo los detalles relevantes ---
#     if pedido_actual.tipo_decorado == "Liso c/s Conchas de Betún":
#         controles_resumen.append(create_summary_row("  ↳ Detalle", pedido_actual.decorado_liso_detalle))
#         # --- CAMBIO: Mostramos los colores y la temática si existen ---
#         if pedido_actual.decorado_liso_detalle == "Diseño o Temática":
#             controles_resumen.append(create_summary_row("  ↳ Temática", pedido_actual.decorado_tematica_detalle))
#
#         # Mostramos los colores para TODAS las opciones de "Liso"
#         controles_resumen.append(create_summary_row("  ↳ Color Principal", pedido_actual.decorado_liso_color1))
#         controles_resumen.append(create_summary_row("  ↳ Color Secundario", pedido_actual.decorado_liso_color2))
#
#     elif pedido_actual.tipo_decorado == "Imágenes Predeterminadas":
#         controles_resumen.append(create_summary_row("  ↳ ID de Imagen", str(pedido_actual.decorado_imagen_id)))
#         if pedido_actual.decorado_imagen_id:
#             url_imagen = use_cases.obtener_url_imagen_galeria_por_id(pedido_actual.decorado_imagen_id)
#             if url_imagen:
#                 controles_resumen.append(
#                     ft.Row([
#                         ft.Text("  ↳ Miniatura:", weight=ft.FontWeight.BOLD, width=150),
#                         ft.Image(src=url_imagen, width=100, height=100, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5)),
#                     ])
#                 )
#
#     # --- 4. Construcción del Layout Final de la Vista ---
#     return ft.View(
#         route="/resumen",
#         controls=[
#             ft.Text("Resumen de tu Pedido", size=30, weight=ft.FontWeight.BOLD),
#             ft.Text("Por favor, verifica que toda la información sea correcta."),
#             ft.Divider(height=20),
#
#             # Usamos la lista de controles que acabamos de construir
#             ft.Column(controls=controles_resumen, spacing=8),
#
#             ft.Divider(height=30),
#             ft.Row(
#                 [
#                     ft.ElevatedButton("Modificar Pedido", on_click=lambda _: page.go("/decorado")),
#                     ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/datos_cliente")),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER
#             )
#         ],
#         vertical_alignment=ft.MainAxisAlignment.START,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         spacing=15,
#         padding=20,
#         scroll=ft.ScrollMode.ADAPTIVE
#     )
def vista_resumen(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Obtención de Datos ---
    pedido_actual = use_cases.obtener_pedido_actual()
    categorias = {c.id: c.nombre for c in use_cases.obtener_categorias()}
    nombre_categoria = categorias.get(pedido_actual.id_categoria, "No seleccionada")

    # --- 2. Construcción de Componentes ---

    # Panel izquierdo con el resumen en texto
    panel_resumen_texto = ft.Container(
        width=749,
        height=333,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(40),
        padding=25,
        content=ft.Column(
            controls=[
                ft.Text("Resumen de tu pedido", size=30, font_family="Bebas Neue", color="#673C1C"),
                ft.Row([
                    ft.Column([
                        ft.Text("Categoría:", weight=ft.FontWeight.BOLD),
                        ft.Text("Fecha de entrega:", weight=ft.FontWeight.BOLD),
                        ft.Text("Tamaño (#Personas):", weight=ft.FontWeight.BOLD),
                        ft.Text("Forma del pastel:", weight=ft.FontWeight.BOLD),
                        ft.Text("Pan:", weight=ft.FontWeight.BOLD),
                        ft.Text("Relleno:", weight=ft.FontWeight.BOLD),
                        ft.Text("Cobertura:", weight=ft.FontWeight.BOLD),
                        ft.Text("Extra:", weight=ft.FontWeight.BOLD),
                    ], expand=1),
                    ft.Column([
                        ft.Text(nombre_categoria),
                        ft.Text(
                            pedido_actual.fecha_entrega.strftime('%d/%m/%Y') if pedido_actual.fecha_entrega else "N/A"),
                        ft.Text(pedido_actual.tamano_pastel),
                        ft.Text(pedido_actual.tipo_forma),
                        ft.Text(pedido_actual.tipo_pan),
                        ft.Text(pedido_actual.tipo_relleno),
                        ft.Text(pedido_actual.tipo_cobertura),
                        ft.Text(pedido_actual.extra_seleccionado),
                        #
                        #         # --- Detalles del Decorado ---
                        #         ft.Text("Detalles del Decorado:", weight=ft.FontWeight.BOLD, size=18),
                        #         create_summary_row("Mensaje en Pastel", pedido_actual.mensaje_pastel),
                        #         create_summary_row("Estilo Principal", pedido_actual.tipo_decorado),
                    ], expand=1),
                ]),
                # ... Aquí puedes añadir más filas para los demás detalles
            ]
        )
    )

    # Botones de acción
    boton_modificar = ft.ElevatedButton("Modificar Pedido", on_click=lambda _: page.go("/decorado"))
    boton_continuar = ft.Container(
        width=169, height=58, bgcolor="#87D5BA", border_radius=15,
        content=ft.Text("Continuar", color=ft.Colors.WHITE, size=30, font_family="Poppins"),
        alignment=ft.alignment.center,
        on_click=lambda _: page.go("/datos_cliente")
    )

    # --- 3. Construcción del Layout Final ---

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner superior
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(expand=True,
                         content=ft.ResponsiveRow(
                             alignment=ft.MainAxisAlignment.CENTER,
                             vertical_alignment=ft.CrossAxisAlignment.CENTER,
                             controls=[
                                 ft.Column(col={"md": 7}, controls=[panel_resumen_texto]),
                                 ft.Column(col={"md": 5}, controls=[
                                     ft.Image(src="tres_leches_final.png", border_radius=20) # 253 x 287
                                 ])
                             ]
                         )
                         ),
            ft.Row([boton_modificar, boton_continuar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            #ft.Image(src="https://placehold.co/1520x1192", fit=ft.ImageFit.COVER, expand=True),
            ft.Image(src="15fc9b754973ad7c32288c9216fe5d62b84512b4.jpg", fit=ft.ImageFit.FILL, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.2, "#DC6262"), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/resumen",
        controls=[layout_final],
        padding=0
    )

def vista_datos_cliente(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Estado de la Vista ---
    # Guardaremos una referencia al campo de texto que tiene el foco
    campo_enfocado = ft.Ref[ft.TextField]()

    # --- 2. Lógica y Manejadores de Eventos ---
    def on_keyboard_key(key: str):
        """El callback que el teclado llamará. Se encarga de la lógica."""
        target = campo_enfocado.current
        if target:
            if key == "BACKSPACE":
                # Borra el último caracter
                target.value = target.value[:-1] if target.value else ""
            elif key == " ":
                # Añade un espacio
                target.value += " "
            else:
                # Añade el caracter
                target.value += key
            page.update()

    def on_textfield_focus(e):
        """Cuando un TextField obtiene el foco, lo guardamos."""
        campo_enfocado.current = e.control
        print(f"DIAGNÓSTICO: Campo enfocado - {e.control.label}")
        # Hacemos visible el teclado
        teclado_virtual.keyboard_control.visible = True
        page.update()

    teclado_virtual = VirtualKeyboard(page, on_keyboard_key)
    teclado_virtual.keyboard_control.visible = False # El teclado empieza oculto

    nombre = ft.TextField(label="Nombre completo", on_focus=on_textfield_focus)
    telefono = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE, on_focus=on_textfield_focus)
    direccion = ft.TextField(label="Dirección (Calle)", on_focus=on_textfield_focus)
    num_ext = ft.TextField(label="Número exterior", width=150, on_focus=on_textfield_focus)
    entre_calles = ft.TextField(label="Entre calles", on_focus=on_textfield_focus)
    cp = ft.TextField(label="Código Postal", width=150, keyboard_type=ft.KeyboardType.NUMBER, on_focus=on_textfield_focus)
    colonia = ft.TextField(label="Colonia", on_focus=on_textfield_focus)
    ciudad = ft.TextField(label="Ciudad", on_focus=on_textfield_focus)
    municipio = ft.TextField(label="Municipio", on_focus=on_textfield_focus)
    estado = ft.TextField(label="Estado", on_focus=on_textfield_focus)
    referencias = ft.TextField(label="Referencias del domicilio", multiline=True, min_lines=2, on_focus=on_textfield_focus)

    def finalizar_pedido(e):
        # Validación simple
        if not nombre.value or not telefono.value or not direccion.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nombre, teléfono y dirección son obligatorios."),
                                         bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        # Recopilamos los datos en un diccionario
        datos_formulario = {
            "nombre_completo": nombre.value,
            "telefono": telefono.value,
            "direccion": direccion.value,
            "numero_exterior": num_ext.value,
            "entre_calles": entre_calles.value,
            "codigo_postal": cp.value,
            "colonia": colonia.value,
            "ciudad": ciudad.value,
            "municipio": municipio.value,
            "estado": estado.value,
            "referencias": referencias.value
        }

        try:
            # 1. Ejecutamos el caso de uso y obtenemos el pedido final y el QR
            pedido_final = use_cases.guardar_datos_y_finalizar(datos_formulario)

            # 2. Guardamos los datos en la sesión de la página para pasarlos a la siguiente vista
            page.session.set("pedido_final", pedido_final)

            # 3. Navegamos a la pantalla final
            page.go("/confirmacion")
        except Exception as ex:
            print(f"ERROR: Ocurrió un error al finalizar el pedido: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al guardar el pedido."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

        # Navegamos a la pantalla final
        page.go("/confirmacion")


    return ft.View(
        route="/datos_cliente",
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    ft.Text("Datos de Entrega", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Toca un campo para activar el teclado."),
                    nombre, telefono, direccion,
                    ft.Row([num_ext, cp]),
                    entre_calles, colonia, ciudad, municipio, estado, referencias,
                    ft.Row(
                        [
                            ft.ElevatedButton("Volver al Resumen", on_click=lambda _: page.go("/resumen")),
                            ft.ElevatedButton("Finalizar Pedido", on_click=finalizar_pedido),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            # 3. Llamamos al método .build() para obtener el control de Flet
            teclado_virtual.build()
        ],
        padding=10
    )


def vista_confirmacion(page: ft.Page, use_cases: PedidoUseCases):

    pedido_final = page.session.get("pedido_final")

    if not pedido_final:
        return ft.View("/", [ft.Text("Error: No se encontraron datos del pedido.")])


    def create_summary_row(title: str, value: str):
        return ft.Row([
            ft.Text(f"{title}:", weight=ft.FontWeight.BOLD, width=100),
            ft.Text(value or "No especificado", expand=True),
        ])

    def reiniciar_app(e):
        # Limpiamos los datos del pedido en memoria para el siguiente cliente
        # (Esto requeriría un caso de uso "reiniciar_app", por ahora solo navegamos)
        page.session.clear() # Limpiamos la sesión
        page.go("/")

    pedido_actual = use_cases.obtener_pedido_actual()
    categorias = {c.id: c.nombre for c in use_cases.obtener_categorias()}
    nombre_categoria = categorias.get(pedido_actual.id_categoria, "No seleccionada")

    ticket_controls = [
        ft.Text("¡Pedido Confirmado!", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Gracias, {pedido_final.datos_entrega.nombre_completo}"),
        ft.Divider(),
        ft.Text("Detalles del Pedido:", weight=ft.FontWeight.BOLD),
        create_summary_row("Categoría", nombre_categoria),
        create_summary_row("Fecha Entrega", pedido_final.fecha_entrega.strftime('%d/%m/%Y')),
        create_summary_row("Tamaño", pedido_final.tamano_pastel),
        create_summary_row("Forma", pedido_final.tipo_forma),
        create_summary_row("Pan", pedido_final.tipo_pan),
        create_summary_row("Relleno", pedido_final.tipo_relleno),
        create_summary_row("Cobertura", pedido_final.tipo_cobertura),
        ft.Divider(),
        ft.ElevatedButton("Iniciar Nuevo Pedido", on_click=reiniciar_app, width=300)
    ]

    return ft.View(
        route="/confirmacion",
        controls=ticket_controls,
        scroll=ft.ScrollMode.ADAPTIVE,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        padding=20
    )

