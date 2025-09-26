# src/infrastructure/flet_adapter/views.py
import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
from src.application.use_cases import PedidoUseCases, FinalizarPedidoUseCases
from .keyboard import VirtualKeyboard
from .controles_comunes import crear_boton_navegacion
from src.application.use_cases import AuthUseCases


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


def crear_vista_con_fondo(ruta, titulo, contenido, page, boton_volver_ruta, boton_continuar, boton_restablecer):
    banner_superior = ft.Container(
        height=67,
        bgcolor="#89C5B0",
        alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                        font_family="Bebas Neue")
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Text(titulo, size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        *contenido
                    ]
                )
            ),
            ft.Row(
                [
                    ft.ElevatedButton("Volver", on_click=lambda _: page.go(boton_volver_ruta)),
                    boton_restablecer,
                    boton_continuar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            ft.Container(height=20)  # Margen inferior
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route=ruta,
        controls=[layout_final],
        padding=0
    )


def vista_login(page: ft.Page, auth_use_cases: AuthUseCases):
    campo_enfocado = ft.Ref[ft.TextField]()
    imagen_personaje_ref = ft.Ref[ft.Image]()

    def on_keyboard_key(key: str):
        target = campo_enfocado.current
        if not target: return
        if key == "BACKSPACE":
            target.value = target.value[:-1] if target.value else ""
        else:
            target.value += key
        page.update()

    def on_login_click(e):
        teclado_virtual.keyboard_control.visible = False
        if imagen_personaje_ref.current:
            imagen_personaje_ref.current.visible = True
        page.update()
        if auth_use_cases.login(campo_usuario.value, campo_password.value):
            page.go("/")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos."), bgcolor=ft.Colors.RED_ACCENT_700)
            page.snack_bar.open = True
            page.update()

    def mostrar_teclado():
        if imagen_personaje_ref.current:
            imagen_personaje_ref.current.visible = False
        teclado_virtual.keyboard_control.visible = True
        page.update()

    def ocultar_teclado(e):
        if imagen_personaje_ref.current:
            imagen_personaje_ref.current.visible = True
        teclado_virtual.keyboard_control.visible = False
        page.update()

    def on_textfield_focus(e):
        campo_enfocado.current = e.control
        mostrar_teclado()

    teclado_virtual = VirtualKeyboard(
        page,
        on_key=on_keyboard_key,
        on_enter=on_login_click,
        on_hide=ocultar_teclado
    )
    teclado_virtual.keyboard_control.visible = False

    campo_usuario = ft.TextField(
        hint_text="Usuario",
        border=ft.InputBorder.NONE,
        height=50,
        bgcolor=ft.Colors.WHITE,
        border_radius=25,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        on_focus=on_textfield_focus
    )

    campo_password = ft.TextField(
        hint_text="Contraseña",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        height=50,
        bgcolor=ft.Colors.WHITE,
        border_radius=25,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        on_focus=on_textfield_focus
    )

    boton_entrar = ft.Container(
        height=55,
        bgcolor="#C16160",
        border_radius=27.5,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SOUP_KITCHEN_OUTLINED, color=ft.Colors.WHITE),
                ft.Text("INICIAR SESIÓN", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ]
        ),
        on_click=on_login_click
    )

    imagen_personaje = ft.Image(
        ref=imagen_personaje_ref,
        src="Recurso 3.png",
        height=400,
        fit=ft.ImageFit.CONTAIN
    )

    contenido_dinamico = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(height=20),
                        ft.Text("¡ BIENVENIDO A NUESTRA PASTELERÍA !", size=40, font_family="Bebas Neue",
                                color="#6D6D6D"),
                        imagen_personaje,
                    ]
                )
            ),
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("INICIA SESIÓN PARA PODER CONTINUAR", weight=ft.FontWeight.BOLD, color="#6D6D6D"),
                    ft.Container(
                        width=450, padding=20,
                        content=ft.Column(
                            spacing=15,
                            controls=[campo_usuario, campo_password, boton_entrar]
                        )
                    ),
                    teclado_virtual.build(),
                    ft.Container(height=20)
                ]
            )
        ]
    )

    layout_final = ft.Stack(
        expand=True,
        controls=[
            ft.Container(bgcolor="#E5ADAD", expand=True),
            ft.Container(
                width=800, height=750,
                bgcolor="#F8F2ED",
                shape=ft.BoxShape.CIRCLE,
                top=-150, left=-70
            ),
            contenido_dinamico
        ]
    )

    return ft.View(
        route="/login",
        controls=[layout_final],
        padding=0
    )


def vista_bienvenida(page: ft.Page):

    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Text(
            'Para envío gratuito en compras de $500 o más',
            color=ft.Colors.WHITE,
            size=24,
            font_family="Bebas Neue",
        )
    )

    imagen_pastel = ft.Image(
        src="Logo Pepe.png",
        fit=ft.ImageFit.CONTAIN,
        height=250,
    )


    texto_bienvenida = ft.Text(
        '¡ Bienvenido a nuestra pastelería !',
        color=ft.Colors.WHITE,
        size=50,
        font_family="Bebas Neue",
        text_align=ft.TextAlign.CENTER,
        opacity=0.90,
    )

    texto_subtitulo = ft.Text(
        'Disfruta de nuestra amplia variedad de pasteles o si lo prefieres\nármalo y personalízalo a tu gusto.',
        color=ft.Colors.WHITE,
        size=22,
        font_family="Bebas Neue",
        text_align=ft.TextAlign.CENTER,
        opacity=0.80,
    )

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

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),
            ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        col={"sm": 11, "md": 8, "lg": 6},
                        controls=[
                            imagen_pastel,
                            texto_bienvenida,
                            texto_subtitulo,
                            ft.Container(height=20),
                            boton_comenzar,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    )
                ]
            ),
            ft.Container(expand=True),
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(
                src="929f8d1fff68e3deddd0d09b79812005b5683447.png",
                fit=ft.ImageFit.FILL,
                expand=True,
            ),
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.50, ft.Colors.BLACK),
                expand=True,
            ),
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


