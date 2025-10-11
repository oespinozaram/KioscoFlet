import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
from src.application.use_cases import PedidoUseCases, FinalizarPedidoUseCases
from .keyboard import VirtualKeyboard
from .controles_comunes import crear_boton_navegacion
from src.application.use_cases import AuthUseCases
import logging

logger = logging.getLogger(__name__)


fondo_hd = 'C:/KioscoPP/img/fondo_hd.png'
logo_pepe = 'C:/KioscoPP/img/logo.png'
chef = 'C:/KioscoPP/img/chef.png'


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
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
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
        #on_focus=on_textfield_focus
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
        #on_focus=on_textfield_focus
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
        src=chef,
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
        src=logo_pepe,
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
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            banner_superior,

            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        imagen_pastel,
                        texto_bienvenida,
                        texto_subtitulo,
                        ft.Container(height=20),
                        boton_comenzar,
                    ]
                )
            ),
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(
                src=fondo_hd,
                fit=ft.ImageFit.FILL,
                expand=True,
            ),
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.50, ft.Colors.BLACK),
                expand=True,
            ),
            banner_superior,
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
            # crear_tarjeta_opcion(
            #     titulo="Conoce nuestro catálogo\ny promociones",
            #     imagen_src="seleccion/promos.png",
            #     on_click_handler=lambda _: print("Navegando a promociones...")
            # ),
            crear_tarjeta_opcion(
                titulo="Arma y Personaliza\ntu Pastel",
                imagen_src="C:/KioscoPP/img/seleccion/arma.png",
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
        src=logo_pepe,
        fit=ft.ImageFit.CONTAIN,
        width=424, height=254,  # Altura máxima para la imagen
    )


    boton_volver = crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/"),
                            es_primario=False
                        )


    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),
            imagen_pastel,
            ft.Container(expand=True),
            contenido_principal,
            ft.Container(height=40),
            boton_volver,
            ft.Container(height=40),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
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
            '%d/%m/%Y') if use_cases.obtener_pedido_actual().fecha_entrega else "Toca para seleccionar",
        size=30, font_family="Bebas Neue", weight=ft.FontWeight.W_400, color=ft.Colors.BLACK54,
    )

    dropdown_hora = ft.Dropdown(
        hint_text="Elige un rango de hora", options=[], disabled=True,
        border_color="#DBCACA", width=300, text_size=18
    )

    texto_error = ft.Text(value="", color=ft.Colors.RED, visible=False, size=20, weight=ft.FontWeight.BOLD)

    def on_date_change(e):
        fecha = e.control.value.date()
        use_cases.seleccionar_fecha(fecha)
        texto_fecha_seleccionada.value = fecha.strftime('%d/%m/%Y')

        dropdown_hora.value = None
        dropdown_hora.options.clear()
        use_cases.seleccionar_hora(None)

        nuevos_rangos = use_cases.obtener_rangos_de_hora(fecha)

        if nuevos_rangos:
            dropdown_hora.options = [ft.dropdown.Option(r) for r in nuevos_rangos]
            dropdown_hora.disabled = False
        else:
            dropdown_hora.hint_text = "No hay horarios"
            dropdown_hora.disabled = True

        texto_error.visible = False
        page.update()

    def on_time_change(e):
        use_cases.seleccionar_hora(e.control.value)
        texto_error.visible = False
        page.update()

    dropdown_hora.on_change = on_time_change

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

    boton_volver = crear_boton_navegacion(
                            texto="Volver",
                            on_click_handler=lambda _: page.go("/seleccion"),
                            es_primario=False
                        )

    def continuar(e):
        pedido = use_cases.obtener_pedido_actual()
        if not pedido.fecha_entrega or not pedido.hora_entrega:
            texto_error.value = "Debes seleccionar fecha y hora."
            texto_error.visible = True
            page.update()
        else:
            page.go("/tamano")

    boton_continuar = crear_boton_navegacion(
                            texto="Continuar",
                            on_click_handler=continuar,
                            es_primario=True
                        )

    banner_superior = ft.Container(
        height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                        font_family="Bebas Neue")
    )

    contenido_formulario = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Paso 1: Elige Fecha y Hora", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(
                on_click=open_date_picker,
                padding=15, border=ft.border.all(2, ft.Colors.with_opacity(0.5, "#DBCACA")),
                border_radius=10, bgcolor=ft.Colors.WHITE,
                width=400,
                content=ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_MONTH, color="#673C1C"),
                    ft.Text("Fecha:", size=30, font_family="Bebas Neue", weight=ft.FontWeight.W_400),
                    texto_fecha_seleccionada
                ])
            ),
            dropdown_hora,
            texto_error,
        ]
    )

    panel_principal = ft.Container(
        width=500,
        padding=30,
        border_radius=ft.border_radius.all(35),
        bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=20, color=ft.Colors.BLACK26),
        content=contenido_formulario
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Image(src=logo_pepe, width=424, height=254,),
                        panel_principal
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    boton_volver,
                    boton_continuar,
                ]
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
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

    def restablecer_pedido_completo(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")

    banner_superior = ft.Container(
        height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
        content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                        font_family="Bebas Neue")
    )

    panel_interactivo = ft.Container(
        width=524,
        padding=ft.padding.only(top=30),
        bgcolor=ft.Colors.with_opacity(0.90, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(50),
        shadow=ft.BoxShadow(
            spread_radius=8, blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(4, 4),
        ),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            '¿Para cuántas personas es tu pastel?',
                            size=38, font_family="Bebas Neue", color="#815E43",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=20),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Container(
                                    width=300, height=75,
                                    border=ft.border.all(5, color=ft.Colors.with_opacity(0.77, "#623F19")),
                                    border_radius=ft.border_radius.all(20),
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, icon_size=30,
                                                          on_click=anterior),
                                            ft.Container(content=texto_tamano, expand=True,
                                                         alignment=ft.alignment.center),
                                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, icon_size=30,
                                                          on_click=siguiente),
                                        ]
                                    )
                                ),
                                ft.Text("Personas", size=18, weight=ft.FontWeight.BOLD, color="#815E43")
                            ]
                        ),
                    ]
                ),

                ft.Container(
                    padding=ft.padding.only(bottom=15),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            crear_boton_navegacion(
                                texto="Volver",
                                on_click_handler=lambda _: page.go("/fecha"),
                                es_primario=False
                            ),
                            crear_boton_navegacion(
                                texto="Restablecer",
                                on_click_handler=restablecer_pedido_completo,
                                es_primario=False,
                                bgcolor=ft.Colors.AMBER_300
                            ),
                            crear_boton_navegacion(
                                texto="Continuar",
                                on_click_handler=lambda _: page.go("/categorias"),
                                es_primario=True
                            )
                        ]
                    )
                )
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
                                 ft.Image(src=logo_pepe, width=424, height=254),
                                 ft.Container(height=20),
                                 ft.Text("Paso 2: Elige El Tamaño del Pastel", size=40, weight=ft.FontWeight.BOLD,
                                         color=ft.Colors.WHITE),
                                 ft.Container(height=30),
                                 panel_interactivo,
                             ]
                         )
                         )
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/tamano",
        controls=[layout_final],
        padding=0
    )


