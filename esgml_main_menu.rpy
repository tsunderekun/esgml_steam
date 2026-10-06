init -990 python:
    if persistent.esgml_main_menu_overlay is None:
        persistent.esgml_main_menu_overlay = True

init 1000 python:
    esgml_overlay_hint = ""

    # Стиль кнопок оверлея в главном меню игры
    style.esgml_ov_btn = Style(style.default)
    style.esgml_ov_btn.font = "res/esgml_new.ttf"
    style.esgml_ov_btn.size = 38
    style.esgml_ov_btn.color = (255, 255, 255, 230)
    style.esgml_ov_btn.hover_color = (255, 226, 125, 255) # Тёплый золотистый цвет ховера в стилистике БЛ
    style.esgml_ov_btn.outlines = [(1, "#000000bb", 0, 0)]

    def esgml_toggle_main_menu_overlay():
        global git_not
        curr = getattr(persistent, "esgml_main_menu_overlay", True)
        persistent.esgml_main_menu_overlay = not curr
        if persistent.esgml_main_menu_overlay:
            git_not = "Быстрые кнопки в меню: ВКЛ"
        else:
            git_not = "Быстрые кнопки в меню: ВЫКЛ"
        renpy.restart_interaction()

    def esgml_overlay_callback():
        try:
            enabled = getattr(persistent, "esgml_main_menu_overlay", True)
            is_main = bool(getattr(store, "main_menu", False) and renpy.get_screen("main_menu"))
            is_shown = bool(renpy.get_screen("esgml_main_menu_overlay"))
            if is_main and enabled:
                if not is_shown:
                    renpy.show_screen("esgml_main_menu_overlay")
            else:
                if is_shown:
                    renpy.hide_screen("esgml_main_menu_overlay")
                    if renpy.get_screen("esgml_overlay_tooltip"):
                        renpy.hide_screen("esgml_overlay_tooltip")
        except Exception:
            pass

    if esgml_overlay_callback not in config.interact_callbacks:
        config.interact_callbacks.append(esgml_overlay_callback)

screen esgml_main_menu_overlay():
    zorder 100
    modal False

    frame:
        background Frame(Solid("#00000088"))
        xpos 35
        ypos 28
        left_padding 20
        right_padding 20
        top_padding 8
        bottom_padding 8

        hbox spacing 22 yalign 0.5:
            textbutton "Моды":
                style "esgml_ov_btn"
                text_style "esgml_ov_btn"
                hovered [SetVariable("esgml_overlay_hint", "Список установленных модов"), Show("esgml_overlay_tooltip", dissolve)]
                unhovered [SetVariable("esgml_overlay_hint", ""), Hide("esgml_overlay_tooltip", dissolve)]
                action [Hide("esgml_overlay_tooltip"), ShowMenu('mods')]
                at git_img_b

            text "•" yalign 0.5:
                color "#ffffff55"
                size 30

            textbutton "ESGML":
                style "esgml_ov_btn"
                text_style "esgml_ov_btn"
                hovered [SetVariable("esgml_overlay_hint", "Загрузчик модов ESGML"), Show("esgml_overlay_tooltip", dissolve)]
                unhovered [SetVariable("esgml_overlay_hint", ""), Hide("esgml_overlay_tooltip", dissolve)]
                action [Hide("esgml_overlay_tooltip"), SetField(persistent, "jump_to", "knz_dwnl_git"), Start()]
                at git_img_b

screen esgml_overlay_tooltip():
    zorder 101
    frame background Frame(Solid("#000000aa")) xpos 35 ypos 95 left_padding 14 right_padding 14 top_padding 5 bottom_padding 5:
        text esgml_overlay_hint:
            style "esgml_nm"
            size 24
            color "#e6e6e6"