# def vista_seleccion(page: ft.Page):
#     # --- 1. Componente Reutilizable para las Nuevas Tarjetas (Sin Cambios) ---
#     def crear_tarjeta_mejorada(titulo: str, imagen_src: str, texto_boton: str, icono_boton, on_click_handler):
#         return ft.Container(
#             width=350,
#             height=480,
#             bgcolor=ft.Colors.WHITE,
#             border_radius=ft.border_radius.all(35),
#             shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26),
#             clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
#             content=ft.Column(
#                 spacing=0,
#                 controls=[
#                     ft.Image(src=imagen_src, height=240, fit=ft.ImageFit.COVER),
#                     ft.Container(
#                         padding=20,
#                         expand=True,
#                         content=ft.Column(
#                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                             alignment=ft.MainAxisAlignment.SPACE_AROUND,
#                             controls=[
#                                 ft.Text(titulo, text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD),
#                                 ft.Container(
#                                     bgcolor="#E5ADAD",
#                                     border_radius=10,
#                                     padding=ft.padding.symmetric(horizontal=20, vertical=10),
#                                     on_click=on_click_handler,
#                                     content=ft.Row(
#                                         spacing=10,
#                                         controls=[
#                                             ft.Icon(icono_boton, color=ft.Colors.BLACK),
#                                             ft.Text(texto_boton, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
#                                         ]
#                                     )
#                                 )
#                             ]
#                         )
#                     )
#                 ]
#             )
#         )
#
#     imagen_pastel = ft.Image(
#         src="Logo Pepe.png",
#         fit=ft.ImageFit.CONTAIN,
#         width=424, height=254,  # Altura máxima para la imagen
#     )
#
#     contenido_principal = ft.ResponsiveRow(
#         vertical_alignment=ft.CrossAxisAlignment.CENTER,
#         alignment=ft.MainAxisAlignment.CENTER,
#         spacing=40,
#         run_spacing=40,
#         controls=[
#             ft.Container(
#                 col={"sm": 12, "md": 5},
#                 alignment=ft.alignment.center,
#                 content=crear_tarjeta_mejorada(
#                     titulo="CONOCE NUESTRO CATÁLOGO Y PROMOCIONES",
#                     imagen_src="seleccion/promos.png",
#                     texto_boton="VER PROMOCIONES",
#                     icono_boton=ft.Icons.SEARCH,
#                     on_click_handler=lambda _: print("Navegar a promociones")
#                 )
#             ),
#             ft.Container(
#                 col={"sm": 12, "md": 5},
#                 alignment=ft.alignment.center,
#                 content=crear_tarjeta_mejorada(
#                     titulo="ARMA Y PERSONALIZA TU PASTEL",
#                     imagen_src="seleccion/arma.png",
#                     texto_boton="ARMA TU PASTEL",
#                     icono_boton=ft.Icons.CAKE_OUTLINED,
#                     on_click_handler=lambda _: page.go("/fecha")
#                 )
#             ),
#         ]
#     )
#
#     # --- 3. Construcción del Layout Final (CON EL LOGO) ---
#     layout_final = ft.Stack(
#         controls=[
#             # Capa 1: Imagen de Fondo
#             ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
#
#             # Capa 2: Banner Superior y Contenido Central
#             ft.Column(
#                 expand=True,
#                 controls=[
#                     ft.Container(  # Banner superior
#                         bgcolor="#89C5B0",
#                         padding=ft.padding.symmetric(horizontal=20, vertical=10),
#                         content=ft.Row(
#                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                             controls=[
#                                 ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.WHITE),
#                                 ft.Text('PARA ENVÍO GRATUITO EN COMPRAS DE $500 O MÁS', color=ft.Colors.WHITE,
#                                         font_family="Bebas Neue", size=24),
#                                 ft.IconButton(ft.Icons.HOME_OUTLINED, icon_color=ft.Colors.WHITE,
#                                               on_click=lambda _: page.go("/")),
#                             ]
#                         )
#                     ),
#                     ft.Container(expand=True),
#                     imagen_pastel,
#                     ft.Container(expand=True),
#                     ft.Container(  # Contenedor para las tarjetas y espaciado
#                         alignment=ft.alignment.center,
#                         expand=True,
#                         padding=ft.padding.only(top=120),  # Ajusta este padding para bajar las tarjetas
#                         content=contenido_principal
#                     )
#                 ]
#             ),
#
#             Capa 3: El Logo de la Pastelería flotando sobre todo
#             ft.Container(
#                 # Posicionamiento absoluto: centro horizontal, y a cierta distancia del top
#                 alignment=ft.alignment.center,
#                 top=50,  # Ajusta este valor para mover el logo verticalmente
#                 content=ft.Row(
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     controls=[
#                        ft.Image(src="Logo Pepe.png", width=424, height=254),
#                     ],
#                 ),
#                 # Asegúrate de que esta sea la ruta correcta a tu logo
#             ),
#         ]
#     )
#
#     return ft.View(
#         route="/seleccion",
#         controls=[layout_final],
#         padding=0
#     )

def vista_seleccion(page: ft.Page):

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

    banner_superior = ft.Container(
        bgcolor="#89C5B0", padding=15, alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=24,
                        font_family="Bebas Neue")
    )


    imagen_pastel = ft.Image(
        src="Logo Pepe.png",
        fit=ft.ImageFit.CONTAIN,
        width=424, height=254,  # Altura máxima para la imagen
    )

    # Botón para volver
    # boton_volver = crear_boton_navegacion(
    #                         texto="Volver",
    #                         on_click_handler=lambda _: page.go("/"),
    #                         es_primario=False
    #                     )
    #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/"))

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),  # Espaciador flexible superior
            imagen_pastel,
            ft.Container(expand=True),
            contenido_principal,  # El ResponsiveRow con las tarjetas
            ft.Container(height=40),  # Espacio fijo
            #boton_volver,  # Botón de volver
            ft.Container(height=40),  # Espacio fijo
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # El Stack final para el fondo y el contenido
    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
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

    texto_fecha_seleccionada = ft.Text(
        value=use_cases.obtener_pedido_actual().fecha_entrega.strftime(
            '%d/%m/%Y') if use_cases.obtener_pedido_actual().fecha_entrega else "No seleccionada",
        size=20, font_family="Poppins", weight=ft.FontWeight.W_600
    )

    def on_date_change(e):
        fecha = e.control.value.date()
        use_cases.seleccionar_fecha(fecha)
        texto_fecha_seleccionada.value = fecha.strftime('%d/%m/%Y')
        page.update()

    def on_time_change(e):
        use_cases.seleccionar_hora(e.control.value)
        page.update()

    fecha_hoy = datetime.date.today()
    fecha_inicial_valida = fecha_hoy + datetime.timedelta(days=4)
    fecha_final_valida = fecha_hoy + relativedelta(months=+6)

    def open_date_picker(e):
        page.open(
            ft.DatePicker(
                first_date=fecha_inicial_valida,
                last_date=fecha_final_valida,
                on_change=on_date_change,
                value=use_cases.obtener_pedido_actual().fecha_entrega or fecha_inicial_valida
            )
        )

    def continuar(e):
        pedido = use_cases.obtener_pedido_actual()
        if not pedido.fecha_entrega or not pedido.hora_entrega:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar fecha y hora para continuar."),
                                         bgcolor=ft.Colors.RED_ACCENT_700)
            page.snack_bar.open = True
            page.update()
        else:
            page.go("/tamano")


    banner_superior = ft.Container(
        height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                        font_family="Bebas Neue")
    )

    panel_principal = ft.Container(
        width=524,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(50),
        shadow=ft.BoxShadow(spread_radius=8, blur_radius=8, color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                            offset=ft.Offset(4, 4)),
        padding=40,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Text("¿Para cuándo necesitas el pastel?", size=35, font_family="Bebas Neue", weight=ft.FontWeight.W_700,
                        text_align=ft.TextAlign.CENTER),

                ft.Container(
                    on_click=open_date_picker,
                    padding=15,
                    border=ft.border.all(2, ft.Colors.with_opacity(0.5, "#DBCACA")),
                    border_radius=10,
                    content=ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, color="#780041"),
                        ft.Text("Fecha:", weight=ft.FontWeight.BOLD, font_family="Bebas Neue"),
                        texto_fecha_seleccionada
                    ])
                ),

                ft.Column([
                    ft.Text("SELECCIONA LA HORA", size=28, font_family="Poppins", color="#623F19",
                            weight=ft.FontWeight.W_600),
                    ft.Dropdown(
                        hint_text="Elige un rango de hora",
                        options=[
                            ft.dropdown.Option("10:00 AM - 12:00 PM"),
                            ft.dropdown.Option("12:00 PM - 02:00 PM"),
                            ft.dropdown.Option("02:00 PM - 04:00 PM"),
                            ft.dropdown.Option("04:00 PM - 06:00 PM"),
                        ],
                        value=use_cases.obtener_pedido_actual().hora_entrega,
                        on_change=on_time_change,
                        border_color="#DBCACA"
                    )
                ]),

                ft.Row(
                    [
                        #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/seleccion")),
                        ft.Container(
                            width=175, height=58, bgcolor="#DC6262", border_radius=15,
                            content=ft.Text("Continuar", color=ft.Colors.WHITE, size=30, font_family="Poppins"),
                            alignment=ft.alignment.center,
                            on_click=continuar
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=20
                )
            ]
        )
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(
                alignment=ft.alignment.center,
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src="Logo Pepe.png", width=424, height=254),
                        ft.Container(height=30),
                        panel_principal,
                    ]
                )
            ),
            banner_superior,
        ]
    )

    return ft.View(
        route="/fecha",
        controls=[layout_final],
        padding=0
    )