def vista_categorias(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    imagen_logo = ft.Image(
        src=logo_pepe,
        fit=ft.ImageFit.CONTAIN,
        width=424, height=254,
    )

    def on_categoria_selected(e):
        id_categoria = e.control.data
        use_cases.seleccionar_categoria(id_categoria)

        for card in carrusel.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False

        page.update()

    def crear_tarjeta_categoria(categoria):
        return ft.Container(
            width=226,
            height=314,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(30),
            shadow=ft.BoxShadow(
                spread_radius=2, blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(6, 6)
            ),
            on_click=on_categoria_selected,
            data=categoria.id,
            content=ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=176, height=119,
                        margin=ft.margin.only(top=25),
                        border_radius=ft.border_radius.all(10),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=f"C:/KioscoPP/img/categorias/{categoria.imagen_url}", fit=ft.ImageFit.COVER)
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Text(
                        categoria.nombre,
                        text_align=ft.TextAlign.CENTER,
                        size=20,
                        font_family="Bebas Neue"
                    ),
                ]
            )
        )

    lista_categorias = use_cases.obtener_categorias()
    carrusel = ft.Row(
        controls=[crear_tarjeta_categoria(cat) for cat in lista_categorias],
        spacing=30,
        scroll=ft.ScrollMode.ALWAYS
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),

            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        imagen_logo,
                        ft.Container(height=10),
                        ft.Text("Paso 3: Elige la Categoría", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/tamano"),
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/forma"),
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(
                alignment=ft.alignment.center,
                padding=5,
                content=ft.Text(
                    "Imágenes ilustrativas diferentes al producto que representan.",
                    size=22,
                    color=ft.Colors.GREY_300,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/categorias",
        controls=[layout_final],
        padding=0
    )


def vista_forma(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_forma_selected(e):
        forma_seleccionada = e.control.data
        use_cases.seleccionar_tipo_forma(forma_seleccionada.id, forma_seleccionada.nombre)

        for card in carrusel_formas.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False

        page.update()

    def restablecer(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")


    carrusel_formas = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria

    for forma in use_cases.obtener_formas_por_categoria(id_categoria_actual):
        tarjeta = crear_tarjeta_seleccion(forma.nombre, f"C:/KioscoPP/img/formas/{forma.imagen_url}", on_forma_selected)
        tarjeta.data = forma
        carrusel_formas.controls.append(tarjeta)

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 4: Elige la Forma", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel_formas
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/categorias"),  # Debe ir a /categorias
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Restablecer",
                        on_click_handler=restablecer,
                        es_primario=False,
                        bgcolor=ft.Colors.AMBER_300
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/pan"),  # Debe ir a /pan
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(
                alignment=ft.alignment.center,
                padding=5,
                content=ft.Text(
                    "Imágenes ilustrativas diferentes al producto que representan.",
                    size=22,
                    color=ft.Colors.GREY_300,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/forma",
        controls=[layout_final],
        padding=0
    )


def vista_pan(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_pan_selected(e):
        id_pan, nombre_pan = e.control.data
        use_cases.seleccionar_tipo_pan(id_pan, nombre_pan)

        for card in carrusel_panes.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False

        page.update()

    def restablecer(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")

    carrusel_panes = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria

    for pan in use_cases.obtener_panes_por_categoria(id_categoria_actual):
        tarjeta_pan = crear_tarjeta_seleccion(pan.nombre, "C:/KioscoPP/img/panes/{}".format(pan.imagen_url),
                                              on_pan_selected)
        tarjeta_pan.data = (pan.id, pan.nombre)
        carrusel_panes.controls.append(tarjeta_pan)


    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 5: Elige el Pan", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel_panes
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/forma"),
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Restablecer",
                        on_click_handler=restablecer,
                        es_primario=False,
                        bgcolor=ft.Colors.AMBER_300
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/relleno"),
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(
                alignment=ft.alignment.center,
                padding=5,
                content=ft.Text(
                    "Imágenes ilustrativas diferentes al producto que representan.",
                    size=22,
                    color=ft.Colors.GREY_300,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/pan",
        controls=[layout_final],
        padding=0
    )


def vista_relleno(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_relleno_selected(e):
        use_cases.seleccionar_tipo_relleno(e.control.data)
        for card in carrusel_rellenos.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False
        page.update()

    def restablecer(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")

    carrusel_rellenos = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    pedido = use_cases.obtener_pedido_actual()
    pan_obj = next((p for p in use_cases.obtener_panes_por_categoria(pedido.id_categoria) if p.nombre == pedido.tipo_pan), None)
    if pan_obj:
        for relleno in use_cases.obtener_rellenos_disponibles(pedido.id_categoria, pan_obj.id):
            carrusel_rellenos.controls.append(
                crear_tarjeta_seleccion(
                    relleno.nombre, f"C:/KioscoPP/img/rellenos/{relleno.imagen_url}", on_relleno_selected
                )
            )
    else:
        carrusel_rellenos.controls.append(ft.Text("Error: No se pudo determinar el tipo de pan.", color=ft.Colors.RED))

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 6: Elige el Relleno", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel_rellenos
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/pan"),
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Restablecer",
                        on_click_handler=restablecer,
                        es_primario=False,
                        bgcolor=ft.Colors.AMBER_300
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/cobertura"),
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(
                alignment=ft.alignment.center,
                padding=5,
                content=ft.Text(
                    "Imágenes ilustrativas diferentes al producto que representan.",
                    size=22,
                    color=ft.Colors.GREY_300,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/relleno",
        controls=[layout_final],
        padding=0
    )


def vista_cobertura(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_cobertura_selected(e):
        use_cases.seleccionar_tipo_cobertura(e.control.data)
        use_cases.obtener_precio_pastel_configurado()
        for card in carrusel_coberturas.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False
        page.update()

    def restablecer(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")

    carrusel_coberturas = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=30)
    pedido = use_cases.obtener_pedido_actual()
    pan_obj = next((p for p in use_cases.obtener_panes_por_categoria(pedido.id_categoria) if p.nombre == pedido.tipo_pan), None)

    if pan_obj:
        for cobertura in use_cases.obtener_coberturas_disponibles(pedido.id_categoria, pan_obj.id):
            carrusel_coberturas.controls.append(
                crear_tarjeta_seleccion(cobertura.nombre, f"C:/KioscoPP/img/coberturas/{cobertura.imagen_url}",
                                        on_cobertura_selected))
    else:
        carrusel_coberturas.controls.append(ft.Text("Error al cargar coberturas.", color=ft.Colors.RED))


    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 7: Elige la Cobertura", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel_coberturas
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/relleno"),
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Restablecer",
                        on_click_handler=restablecer,
                        es_primario=False,
                        bgcolor=ft.Colors.AMBER_300
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/decorado1"),
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(
                alignment=ft.alignment.center,
                padding=5,
                content=ft.Text(
                    "Imágenes ilustrativas diferentes al producto que representan.",
                    size=22,
                    color=ft.Colors.GREY_300,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/cobertura",
        controls=[layout_final],
        padding=0
    )


def vista_decorado1(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def on_decorado_principal_click(e):
        tipo_decorado = e.control.data
        use_cases.seleccionar_tipo_decorado(tipo_decorado)

        for card in carrusel_decorado.controls:
            card.border = ft.border.all(3, ft.Colors.GREEN_500) if card == e.control else None

        if tipo_decorado == "Imágenes Prediseñadas":
            page.go("/galeria")
            return


        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = False
        page.update()

    def restablecer(e):
        use_cases.reiniciar_decorado()
        for card in carrusel_decorado.controls:
            card.border = None
        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = True
        page.update()

    carrusel_decorado = ft.Row(
        scroll=ft.ScrollMode.ALWAYS,
        spacing=30,
        controls=[
            crear_tarjeta_seleccion("Liso c/s Conchas de Betún", "C:/KioscoPP/img/decorado/liso2.png",
                                    on_decorado_principal_click),
            crear_tarjeta_seleccion("Imágenes Prediseñadas", "C:/KioscoPP/img/decorado/imagenes.png",
                                    on_decorado_principal_click, ),
        ]
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 8: Elige el Estilo", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER),
                        carrusel_decorado
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion(
                        texto="Volver",
                        on_click_handler=lambda _: page.go("/cobertura"),
                        es_primario=False
                    ),
                    crear_boton_navegacion(
                        texto="Restablecer",
                        on_click_handler=restablecer,
                        es_primario=False,
                        bgcolor=ft.Colors.AMBER_300
                    ),
                    crear_boton_navegacion(
                        texto="Continuar",
                        on_click_handler=lambda _: page.go("/decorado2"),
                        ref=ref_boton_continuar,
                        disabled=True
                    )
                ]
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/decorado1",
        controls=[layout_final],
        padding=0
    )


def vista_decorado2(page: ft.Page, use_cases: PedidoUseCases):
    ref_boton_continuar = ft.Ref[ft.Container]()

    def check_continuar():
        print("[DEBUG] VISTA: Verificando si se puede continuar...")
        if ref_boton_continuar.current:
            is_ready = use_cases.check_continuar_decorado()
            ref_boton_continuar.current.disabled = not is_ready
            print(f"[DEBUG] VISTA: Botón 'Continuar' deshabilitado: {not is_ready}")

    def on_text_tematica_change(e):
        print(f"[DEBUG] VISTA: Se escribió en temática: '{e.control.value}'")
        use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", "Diseño o Temática", e.control.value)
        check_continuar()
        page.update()

    def on_color_change(e):
        print(f"[DEBUG] VISTA: Cambió color. Color1='{dd_color1.value}', Color2='{dd_color2.value}'")
        use_cases.seleccionar_colores_decorado(dd_color1.value, dd_color2.value)
        check_continuar()
        page.update()

    def on_sub_opcion_liso_click(e):
        print(f"\n[DEBUG] VISTA: === Clic en sub-opción: '{e.control.data}' ===")
        use_cases.reiniciar_detalles_decorado()

        detalle = e.control.data
        use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle)

        for btn in carrusel_sub_opciones.controls:
            btn.border = ft.border.all(3, ft.Colors.GREEN_500) if btn == e.control else None

        colores_disponibles = use_cases.obtener_colores_disponibles()
        hay_colores = bool(colores_disponibles)

        if hay_colores:
            dd_color1.options = [ft.dropdown.Option(color) for color in colores_disponibles]
            dd_color2.options = [ft.dropdown.Option(color) for color in colores_disponibles]
            dd_color1.value = None
            dd_color2.value = None
        else:
            use_cases.seleccionar_colores_decorado("Sin Selección", None)

        panel_principal.visible = True
        contenedor_colores.visible = hay_colores
        tematica_container.visible = (detalle == "Diseño o Temática")

        check_continuar()
        page.update()
        print("[DEBUG] VISTA: === Fin del clic ===\n")

    def restablecer(e):
        use_cases.reiniciar_detalles_decorado()
        for card in carrusel_sub_opciones.controls: card.border = None
        panel_principal.visible = False
        if ref_boton_continuar.current:
            ref_boton_continuar.current.disabled = True
        page.update()

    tematica_container = ft.Column(
        visible=False,
        controls=[
            ft.TextField(label="Escribe la temática o personaje", on_change=on_text_tematica_change),
            ft.Text("El material será acetato no comestible.", italic=True, size=12, color=ft.Colors.BLACK54)
        ]
    )
    dd_color1 = ft.Dropdown(label="Color Principal", expand=True, on_change=on_color_change)
    dd_color2 = ft.Dropdown(label="Color Secundario (opcional)", expand=True, on_change=on_color_change)
    contenedor_colores = ft.Row(controls=[dd_color1, dd_color2], visible=False)

    carrusel_sub_opciones = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=15)
    detalles_liso = [
        {"nombre": "Chantilli", "imagen": "C:/KioscoPP/img/decorado/chantilli.png"},
        {"nombre": "Chorreado", "imagen": "C:/KioscoPP/img/decorado/chorreado.png"},
        {"nombre": "Diseño o Temática", "imagen": "C:/KioscoPP/img/decorado/tematica.png"},
    ]
    for opcion in detalles_liso:
        carrusel_sub_opciones.controls.append(
            crear_tarjeta_seleccion(opcion["nombre"], opcion["imagen"], on_sub_opcion_liso_click)
        )

    panel_principal = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
        visible=False,
        content=ft.Column(
            spacing=15,
            controls=[
                tematica_container,
                contenedor_colores,

            ]
        )
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=36,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 8.1: Detalla tu Decorado", size=40, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text("Elige un detalle:", color=ft.Colors.WHITE),
                        carrusel_sub_opciones,
                        panel_principal,
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion("Volver", lambda _: page.go("/decorado1"), es_primario=False),
                    crear_boton_navegacion("Restablecer", restablecer, es_primario=False, bgcolor=ft.Colors.AMBER_300),
                    crear_boton_navegacion("Continuar", lambda _: page.go("/mensaje"), ref=ref_boton_continuar,
                                           disabled=True)
                ]
            ),
            ft.Container(height=30)
        ]
    )
    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/decorado2",
        controls=[layout_final],
        padding=0
    )


def vista_galeria(page: ft.Page, use_cases: PedidoUseCases):
    campo_enfocado = ft.Ref[ft.TextField]()

    def on_keyboard_key(key: str):
        target = campo_enfocado.current
        if not target: return
        if key == "BACKSPACE":
            target.value = target.value[:-1] if target.value else ""
        else:
            target.value += key
        actualizar_galeria()
        page.update()

    def on_textfield_focus(e):
        campo_enfocado.current = e.control
        teclado_virtual.keyboard_control.visible = True
        page.update()

    def ocultar_teclado(e):
        teclado_virtual.keyboard_control.visible = False
        page.update()

    teclado_virtual = VirtualKeyboard(
        page,
        on_key=on_keyboard_key,
        on_hide=ocultar_teclado,
        on_enter=ocultar_teclado  # La tecla Enter simplemente oculta el teclado
    )
    teclado_virtual.keyboard_control.visible = False

    grid = ft.GridView(
        expand=True,  # Permitimos que la cuadrícula se expanda
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10
    )

    def on_image_click(e):
        id_imagen_seleccionada = e.control.data
        use_cases.seleccionar_imagen_decorado(id_imagen_seleccionada)
        page.go("/mensaje")

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
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Stack(
                        [
                            ft.Image(
                                src=img.ruta,
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Container(
                                content=ft.Text(img.categoria, color="white", weight=ft.FontWeight.BOLD),
                                # Asumo que es 'nombre' y no 'descripcion'
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                                padding=8,
                                alignment=ft.alignment.bottom_center,
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
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Bodas"),
            ft.dropdown.Option("Bautizos"),
            ft.dropdown.Option("Primera Comunión"),
            ft.dropdown.Option("Niños"),
            ft.dropdown.Option("XV Años"),
            ft.dropdown.Option("Niñas"),
            ft.dropdown.Option("Otros"),
            ft.dropdown.Option("Flores"),
            ft.dropdown.Option("Cumpleaños"),
        ],
        value="Todas",
        on_change=actualizar_galeria,
        expand=True
    )
    campo_busqueda = ft.TextField(
        label="Buscar...",
        on_change=actualizar_galeria,
        #on_focus=on_textfield_focus,
        expand=True
    )

    panel_filtros = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
        border_radius=15,
        padding=15,
        content=ft.Row([filtro_categoria, campo_busqueda])
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(  # Banner superior
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row([
                            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/decorado1"),
                                          tooltip="Volver", icon_color=ft.Colors.WHITE),
                            ft.Text("Galería de Imágenes", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ]),
                        panel_filtros,
                        grid
                    ]
                )
            )
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            ft.Container(bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK), expand=True),
            contenido_superpuesto
        ]
    )

    actualizar_galeria()

    return ft.View(
        route="/galeria",
        controls=[layout_final],
        padding=0
    )


def vista_mensaje(page: ft.Page, use_cases: PedidoUseCases):
    pedido_actual = use_cases.obtener_pedido_actual()
    ruta_volver = "/galeria" if pedido_actual.tipo_decorado == "Imágenes Prediseñadas" else "/decorado2"

    def on_change(e):
        use_cases.guardar_mensaje_y_edad(campo_mensaje.value, campo_edad.value if campo_edad.value else None)

    def restablecer(e):
        use_cases.reiniciar_mensaje_y_edad()
        campo_mensaje.value = ""
        campo_edad.value = ""
        page.update()

    campo_mensaje = ft.TextField(
        label="Mensaje de felicitación (opcional)",
        value=use_cases.obtener_pedido_actual().mensaje_pastel or "",
        on_change=on_change,
        multiline=True,
        min_lines=3,
    )
    campo_edad = ft.TextField(
        label="Años a cumplir (opcional)",
        value=str(use_cases.obtener_pedido_actual().edad_pastel or ""),
        on_change=on_change,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )

    # Panel blanco para los campos
    panel_principal = ft.Container(
        width=500,
        padding=30,
        border_radius=ft.border_radius.all(35),
        bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=20, color=ft.Colors.BLACK26),
        content=ft.Column(
            spacing=20,
            controls=[
                campo_mensaje,
                campo_edad
            ]
        )
    )

    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                height=67, bgcolor="#89C5B0", alignment=ft.alignment.center,
                content=ft.Text('Para envío gratuito en compras de $500 o más', color=ft.Colors.WHITE, size=28,
                                font_family="Bebas Neue")
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=logo_pepe, width=250),
                        ft.Text("Paso 9: Mensaje y Edad", size=40, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                        panel_principal
                    ]
                )
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion("Volver", lambda _: page.go(ruta_volver), es_primario=False),
                    crear_boton_navegacion("Restablecer", restablecer, es_primario=False, bgcolor=ft.Colors.AMBER_300),
                    crear_boton_navegacion("Continuar", lambda _: page.go("/extras"))
                ]
            ),
            ft.Container(height=30)
        ]
    )

    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/mensaje",
        controls=[layout_final],
        padding=0
    )