def vista_tamano(page: ft.Page, use_cases: PedidoUseCases):
    use_cases.obtener_tamanos()
    pedido_actual = use_cases.obtener_pedido_actual()
    texto_tamano = ft.Text(
        value=pedido_actual.tamano_pastel or "N/A",
        size=48, font_family="Bebas Neue", color="#623F19", text_align=ft.TextAlign.CENTER
    )

    def anterior(e):
        use_cases.seleccionar_anterior_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    def siguiente(e):
        use_cases.seleccionar_siguiente_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    banner_superior = ft.Container(
        height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                        font_family="Bebas Neue")
    )
    panel_interactivo = ft.Container(
        width=524, height=369,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(50),
        shadow=ft.BoxShadow(
            spread_radius=8, blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK), offset=ft.Offset(4, 4),
        ),
        padding=30,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    '¿Para cuántas personas es tu pastel?',
                    size=38, font_family="Bebas Neue", color="#815E43",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.Container(
                    width=263, height=75,
                    border=ft.border.all(5, color=ft.Colors.with_opacity(0.77, "#623F19")),
                    border_radius=ft.border_radius.all(20),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, icon_size=30, on_click=anterior),
                            ft.Container(content=texto_tamano, expand=True, alignment=ft.alignment.center),
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, icon_size=30, on_click=siguiente),
                        ]
                    )
                ),
                ft.Container(height=15),
                ft.Row([
                    #ft.ElevatedButton("Volver", on_click=lambda _: page.go("/fecha")),
                    ft.Container(
                        width=108, height=35, bgcolor="#E5ADAD",
                        border_radius=ft.border_radius.all(10),
                        content=ft.Text("Continuar", color=ft.Colors.WHITE, size=20, font_family="Bebas Neue"),
                        alignment=ft.alignment.center,
                        on_click=lambda _: page.go("/categorias"),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True,
                         content=ft.Column(
                             alignment=ft.MainAxisAlignment.CENTER,
                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                             controls=[
                                 ft.Image(src="Logo Pepe.png", width=424, height=254),
                                 ft.Container(height=30),
                                 panel_interactivo,
                             ]
                         )
                         )
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/tamano",
        controls=[layout_final],
        padding=0
    )


def vista_categorias(page: ft.Page, use_cases: PedidoUseCases):

    def seleccionar_y_avanzar(id_categoria: int):
        use_cases.seleccionar_categoria(id_categoria)
        page.go("/forma")

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
                        content=ft.Image(src="C:/KioscoPP/img/categorias/{}".format(categoria.imagen_url), fit=ft.ImageFit.COVER)
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

    carrusel = ft.Row(
        controls=tarjetas_categorias,
        spacing=30,
        scroll=ft.ScrollMode.ALWAYS
    )

    contenido_principal = ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                col={"sm": 12},
                alignment=ft.MainAxisAlignment.CENTER,
                #wrap=True,
                spacing=30,
                run_spacing=30,
                controls=tarjetas_categorias
            )
        ]
    )

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

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.2, "#DC6262"), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/categorias",
        controls=[layout_final],
        padding=0
    )


def vista_forma(page: ft.Page, use_cases: PedidoUseCases):
    boton_continuar = ft.ElevatedButton("Continuar", disabled=True, on_click=lambda _: page.go("/pan"))

    def on_forma_selected(e):
        use_cases.seleccionar_tipo_forma(e.control.data)
        for card in carrusel_formas.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None
        boton_continuar.disabled = False
        page.update()

    def restablecer(e):
        use_cases.reiniciar_forma()
        for card in carrusel_formas.controls: card.border = None
        boton_continuar.disabled = True
        page.update()

    carrusel_formas = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    for forma in use_cases.obtener_formas_por_categoria(use_cases.obtener_pedido_actual().id_categoria):
        carrusel_formas.controls.append(crear_tarjeta_seleccion(forma.nombre, "C:/KioscoPP/img/formas/{}".format(forma.imagen_url), on_forma_selected))

    return crear_vista_con_fondo(
        ruta="/forma",
        titulo="Paso 3.1: Elige la Forma",
        contenido=[carrusel_formas],
        page=page,
        boton_volver_ruta="/categorias",
        boton_continuar=boton_continuar,
        boton_restablecer=ft.ElevatedButton("Restablecer", on_click=restablecer)
    )


def vista_pan(page: ft.Page, use_cases: PedidoUseCases):
    boton_continuar = ft.ElevatedButton("Continuar", disabled=True, on_click=lambda _: page.go("/relleno"))

    def on_pan_selected(e):
        id_pan, nombre_pan = e.control.data
        use_cases.seleccionar_tipo_pan(nombre_pan)
        for card in carrusel_panes.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None
        boton_continuar.disabled = False
        page.update()

    def restablecer(e):
        use_cases.reiniciar_pan()
        for card in carrusel_panes.controls: card.border = None
        boton_continuar.disabled = True
        page.update()

    carrusel_panes = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    for pan in use_cases.obtener_panes_por_categoria(use_cases.obtener_pedido_actual().id_categoria):
        tarjeta_pan = crear_tarjeta_seleccion(pan.nombre, "C:/KioscoPP/img/panes/{}".format(pan.imagen_url),
                                              on_pan_selected)
        tarjeta_pan.data = (pan.id, pan.nombre)
        carrusel_panes.controls.append(tarjeta_pan)

    return crear_vista_con_fondo(
        ruta="/pan",
        titulo="Paso 3.2: Elige el Pan",
        contenido=[carrusel_panes],
        page=page,
        boton_volver_ruta="/forma",
        boton_continuar=boton_continuar,
        boton_restablecer=ft.ElevatedButton("Restablecer", on_click=restablecer)
    )