def vista_extras(page: ft.Page, use_cases: PedidoUseCases):
    texto_precio = ft.Text(value="$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK54)

    def on_cantidad_change(e):
        cantidad_valida = 0
        costo_total = 0
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
                    cantidad_valida = cantidad
            except ValueError:
                e.control.error_text = "Inválido"
                use_cases.guardar_cantidad_flor(None)
        else:
            e.control.error_text = None
            use_cases.guardar_cantidad_flor(None)

        use_cases.guardar_cantidad_flor(cantidad_valida if cantidad_valida > 0 else None)

        # --- CAMBIO: Calcular y mostrar el precio total ---
        pedido_actual = use_cases.obtener_pedido_actual()
        if pedido_actual.extra_precio and cantidad_valida > 0:
            costo_total = pedido_actual.extra_precio * cantidad_valida

        texto_precio.value = f"${costo_total:.2f}"

        page.update()

    campo_cantidad_flores = ft.TextField(
        label="Cantidad",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_cantidad_change,
        visible=False
    )

    campo_cantidad_flores.on_change = on_cantidad_change

    def on_radio_change(e):
        seleccion = e.control.value
        use_cases.seleccionar_extra(seleccion if seleccion != "Ninguno" else None)

        pedido_actual = use_cases.obtener_pedido_actual()
        if pedido_actual.extra_precio:
            texto_precio.value = f"${pedido_actual.extra_precio:.2f}"
        else:
            texto_precio.value = "$0.00"

        if seleccion == "Flor Artificial":
            campo_cantidad_flores.visible = True
            campo_cantidad_flores.value = '1'
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

    def restablecer(e):
        use_cases.iniciar_nuevo_pedido()
        page.go("/")


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
                    ft.Radio(value="Chorreado Dorado"),
                    ft.Text("Chorreado Dorado", size=20, font_family="Montserrat Alternates",
                            weight=ft.FontWeight.W_600)
                ]),
                ft.Row([
                    ft.Radio(value="Chorreado Plateado"),
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
                ft.Divider(height=15),
                ft.Row(
                    [
                        ft.Text("Costo Adicional:", size=20),
                        texto_precio
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
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
            ft.Container(expand=True),

            ft.Image(src=logo_pepe, width=424, height=254),

            panel_interactivo,

            ft.Container(expand=True),

            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    crear_boton_navegacion("Volver", lambda _: page.go("/decorado1"), es_primario=False),
                    crear_boton_navegacion("Restablecer", restablecer, es_primario=False, bgcolor=ft.Colors.AMBER_300),
                    crear_boton_navegacion("Continuar", lambda _: page.go("/datos_cliente")),
                ]
            ),
            ft.Container(height=30)
        ]
    )


    layout_final = ft.Stack(
        controls=[
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/extras",
        controls=[layout_final],
        padding=0
    )


def vista_datos_cliente(page: ft.Page, use_cases: PedidoUseCases, finalizar_use_cases: FinalizarPedidoUseCases):
    campo_enfocado = ft.Ref[ft.TextField]()
    ref_boton_finalizar = ft.Ref[ft.Container]()
    logo_ref = ft.Ref[ft.Image]()
    titulo_ref = ft.Ref[ft.Text]()

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
        campos_requeridos = {
            nombre: "Nombre completo es requerido.",
            telefono: "Teléfono es requerido.",
            direccion: "Dirección es requerida.",
            num_ext: "El número exterior es requerido",
            entre_calles: "Entre calles es requerido.",
            ciudad: "Ciudada es requerida.",
        }

        hay_errores = False
        for campo, mensaje_error in campos_requeridos.items():
            if not campo.value:
                campo.error_text = mensaje_error
                hay_errores = True
            else:
                campo.error_text = None

        if hay_errores:
            page.update()
            return

        ocultar_teclado(e)
        if ref_boton_finalizar.current:
            ref_boton_finalizar.current.disabled = True
            ref_boton_finalizar.current.content.value = "Procesando..."
        page.update()

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
        page.go("/confirmacion")


    teclado_virtual = VirtualKeyboard(
        page,
        on_key=on_keyboard_key,
        on_hide=ocultar_teclado,
        on_enter=finalizar_pedido
    )
    teclado_virtual.keyboard_control.visible = False

    def crear_campo_texto(label: str, expand=False, multiline=False, min_lines=1):
        return ft.TextField(
            label=label, #on_focus=on_textfield_focus,
            border=ft.InputBorder.NONE, bgcolor=ft.Colors.WHITE,
            border_radius=14, expand=expand, content_padding=15,
            multiline=multiline, min_lines=min_lines
        )

    nombre = crear_campo_texto("Nombre completo", expand=True)
    telefono = crear_campo_texto("Teléfono")
    direccion = crear_campo_texto("Dirección (calle)", expand=True)
    num_ext = crear_campo_texto("Número exterior")
    cp = crear_campo_texto("Código postal", expand=True)
    colonia = crear_campo_texto("Colonia", expand=True)
    entre_calles = crear_campo_texto("Entre calles", expand=True)
    ciudad = crear_campo_texto("Ciudad", expand=True)
    municipio = crear_campo_texto("Municipio", expand=True)
    estado = crear_campo_texto("Estado")
    referencias = crear_campo_texto("Referencias del domicilio", multiline=True, min_lines=3)

    logo = ft.Image(ref=logo_ref, src=logo_pepe, width=250)
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
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),
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
                    # El teclado se coloca justo debajo
                    teclado_virtual.build()
                ]
            )
        ]
    )