# --- VISTA DE RELLENO (REDISEÑADA) ---
def vista_relleno(page: ft.Page, use_cases: PedidoUseCases):
    boton_continuar = ft.ElevatedButton("Continuar", disabled=True, on_click=lambda _: page.go("/cobertura"))

    def on_relleno_selected(e):
        use_cases.seleccionar_tipo_relleno(e.control.data)
        for card in carrusel_rellenos.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None
        boton_continuar.disabled = False
        page.update()

    def restablecer(e):
        use_cases.reiniciar_relleno()
        for card in carrusel_rellenos.controls: card.border = None
        boton_continuar.disabled = True
        page.update()

    carrusel_rellenos = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    pedido = use_cases.obtener_pedido_actual()
    pan_obj = next(
        (p for p in use_cases.obtener_panes_por_categoria(pedido.id_categoria) if p.nombre == pedido.tipo_pan), None)

    if pan_obj:
        for relleno in use_cases.obtener_rellenos_disponibles(pedido.id_categoria, pan_obj.id):
            carrusel_rellenos.controls.append(
                crear_tarjeta_seleccion(relleno.nombre, "C:/KioscoPP/img/rellenos/{}".format(relleno.imagen_url),
                                        on_relleno_selected))

    return crear_vista_con_fondo(
        ruta="/relleno",
        titulo="Paso 3.3: Elige el Relleno",
        contenido=[carrusel_rellenos],
        page=page,
        boton_volver_ruta="/pan",
        boton_continuar=boton_continuar,
        boton_restablecer=ft.ElevatedButton("Restablecer", on_click=restablecer)
    )


def vista_cobertura(page: ft.Page, use_cases: PedidoUseCases):
    boton_continuar = ft.ElevatedButton("Elegir Decorado", on_click=lambda _: page.go("/decorado"), disabled=True)

    def on_cobertura_selected(e):
        use_cases.seleccionar_tipo_cobertura(e.control.data)
        for card in carrusel_coberturas.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None
        boton_continuar.disabled = False
        page.update()

    def restablecer(e):
        use_cases.reiniciar_cobertura()
        for card in carrusel_coberturas.controls: card.border = None
        boton_continuar.disabled = True
        page.update()

    carrusel_coberturas = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    pedido = use_cases.obtener_pedido_actual()
    pan_obj = next(
        (p for p in use_cases.obtener_panes_por_categoria(pedido.id_categoria) if p.nombre == pedido.tipo_pan), None)

    if pan_obj:
        for cobertura in use_cases.obtener_coberturas_disponibles(pedido.id_categoria, pan_obj.id):
            carrusel_coberturas.controls.append(
                crear_tarjeta_seleccion(cobertura.nombre, "C:/KioscoPP/img/coberturas/{}".format(cobertura.imagen_url),
                                        on_cobertura_selected))

    return crear_vista_con_fondo(
        ruta="/cobertura",
        titulo="Paso 4: Elige la Cobertura",
        contenido=[carrusel_coberturas],
        page=page,
        boton_volver_ruta="/relleno",
        boton_continuar=boton_continuar,
        boton_restablecer=ft.ElevatedButton("Restablecer", on_click=restablecer)
    )


def vista_decorado(page: ft.Page, use_cases: PedidoUseCases):
    def crear_tarjeta_decorado(texto: str, on_click_handler, data=None):
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

    campo_mensaje = ft.TextField(
        label="Mensaje en el pastel (opcional)",
        value=use_cases.obtener_pedido_actual().mensaje_pastel or ""
    )
    sub_opciones_container = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=15, alignment=ft.MainAxisAlignment.CENTER)
    tematica_container = ft.Column(
        visible=False,
        controls=[
            ft.TextField(label="Escribe la temática o personaje"),
            ft.Text("El material que se usará será acetato y no es comestible.", italic=True, size=12,
                    color=ft.Colors.WHITE)
        ]
    )
    dd_color1 = ft.Dropdown(label="Color Principal", expand=True)
    dd_color2 = ft.Dropdown(label="Color Secundario (opcional)", expand=True)
    contenedor_colores = ft.Row(controls=[dd_color1, dd_color2], visible=False)

    boton_continuar = ft.ElevatedButton("Continuar a Extras", on_click=lambda _: page.go("/extras"), visible=False)

    def check_continuar():
        pedido = use_cases.obtener_pedido_actual()
        listo = False
        if pedido.tipo_decorado == "Liso c/s Conchas de Betún":
            if pedido.decorado_liso_detalle and pedido.decorado_liso_color1:
                if pedido.decorado_liso_detalle == "Diseño o Temática":
                    if pedido.decorado_tematica_detalle:
                        listo = True
                else:
                    listo = True
        elif pedido.tipo_decorado == "Imágenes Predeterminadas":
            # La navegación es directa, así que no se necesita este botón.
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
            btn.border = ft.border.all(3, ft.Colors.GREEN_500) if btn == e.control else None

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

        for btn in opciones_principales_row.controls:
            btn.border = ft.border.all(3, ft.Colors.GREEN_500) if btn == e.control else None

        if tipo_decorado == "Imágenes Predeterminadas":
            page.go("/galeria")
            return

        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        tematica_container.visible = False
        boton_continuar.visible = False

        detalles_liso = ["Chantilli", "Chorreado", "Diseño o Temática"]
        for opcion in detalles_liso:
            sub_opciones_container.controls.append(
                crear_tarjeta_decorado(opcion, on_sub_opcion_liso_click)
            )
        page.update()

    def restablecer_decorado(e):
        use_cases.reiniciar_decorado()
        for card in opciones_principales_row.controls:
            card.border = None

        sub_opciones_container.controls.clear()
        tematica_container.visible = False
        contenedor_colores.visible = False
        boton_continuar.visible = False
        campo_mensaje.value = ""
        page.update()

    opciones_principales_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            crear_tarjeta_decorado("Liso c/s Conchas de Betún", on_decorado_principal_click),
            crear_tarjeta_decorado("Imágenes Predeterminadas", on_decorado_principal_click),
        ]
    )

    contenido_vista = [
        campo_mensaje,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Text("Elige un estilo de decoración:", color=ft.Colors.WHITE),
        opciones_principales_row,
        ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
        sub_opciones_container,
        tematica_container,
        contenedor_colores,
    ]

    return crear_vista_con_fondo(
        ruta="/decorado",
        titulo="Paso 5: Elige el Decorado",
        contenido=contenido_vista,
        page=page,
        boton_volver_ruta="/cobertura",
        boton_continuar=boton_continuar,
        boton_restablecer=ft.ElevatedButton("Restablecer", on_click=restablecer_decorado)
    )


def vista_galeria(page: ft.Page, use_cases: PedidoUseCases):
    grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=180,  # Un poco más de espacio para las imágenes
        child_aspect_ratio=0.8,  # Ajustado para imagen + texto
        spacing=10,
        run_spacing=10
    )

    def on_image_click(e):
        id_imagen_seleccionada = e.control.data
        use_cases.seleccionar_imagen_decorado(id_imagen_seleccionada)
        page.go("/extras")

    def actualizar_galeria(e=None):
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
                    )
                )
            )
        page.update()

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

    actualizar_galeria()

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
    campo_cantidad_flores = ft.TextField(
        label="Cantidad",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
        visible=False  # Empieza oculto
    )

    def on_cantidad_change(e):
        valor = e.control.value
        if valor:
            try:
                cantidad = int(valor)
                if not (1 <= cantidad <= 10):
                    e.control.error_text = "Max. 10"
                    use_cases.guardar_cantidad_flor(None)  # Guardamos nulo si es inválido
                else:
                    e.control.error_text = None
                    use_cases.guardar_cantidad_flor(cantidad)  # Guardamos la cantidad válida
            except ValueError:
                e.control.error_text = "Inválido"
                use_cases.guardar_cantidad_flor(None)
        else:
            e.control.error_text = None
            use_cases.guardar_cantidad_flor(None)

        page.update()

    campo_cantidad_flores.on_change = on_cantidad_change

    def on_radio_change(e):
        seleccion = e.control.value
        use_cases.seleccionar_extra(seleccion if seleccion != "Ninguno" else None)

        if seleccion == "Flor Artificial":
            campo_cantidad_flores.visible = True
        else:
            campo_cantidad_flores.visible = False
            campo_cantidad_flores.value = ""
            campo_cantidad_flores.error_text = None

        page.update()

    opcion_flor_artificial = ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Radio(value="Flor Artificial"),
            ft.Text("Flor Artificial", size=20, font_family="Montserrat Alternates", weight=ft.FontWeight.W_600),
            campo_cantidad_flores
        ]
    )

    opciones_extra = ft.RadioGroup(
        on_change=on_radio_change,
        value=use_cases.obtener_pedido_actual().extra_seleccionado or "Ninguno",
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row([
                    ft.Radio(value="Ninguno"),
                    ft.Text("Ninguno", size=20, font_family="Montserrat Alternates", weight=ft.FontWeight.W_600)
                ]),
                opcion_flor_artificial,
                ft.Row([
                    ft.Radio(value="Chorreado dorado"),
                    ft.Text("Chorreado Dorado", size=20, font_family="Montserrat Alternates",
                            weight=ft.FontWeight.W_600)
                ]),
                ft.Row([
                    ft.Radio(value="Chorreado plateado"),
                    ft.Text("Chorreado Plateado", size=20, font_family="Montserrat Alternates",
                            weight=ft.FontWeight.W_600)
                ]),
            ]
        )
    )

    panel_interactivo = ft.Container(
        width=524,
        padding=30,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(50),
        shadow=ft.BoxShadow(
            spread_radius=8, blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(4, 4),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    '¿Deseas algún extra?',
                    size=35,
                    font_family="Cabin",
                    weight=ft.FontWeight.W_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                opciones_extra,
            ]
        )
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(  # Banner superior
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                                font_family="Bebas Neue")
            ),
            # Espaciador flexible para empujar el contenido hacia el centro
            ft.Container(expand=True),

            # El logo/imagen
            ft.Image(src="Logo Pepe.png", width=424, height=254),

            # El panel interactivo con las opciones
            panel_interactivo,

            # Espaciador flexible para empujar los botones hacia abajo
            ft.Container(expand=True),

            # Fila de botones de navegación
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.ElevatedButton("Volver", on_click=lambda _: page.go("/decorado")),
                    ft.ElevatedButton("Ver Resumen", on_click=lambda _: page.go("/datos_cliente")),
                ]
            ),
            ft.Container(height=30)  # Un pequeño margen inferior
        ]
    )

    # El Stack se usa solo para el fondo
    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/extras",
        controls=[layout_final],
        padding=0
    )