def vista_confirmacion(page: ft.Page, use_cases: FinalizarPedidoUseCases, pedido_use_cases: PedidoUseCases):
    from src.infrastructure.printing_service import PrintingService

    ticket_finalizado = use_cases.finalizar_y_obtener_ticket()
    pedido = pedido_use_cases.obtener_pedido_actual()

    if not ticket_finalizado:
        page.snack_bar = ft.SnackBar(ft.Text("No se pudo finalizar el pedido."))
        page.snack_bar.open = True
        page.go("/")
        page.update()
        return
    try:
        ps = PrintingService()
        pdf_path = ps.generar_ticket_pdf(ticket_finalizado)
        ps.enviar_a_impresora(pdf_path)
    except Exception as e:
        logger.error(f"ERROR impresión: {e}")

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
        pedido_use_cases.iniciar_nuevo_pedido()
        page.go("/")

    def abrir_detalle_pedido(e):
        t = ticket_finalizado
        p = pedido
        if getattr(t, 'nombre_categoria', None):
            nombre_categoria = t.nombre_categoria
        else:
            categorias = {c.id: c.nombre for c in pedido_use_cases.obtener_categorias()}
            nombre_categoria = categorias.get(getattr(t, 'id_categoria', None), "N/A")

        def crear_fila_resumen(icono, titulo, valor):
            return ft.Row(
                spacing=15,
                controls=[
                    ft.Image(src=f"c:/KioscoPP/img/iconos/{icono}", width=40, height=40),
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(titulo, size=12, color=ft.Colors.GREY_600),
                            ft.Text(valor or "No seleccionado", size=16, weight=ft.FontWeight.BOLD),
                        ]
                    )
                ]
            )

        # Formateador de moneda
        def mxn(v):
            try:
                return f"${v:,.2f}"
            except Exception:
                return f"${v}"

        # Detalle del extra (por si es Flor Artificial multiplicada)
        extra_detalle = ""
        unit = (getattr(t, 'extra_precio', None) if getattr(t, 'extra_precio', None) is not None else (getattr(t, 'extra_costo', 0.0) or 0.0))
        qty = getattr(t, 'extra_flor_cantidad', 0) or 0
        if getattr(t, 'extra_seleccionado', None):
            if t.extra_seleccionado == "Flor Artificial" and qty > 0:
                extra_monto = unit * qty
                extra_detalle = f"{t.extra_seleccionado} ({qty} x {mxn(unit)})"
            else:
                extra_monto = unit
                extra_detalle = t.extra_seleccionado
        else:
            extra_monto = 0.0
        costo_pastel = (getattr(t, 'precio_pastel', 0.0) or 0.0)
        subtotal = (costo_pastel or 0.0) + (extra_monto or 0.0)
        costo_envio = 50.0 if subtotal < 500 else 0.0
        total_mostrar = subtotal + costo_envio

        # 'incluye' puede no existir en Ticket; usar vacío como fallback
        incluye_texto = p.incluye #getattr(t, 'incluye', '') or ''

        bs_detalle = ft.BottomSheet(
            content=ft.Container(
                height=int(page.height * 0.90),
                padding=20,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda _: setattr(bs_detalle, 'open',
                                                                                                    False) or page.update())]
                        ),
                        ft.Text(f"Detalle del Pedido #{t.id_pedido}", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Row(
                            controls=[
                                ft.Column([
                                    crear_fila_resumen("categoria.png", "Categoría", nombre_categoria),
                                    crear_fila_resumen("forma.png", "Forma", t.tipo_forma),
                                    crear_fila_resumen("relleno.png", "Relleno", t.tipo_relleno),
                                ], expand=1),
                                ft.Column([
                                    crear_fila_resumen("tamano2.png", "Tamaño (Personas)", t.tamano_pastel),
                                    crear_fila_resumen("pan.png", "Pan", t.tipo_pan),
                                    crear_fila_resumen("cobertura.png", "Cobertura", t.tipo_cobertura),
                                ], expand=1),
                            ]
                        ),
                        ft.Divider(height=10),
                        ft.Text(
                            f"Fecha de entrega: {getattr(t, 'fecha_entrega', 'N/A') or 'N/A'} a las {getattr(t, 'hora_entrega', 'N/A') or 'N/A'}"),
                        ft.Text(f"Cliente: {getattr(t, 'nombre_cliente', '')} ({getattr(t, 'telefono_cliente', '')})"),
                        ft.Text(
                            f"Dirección: {getattr(t, 'direccion_cliente', '')} #{getattr(t, 'num_ext_cliente', '')}, {getattr(t, 'colonia_cliente', '')}, {getattr(t, 'ciudad_cliente', '')}, {getattr(t, 'estado_cliente', '')}, CP: {getattr(t, 'cp_cliente', '')}"),
                        ft.Divider(height=15),
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
                                        controls=[ft.Text("Precio del pastel"), ft.Text(mxn(costo_pastel))]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Extra" + (f" – {extra_detalle}" if extra_detalle else "")),
                                            ft.Text(mxn(extra_monto))
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Costo de envío"),
                                            ft.Text(mxn(costo_envio))
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
                        ft.Container(height=10),
                        ft.Text("Incluye", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                            border_radius=10,
                            content=ft.Text(incluye_texto)
                        ),

                    ]
                ),
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

    logo = ft.Image(src=logo_pepe, width=424, height=254, opacity=0, animate_opacity=300)

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
                        content=ft.Text("Nuevo pedido", color=ft.Colors.WHITE, size=30),
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
            ft.Image(src=fondo_hd, fit=ft.ImageFit.COVER, expand=True),

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