def vista_datos_cliente(page: ft.Page, use_cases: PedidoUseCases, finalizar_use_cases: FinalizarPedidoUseCases):
    # --- 1. Estado y Referencias ---
    campo_enfocado = ft.Ref[ft.TextField]()
    logo_ref = ft.Ref[ft.Image]()
    titulo_ref = ft.Ref[ft.Text]()

    # --- 2. Lógica y Manejadores ---
    def on_keyboard_key(key: str):
        target = campo_enfocado.current
        if not target: return
        if key == "BACKSPACE":
            target.value = target.value[:-1] if target.value else ""
        else:
            target.value += key
        page.update()

    def ocultar_teclado(e):
        teclado_virtual.keyboard_control.visible = False
        if logo_ref.current: logo_ref.current.visible = True
        if titulo_ref.current: titulo_ref.current.visible = True
        page.update()

    def mostrar_teclado():
        teclado_virtual.keyboard_control.visible = True
        if logo_ref.current: logo_ref.current.visible = False
        if titulo_ref.current: titulo_ref.current.visible = False
        page.update()

    def on_textfield_focus(e):
        campo_enfocado.current = e.control
        mostrar_teclado()

    def finalizar_pedido(e):
        ocultar_teclado(e)
        use_cases.guardar_datos_cliente(
            nombre=nombre.value,
            telefono=telefono.value,
            direccion=direccion.value,
            num_ext=num_ext.value,
            entre_calles=entre_calles.value,
            cp=cp.value,
            colonia=colonia.value,
            ciudad=ciudad.value,
            municipio=municipio.value,
            estado=estado.value,
            referencias=referencias.value
        )
        # if finalizar_use_cases.finalizar_y_obtener_ticket():
        page.go("/confirmacion")
        # else:
        #     page.snack_bar = ft.SnackBar(ft.Text("Error al finalizar el pedido."), bgcolor=ft.Colors.RED)
        #     page.snack_bar.open = True
        #     page.update()

    teclado_virtual = VirtualKeyboard(
        page,
        on_key=on_keyboard_key,
        on_hide=ocultar_teclado,
        on_enter=finalizar_pedido
    )
    teclado_virtual.keyboard_control.visible = False

    # --- 3. Construcción de Componentes ---
    def crear_campo_texto(label: str, expand=False, multiline=False, min_lines=1):
        return ft.TextField(
            label=label, on_focus=on_textfield_focus,
            border=ft.InputBorder.NONE, bgcolor=ft.Colors.WHITE,
            border_radius=14, expand=expand, content_padding=15,
            multiline=multiline, min_lines=min_lines
        )

    nombre = crear_campo_texto("Nombre completo", expand=True)
    telefono = crear_campo_texto("Teléfono")
    direccion = crear_campo_texto("Dirección (calle)", expand=True)
    num_ext = crear_campo_texto("Número exterior")
    cp = crear_campo_texto("Código postal")
    colonia = crear_campo_texto("Colonia", expand=True)
    entre_calles = crear_campo_texto("Entre calles", expand=True)
    ciudad = crear_campo_texto("Ciudad", expand=True)
    municipio = crear_campo_texto("Municipio", expand=True)
    estado = crear_campo_texto("Estado")
    referencias = crear_campo_texto("Referencias del domicilio", multiline=True, min_lines=3)

    # --- 4. Construcción del Layout ---
    logo = ft.Image(ref=logo_ref, src="Logo Pepe.png", width=250)
    titulo = ft.Text(ref=titulo_ref, value="Datos de entrega", size=40, color=ft.Colors.WHITE, font_family="Cabin",
                     weight=ft.FontWeight.W_700)

    panel_formulario = ft.Container(
        width=628,
        bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.WHITE),
        border_radius=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
        padding=25,
        content=ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=12,
            controls=[
             ft.Row([nombre]),
             ft.Row([telefono]),
             ft.Row([direccion]),
             ft.Row([num_ext, cp]),
             ft.Row([colonia]),
             ft.Row([entre_calles]),
             ft.Row([ciudad, municipio]),
             ft.Row([estado]),
             referencias,
            ]
        )
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                        ft.Text('PARA ENVÍO GRATUITO EN COMPRAS DE $500 O MÁS', color=ft.Colors.WHITE,
                                font_family="Bebas Neue", size=24),
                        ft.IconButton(ft.Icons.HOME_OUTLINED, icon_color=ft.Colors.WHITE,
                                      on_click=lambda _: page.go("/")),
                    ]
                )
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo,
                    titulo,
                    ft.Container(height=15),
                    panel_formulario,
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Container(width=188, height=76, bgcolor="#89C5B0", border_radius=15,
                                 alignment=ft.alignment.center, on_click=lambda _: page.open_summary(None),
                                 content=ft.Text("Ver resumen", color=ft.Colors.WHITE, size=24, font_family="Outfit",
                                                 weight=ft.FontWeight.W_600)),
                    ft.Container(width=233, height=76, bgcolor="#DC6262", border_radius=15,
                                 alignment=ft.alignment.center, on_click=finalizar_pedido,
                                 content=ft.Text("Finalizar pedido", color=ft.Colors.WHITE, size=24,
                                                 font_family="Outfit", weight=ft.FontWeight.W_600)),
                ]
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/datos_cliente",
        padding=0,
        controls=[
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(content=layout_final, expand=True),
                    teclado_virtual.build()
                ]
            )
        ]
    )


def vista_confirmacion(page: ft.Page, use_cases: FinalizarPedidoUseCases, pedido_use_cases: PedidoUseCases):
    ticket_finalizado = use_cases.finalizar_y_obtener_ticket()

    if ticket_finalizado:
        use_cases.imprimir_ticket_por_folio(ticket_finalizado.id_pedido)

    def animar_entrada():
        import time
        time.sleep(0.1)

        logo.opacity = 1
        circulo_verificacion.opacity = 1
        titulo.opacity = 1
        folio.opacity = 1
        gracias.opacity = 1
        botones.opacity = 1
        page.update()

    def nuevo_pedido(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")

    def abrir_detalle_pedido(e):
        """Construye y muestra el BottomSheet de detalle del pedido."""


        # Obtenemos el nombre de la categoría para mostrarlo
        # (Necesitaríamos pasar PedidoUseCases a vista_confirmacion o refactorizar)
        # Por ahora, un placeholder.
        categorias = {c.id: c.nombre for c in pedido_use_cases.obtener_categorias()}
        nombre_categoria = categorias.get(ticket_finalizado.id_categoria, "N/A")

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

        # Construimos dinámicamente el contenido del BottomSheet
        bs_detalle = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            #controls=[ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda _: bs_detalle.set_attrs(open=False) or page.update())]
                            controls=[ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda _: setattr(bs_detalle, 'open',
                                                                                                    False) or page.update())]
                        ),
                        ft.Text(f"Detalle del Pedido #{ticket_finalizado.id_pedido}", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Row(
                            controls=[
                                ft.Column([
                                    crear_fila_resumen("categoria.png", "Categoría", nombre_categoria),
                                    crear_fila_resumen("forma.png", "Forma", ticket_finalizado.tipo_forma),
                                    crear_fila_resumen("relleno.png", "Relleno", ticket_finalizado.tipo_relleno),
                                ], expand=1),
                                ft.Column([
                                    crear_fila_resumen("tamano.png", "Tamaño", ticket_finalizado.tamano_pastel),
                                    crear_fila_resumen("pan.png", "Pan", ticket_finalizado.tipo_pan),
                                    crear_fila_resumen("cobertura.png", "Cobertura", ticket_finalizado.tipo_cobertura),
                                ], expand=1),
                            ]
                        ),
                        ft.Divider(height=10),
                        ft.Text(
                            f"Fecha de entrega: {ticket_finalizado.fecha_entrega} a las {ticket_finalizado.hora_entrega}"),
                        ft.Text(f"Cliente: {ticket_finalizado.nombre_cliente} ({ticket_finalizado.telefono_cliente})"),
                        ft.Text(
                            f"Dirección: {ticket_finalizado.direccion_cliente} #{ticket_finalizado.num_ext_cliente}, {ticket_finalizado.colonia_cliente}, {ticket_finalizado.ciudad_cliente}, {ticket_finalizado.estado_cliente}, CP: {ticket_finalizado.cp_cliente}"),
                        # No hay botón de restablecer aquí
                    ]
                ),
                padding=20
            ),
            open=True,  # Lo abrimos inmediatamente
            on_dismiss=lambda _: page.update()  # Para que la página se actualice al cerrar
        )
        page.overlay.append(bs_detalle)
        page.update()


    if not ticket_finalizado:
        vista_error = ft.View(
            "/confirmacion",
            [
                ft.Text("Error al generar el ticket.", color=ft.Colors.RED),
                ft.ElevatedButton("Volver", on_click=lambda _: page.go("/datos_cliente"))
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return vista_error, lambda: None

    logo = ft.Image(src="Logo Pepe.png", width=424, height=254, opacity=0, animate_opacity=300)

    titulo = ft.Text("¡Pedido confirmado!", size=45, font_family="Outfit", weight=ft.FontWeight.W_700,
                     text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE, opacity=0, animate_opacity=500)

    circulo_verificacion = ft.Container(
        width=150, height=150,
        shape=ft.BoxShape.CIRCLE,
        bgcolor="#DC6262",
        alignment=ft.alignment.center,
        content=ft.Icon(name=ft.Icons.CHECK, color=ft.Colors.WHITE, size=70),
        opacity=0, animate_opacity=700
    )

    folio = ft.Text(f"Número de folio: {ticket_finalizado.id_pedido}", size=30, font_family="Outfit",
                    text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE, opacity=0, animate_opacity=700)
    gracias = ft.Text(f"Gracias: {ticket_finalizado.nombre_cliente}", size=35, font_family="Outfit", weight=ft.FontWeight.W_500,
                      text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE, opacity=0, animate_opacity=900)

    botones = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        opacity=0,
        animate_opacity=1300,
        controls=[
            ft.Container(
            alignment=ft.alignment.bottom_center,
            padding=50,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Container(
                        width=250, height=60, bgcolor="#89C5B0", border_radius=15,
                        content=ft.Text("Iniciar nuevo pedido", color=ft.Colors.WHITE, size=30),
                        alignment=ft.alignment.center, on_click=nuevo_pedido
                    ),
                    ft.Container(
                        width=250, height=60, bgcolor="#C16160", border_radius=15,
                        content=ft.Text("Detalle del pedido", color=ft.Colors.WHITE, size=30),
                        alignment=ft.alignment.center, on_click=abrir_detalle_pedido
                    ),
                ]
            )
        )]

    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src="929f8d1fff68e3deddd0d09b79812005b5683447.png", fit=ft.ImageFit.COVER, expand=True),

            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Container(height=20),
                    logo,
                    ft.Container(height=5),
                    titulo,
                    ft.Container(height=15),
                    circulo_verificacion,
                    ft.Container(height=15),
                    folio,
                    gracias,
                    ft.Container(height=30, expand=True),
                    botones,
                    ft.Container(height=20),
                ]
            ),
        ]
    )

    vista = ft.View(
        route="/confirmacion",
        controls=[layout_final],
        padding=0
    )

    return vista, animar_entrada
