init -999 python:
    import os as git_os
    _workshop_dir = git_os.path.normpath(git_os.path.join(renpy.config.basedir, '..', '..', 'workshop', 'content', '331470', '1515489831')) + '/'
    _workshop_parent = git_os.path.normpath(git_os.path.join(renpy.config.basedir, '..', '..', 'workshop', 'content', '331470'))
    if git_os.path.exists(_workshop_parent):
        if not git_os.path.exists(_workshop_dir):
            try:
                git_os.makedirs(_workshop_dir)
            except Exception:
                pass
        git_destination = _workshop_dir
    else:
        _fallback_dir = git_os.path.normpath(git_os.path.join(renpy.config.gamedir, 'mods', 'esgml')) + '/'
        if not git_os.path.exists(_fallback_dir):
            try:
                git_os.makedirs(_fallback_dir)
            except Exception:
                pass
        git_destination = _workshop_dir if git_os.path.exists(_workshop_dir) else _fallback_dir

    if git_destination:
        _d_clean = git_os.path.normpath(git_destination)
        if _d_clean not in renpy.config.searchpath:
            renpy.config.searchpath.append(_d_clean)
        try:
            renpy.loader.cleardirfiles()
        except Exception:
            pass
        try:
            renpy.loader.loadable_cache.clear()
        except Exception:
            pass

init:
    python:
        try:
            mods["knz_dwnl_git"] = u"{font=res/esgml_new.ttf}Everlasting Summer GitHub Mods Loader{/font}"
        except Exception:
            pass
    $ esgml_ver = '4.1'
    $ ch_pr = ''
    $ ready_ma = False
    $ ready_m = False
    if persistent.git_mod_installed == None:
        $ persistent.git_mod_installed = []
    transform git_img_b():
        subpixel True
        parallel:
            on idle:
                ease 0.22 zoom 1.0
            on hover:
                ease 0.22 zoom 1.25
        parallel:
            on idle:
                ease 0.22 alpha 1.0
            on hover:
                ease 0.22 alpha 0.7

    transform git_img_c():
        subpixel True
        on idle:
            ease 0.25 alpha 1.0
        on hover:
            ease 0.25 alpha 0.65

    transform git_img_u():
        subpixel True
        easein 2 alpha 0
        easein 2 alpha 1.0

    transform git_img_btn_sm():
        subpixel True
        parallel:
            on idle:
                ease 0.18 zoom 0.72
            on hover:
                ease 0.18 zoom 0.88
        parallel:
            on idle:
                ease 0.18 alpha 1.0
            on hover:
                ease 0.18 alpha 0.7

    image git_nfo = "res/git_nfo.png"
    $ nfo_text = ''
    $ m_nfo_text = ''
    $ git_queue = []
    $ git_del_queue = []
    $ git_qu_tab = 'dwl'



    $ style.esgml_mm = Style(style.default)
    $ style.esgml_mm.color = (255, 255, 255, 100)
    $ style.esgml_mm.hover_color = (255, 255, 255, 55)
    $ style.esgml_mm.size = 55
    $ style.esgml_mm.font = "res/esgml_new.ttf"
    $ style.esgml_mm.text_align = 0.5

    $ style.esgml_bb = Style(style.esgml_mm)
    $ style.esgml_bb.text_align = 2
    $ style.esgml_bb.size = 72

    $ style.esgml_ii = Style(style.esgml_mm)
    $ style.esgml_ii.font = "res/esgml_descr.ttf"
    $ style.esgml_ii.text_align = 0.5
    $ style.esgml_ii.size = 32
    $ style.esgml_ii.color = (255, 255, 255, 100)

    $ style.esgml_nn = Style(style.esgml_mm)
    $ style.esgml_nn.color = (255, 255, 255, 100)
    $ style.esgml_nn.size = 80

    $ style.esgml_nm = Style(style.esgml_nn)
    $ style.esgml_nm.size = 40

    $ style.esgml_not = Style(style.esgml_nn)
    $ style.esgml_not.size = 48
    $ style.esgml_not.outlines = [(1, "#000", 0, 0)] #dialogue text

    $ style.esgml_notb = Style(style.esgml_not)
    $ style.esgml_notb.size = 60

    $ style.esgml_mn = Style(style.esgml_nm)
    $ style.esgml_mn.size = 40
    $ style.esgml_mn.color = (255, 255, 255, 100)

    $ style.esgml_mmn = Style(style.esgml_mn)
    $ style.esgml_mmn.size = 80

    $ style.esgml_vbar = Style(style.vbar)
    $ style.esgml_vbar.bar_vertical = True
    $ style.esgml_vbar.top_bar = Solid("#00000055")
    $ style.esgml_vbar.bottom_bar = Solid("#00000055")
    $ style.esgml_vbar.thumb = Solid("#ffe27d88")
    $ style.esgml_vbar.hover_thumb = Solid("#ffe27dff")
    $ style.esgml_vbar.thumb_shadow = None
    $ style.esgml_vbar.thumb_offset = 0
    $ style.esgml_vbar.xmaximum = 12
    $ style.esgml_vbar.xminimum = 12

    $ style.esgml_bar_btn = Style(style.default)
    $ style.esgml_bar_btn.font = "res/esgml_new.ttf"
    $ style.esgml_bar_btn.size = 26
    $ style.esgml_bar_btn.color = (200, 200, 200, 220)
    $ style.esgml_bar_btn.hover_color = (255, 226, 125, 255)
    $ style.esgml_bar_btn.selected_color = (255, 226, 125, 255)
    $ style.esgml_bar_btn.selected_hover_color = (255, 245, 180, 255)
    $ style.esgml_bar_btn.outlines = [(1, "#000000bb", 0, 0)]

    $ style.esgml_mod_btn = Style(style.esgml_mm)
    $ style.esgml_mod_btn.size = 35

    $ tindex = ''
    $ git_not = ''
    $ git_not1 = ''
    $ global tindex

init python:
    import re as _esgml_re

    if getattr(persistent, "esgml_sort_mode", None) is None:
        persistent.esgml_sort_mode = "name_asc"
    if getattr(persistent, "esgml_filter_mode", None) is None:
        persistent.esgml_filter_mode = "all"
    esgml_search_query = ""

    def _esgml_clean_str(s):
        if not s:
            return u""
        if isinstance(s, str):
            try:
                s = s.decode("utf-8", "ignore")
            except Exception:
                s = unicode(s)
        elif not isinstance(s, unicode):
            s = unicode(s)
        return _esgml_re.sub(r'\{[^\}]+\}', '', s).strip().lower()

    def esgml_get_counts():
        global git_mod_lists, persistent
        installed_set = set(str(x) for x in (getattr(persistent, "git_mod_installed", []) or []))
        total = len(git_mod_lists)
        installed = sum(1 for m in git_mod_lists if str(m) in installed_set)
        available = total - installed
        return total, installed, available

    def git_get_filtered_sorted_mods():
        global git_mod_lists, git_info, persistent, esgml_search_query
        installed_set = set(str(x) for x in (getattr(persistent, "git_mod_installed", []) or []))
        flt = getattr(persistent, "esgml_filter_mode", "all")
        sort_m = getattr(persistent, "esgml_sort_mode", "name_asc")
        q = _esgml_clean_str(esgml_search_query)

        result = []
        for mid in git_mod_lists:
            mid_str = str(mid)
            is_inst = mid_str in installed_set

            if flt == "installed" and not is_inst:
                continue
            elif flt == "available" and is_inst:
                continue

            if q:
                minfo = git_info.get(mid, {})
                m_name = _esgml_clean_str(minfo.get("name", ""))
                m_desc = _esgml_clean_str(minfo.get("desc", ""))
                m_id = _esgml_clean_str(mid_str)
                if q not in m_name and q not in m_desc and q not in m_id:
                    continue

            result.append(mid)

        if sort_m == "name_asc":
            result.sort(key=lambda m: _esgml_clean_str(git_info.get(m, {}).get("name", m)))
        elif sort_m == "name_desc":
            result.sort(key=lambda m: _esgml_clean_str(git_info.get(m, {}).get("name", m)), reverse=True)
        elif sort_m == "installed_first":
            result.sort(key=lambda m: (0 if str(m) in installed_set else 1, _esgml_clean_str(git_info.get(m, {}).get("name", m))))
        elif sort_m == "default":
            pass

        return result

label esgml_search_input:
    python:
        _cur_s = esgml_search_query if esgml_search_query else ""
        _in_val = renpy.input(u"Поиск по названию или описанию мода (Enter для подтверждения):", default=_cur_s, length=40)
        esgml_search_query = _in_val.strip() if _in_val else ""
    return

label knz_dwnl_git:
    window hide
    python:
        try:
            git_load_custom_repos()
        except Exception:
            pass
    $ config.mouse = {'default' : [("res/cursor.png", 0, 0)]}
    play sound 'res/git_start.ogg'
    show image "res/git_splash.png" with dspr
    $ renpy.pause(1.5)
    play music 'res/git_main.ogg' fadein 3
    if _return == "mm":
        $ config.mouse = {'default' : [("images/misc/mouse/1.png", 0, 0)]}
        return
    call screen knz_git_dwnl_menu with dissolve

screen knz_info_screen(nfo_text, m_nfo_text):
    modal False
    add 'git_nfo'
    vbox xalign 0.5 yalign 0.5:
        text nfo_text substitute False xalign 0.5 at git_img_u:
            style "esgml_nn"
        null height 20
        text m_nfo_text substitute False xalign 0.5 at git_img_u:
            style "esgml_nm"
        null height 10
        text ch_pr substitute False xalign 0.5 at git_img_u:
            style "esgml_nm"




screen knz_git_dwnl_menu:
    $ import os as git_os
    $ import urlparse
    modal False

    $ _cnt_tot, _cnt_inst, _cnt_avail = esgml_get_counts()
    $ _displayed_mods = git_get_filtered_sorted_mods()

    window:
        xalign 0 yalign 0
        background "git_nfo"
        vbox xpos 0.05 ypos 0.02:

            text "Everlasting Summer Git Mods Loader":
                style "esgml_mmn"
                size 48

            hbox spacing 14 yalign 0.5:
                text ("Каталог модов (" + str(len(_displayed_mods)) + " из " + str(_cnt_tot) + "):"):
                    style "esgml_mn"
                    size 26
                    yalign 0.5

                if esgml_search_query:
                    hbox spacing 8 yalign 0.5:
                        text ("{color=#ffe27d}Поиск: «" + esgml_search_query + "»{/color}") size 24 yalign 0.5
                        textbutton "(Сбросить)":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetVariable("esgml_search_query", "")
                            yalign 0.5

            null height 6

            frame:
                background Frame(Solid("#00000077"))
                left_padding 14
                right_padding 14
                top_padding 6
                bottom_padding 6
                hbox spacing 18 yalign 0.5:
                    hbox spacing 8 yalign 0.5:
                        text "Фильтр:" size 24 color "#aaaaaa" yalign 0.5
                        textbutton ("Все (" + str(_cnt_tot) + ")"):
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_filter_mode", "all")
                            selected (persistent.esgml_filter_mode == "all")
                        textbutton ("Установленные (" + str(_cnt_inst) + ")"):
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_filter_mode", "installed")
                            selected (persistent.esgml_filter_mode == "installed")
                        textbutton ("Доступные (" + str(_cnt_avail) + ")"):
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_filter_mode", "available")
                            selected (persistent.esgml_filter_mode == "available")

                    text "|" size 24 color "#555555" yalign 0.5

                    hbox spacing 8 yalign 0.5:
                        text "Сортировка:" size 24 color "#aaaaaa" yalign 0.5
                        textbutton "А-Я":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_sort_mode", "name_asc")
                            selected (persistent.esgml_sort_mode == "name_asc")
                        textbutton "Я-А":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_sort_mode", "name_desc")
                            selected (persistent.esgml_sort_mode == "name_desc")
                        textbutton "Установленные":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_sort_mode", "installed_first")
                            selected (persistent.esgml_sort_mode == "installed_first")
                        textbutton "По умолчанию":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action SetField(persistent, "esgml_sort_mode", "default")
                            selected (persistent.esgml_sort_mode == "default")

                    text "|" size 24 color "#555555" yalign 0.5

                    hbox spacing 8 yalign 0.5:
                        textbutton "Поиск":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action Function(renpy.call_in_new_context, 'esgml_search_input')
                        textbutton "Сброс":
                            style "esgml_bar_btn"
                            text_style "esgml_bar_btn"
                            action [SetVariable("esgml_search_query", ""), SetField(persistent, "esgml_filter_mode", "all"), SetField(persistent, "esgml_sort_mode", "name_asc")]

    side "c r":
        area (0.05, 0.170, 0.85, 0.745)
        viewport id "git_mods_menu":
            draggable True
            mousewheel True
            has vbox
            if not _displayed_mods:
                null height 50
                text "Модификации по выбранным критериям не найдены" size 28 color "#888888" xalign 0.5
            for id in _displayed_mods:
                hbox spacing 10 yalign 0.5:

                    if str(id) in persistent.git_mod_installed:
                        add 'res/git_dwl_inactive.png' yalign 0.5 at git_img_btn_sm
                    else:
                        imagebutton auto 'res/git_dwl_%s.png' action [Function(generate_index, id), Function(renpy.call_in_new_context, 'run_down2')] at git_img_btn_sm yalign 0.5

                    if str(id) in persistent.git_mod_installed:
                        if str(id) in git_del_queue:
                            add 'res/git_qu_inactive.png' yalign 0.5 at git_img_btn_sm
                        else:
                            imagebutton auto 'res/git_qu_%s.png' action [Function(git_del_queue.append, id), SetVariable("git_not", git_info[id]["name"] + '\nдобавлен в очередь удаления'), Show("git_notice", dissolve)] at git_img_btn_sm yalign 0.5
                    elif str(id) in git_queue:
                        add 'res/git_qu_inactive.png' yalign 0.5 at git_img_btn_sm
                    else:
                        imagebutton auto 'res/git_qu_%s.png' action [Function(git_queue.append, id), SetVariable("git_not", git_info[id]["name"] + '\nдобавлен в очередь загрузки'), Show("git_notice", dissolve)] at git_img_btn_sm yalign 0.5

                    if str(id) in persistent.git_mod_installed:
                        imagebutton auto 'res/git_del_%s.png' action [Function(generate_index, id), Function(renpy.call_in_new_context, 'deleter')] at git_img_btn_sm yalign 0.5
                    else:
                        add 'res/git_del_inactive.png' yalign 0.5 at git_img_btn_sm

                    textbutton git_info[id]["name"] yalign 0.5 action [Hide("knz_git_dwnl_menu", dissolve), Show('git_modnfo', dissolve, id)] at git_img_b:
                        style "esgml_mod_btn"
                        text_style "esgml_mod_btn"

        vbar value YScrollValue("git_mods_menu") style "esgml_vbar"

    frame background Frame(Solid("0008")) left_padding 20 right_padding 20 bottom_padding 12 top_padding 10 xalign 0.5 yalign 1.0 xminimum 1920 xmaximum 1920:
        grid 6 1 spacing 96 xalign 0.5 yalign 0.5:

            imagebutton auto 'res/git_main_%s.png' action [SetField(config, "mouse", {'default' : [('images/misc/mouse/1.png', 0, 0)]}), MainMenu(confirm=False)] hovered [SetVariable("git_not1", "Вернуться в главное меню"), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b

            $ _qu_text = "Очередь: загрузка (" + str(len(git_queue)) + "), удаление (" + str(len(git_del_queue)) + ")" if (git_queue or git_del_queue) else "Очередь"
            imagebutton auto 'res/git_qu1_%s.png' action [Function(renpy.call_in_new_context, 'go_to_git_qu')] hovered [SetVariable("git_not1", _qu_text), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b

            imagebutton auto 'res/git_nlt_%s.png' action [Show("git_debug", dissolve)] hovered [SetVariable("git_not1", "Настройки и отладка"), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b

            imagebutton auto 'res/git_rst_%s.png' action [Function(renpy.utter_restart)] hovered [SetVariable("git_not1", "Перезагрузить"), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b

            imagebutton auto 'res/git_nfo_%s.png' action [Function(renpy.call_in_new_context, 'go_to_git_authors')] hovered [SetVariable("git_not1", "Информация о моде"), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b

            imagebutton auto 'res/git_exit_%s.png' action [Quit(confirm=False)] hovered [SetVariable("git_not1", "Выйти из БЛ"), Show("git_notice_d")] unhovered [SetVariable("git_not1", ""), Hide("git_notice_d")] at git_img_b


    # default git_not1 = ''

    # vbox xalign 0.5 yalign 0.875:
    #     textbutton git_not1:
    #         style "esgml_not"
    #         text_style "esgml_not"

screen git_notice():
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.5 left_padding 25 right_padding 25 bottom_padding 25 top_padding 25:
        textbutton git_not:
            style "esgml_not"
            text_style "esgml_not"
    timer 2.0 action Hide("git_notice", dissolve)

screen git_notice_d():
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.875 left_padding 10 right_padding 10 bottom_padding 10 top_padding 10:
        textbutton git_not1:
            style "esgml_not"
            text_style "esgml_not"

screen git_restart_prompt(prompt_title="Требуется перезагрузка", prompt_msg="Для применения изменений требуется перезагрузка игры.\nПерезагрузить сейчас?"):
    modal True
    add Solid("#000000a0")
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.5 left_padding 40 right_padding 40 bottom_padding 35 top_padding 35:
        vbox xalign 0.5:
            textbutton prompt_title xalign 0.5:
                style "esgml_notb"
                text_style "esgml_notb"
            null height 20
            text prompt_msg substitute False xalign 0.5 text_align 0.5:
                style "esgml_nm"
            null height 35
            hbox xalign 0.5 spacing 80:
                textbutton "Перезагрузить" action [Hide("git_restart_prompt", dissolve), Function(renpy.utter_restart)] at git_img_b:
                    style "esgml_not"
                    text_style "esgml_not"
                textbutton "Позже" action [Hide("git_restart_prompt", dissolve), Return()] at git_img_b:
                    style "esgml_not"
                    text_style "esgml_not"

screen git_debug():
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.5 left_padding 25 right_padding 25 bottom_padding 25 top_padding 25:
        vbox:
            textbutton "Настройки и отладка" xalign 0.5:
                style "esgml_notb"
                text_style "esgml_notb"
            null height 20

            $ _ov_state = " (ВКЛ)" if getattr(persistent, "esgml_main_menu_overlay", True) else " (ВЫКЛ)"
            $ _ov_txt = "Быстрые кнопки в главном меню:" + _ov_state
            textbutton _ov_txt xalign 0.5 action [Function(esgml_toggle_main_menu_overlay), Show("git_notice", dissolve)] at git_img_b:
                style "esgml_not"
                text_style "esgml_not"

            null height 15
            textbutton "Очистить индексы установленных модов" xalign 0.5 action [Hide("git_debug", dissolve), Function(git_clear_index)] at git_img_b:
                style "esgml_not"
                text_style "esgml_not"
            textbutton "Ручное управление индексами" xalign 0.5 action [Hide("git_debug", dissolve), Function(renpy.call_in_new_context, 'go_to_git_manual_index')] at git_img_b:
                style "esgml_not"
                text_style "esgml_not"
            if 'NLT_tl' in globals():
                textbutton "Запустить New Life Team ModPack" xalign 0.5 action [Function(renpy.call_in_new_context, 'NLT_toolbox')] at git_img_b:
                    style "esgml_not"
                    text_style "esgml_not"
            else:
                textbutton "Загрузить New Life Team ModPack" xalign 0.5 action [OpenURL('steam://url/CommunityFilePage/847728687')] at git_img_b:
                    style "esgml_not"
                    text_style "esgml_not"
            null height 20
            textbutton "Назад" xalign 0.5 action Hide("git_debug", dissolve) at git_img_b:
                style "esgml_not"
                text_style "esgml_not"

screen git_debug_id(id):
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.5 left_padding 25 right_padding 25 bottom_padding 25 top_padding 25:
        vbox xalign 0.5:
            textbutton "Операции с индексом" xalign 0.5:
                style "esgml_notb"
                text_style "esgml_notb"
            null height 25
            hbox xalign 0.5 spacing 48:
                if str(id) in persistent.git_mod_installed:
                    textbutton "Удалить" action [Function(git_manual_index, id, 0), Hide("git_debug_id", dissolve)] at git_img_b:
                        style "esgml_not"
                        text_style "esgml_not"
                    textbutton "(есть в списке)" at git_img_b:
                        style "esgml_not"
                        text_style "esgml_not"
                else:
                    textbutton "Добавить" action [Function(git_manual_index, id, 1), Hide("git_debug_id", dissolve)] at git_img_b:
                        style "esgml_not"
                        text_style "esgml_not"
                    textbutton "(нет в списке)" at git_img_b:
                        style "esgml_not"
                        text_style "esgml_not"
            null height 25
            textbutton "Назад" xalign 0.5 action Hide("git_debug_id", dissolve) at git_img_b:
                style "esgml_not"
                text_style "esgml_not"



label go_to_git_authors:
    hide screen knz_git_dwnl_menu
    if _return == "mm":
        return
    call screen git_authors with fade

label go_to_git_qu:
    hide screen knz_git_dwnl_menu
    if _return == "mm":
        return
    call screen git_qus with fade

label go_to_git_manual_index:
    hide screen knz_git_dwnl_menu
    if _return == "mm":
        return
    call screen git_manual_index with fade

screen git_qus:
    modal False
    add "git_nfo"

    $ _qu_dwl_title = "Очередь загрузки (" + str(len(git_queue)) + ")"
    $ _qu_del_title = "Очередь удаления (" + str(len(git_del_queue)) + ")"

    vbox xpos 0.05 ypos 0.08:
        hbox spacing 40:
            if git_qu_tab == 'dwl':
                textbutton _qu_dwl_title:
                    style "esgml_nn"
                    text_style "esgml_nn"
            else:
                textbutton _qu_dwl_title action SetVariable("git_qu_tab", "dwl") at git_img_b:
                    style "esgml_mn"
                    text_style "esgml_mn"

            if git_qu_tab == 'del':
                textbutton _qu_del_title:
                    style "esgml_nn"
                    text_style "esgml_nn"
            else:
                textbutton _qu_del_title action SetVariable("git_qu_tab", "del") at git_img_b:
                    style "esgml_mn"
                    text_style "esgml_mn"

    side "c r":
        area (0.05, 0.20, 0.88, 0.65)
        viewport id "git_qu_menu":
            draggable True
            mousewheel True
            has vbox
            if git_qu_tab == 'dwl':
                if not git_queue:
                    textbutton "Очередь загрузки пуста" at git_img_b:
                        style "esgml_mm"
                        text_style "esgml_mm"
                else:
                    for id in git_queue:
                        hbox spacing 24 yalign 0.5:
                            imagebutton auto 'res/git_del_%s.png' action [Function(git_queue.remove, id), SetVariable("git_not", git_info[id]["name"] + '\nубран из очереди'), Show("git_notice", dissolve)] at git_img_b yalign 0.5
                            textbutton git_info[id]["name"] action [Hide("git_qus", dissolve), Show('git_modnfo', dissolve, id)] at git_img_b yalign 0.5:
                                style "esgml_mm"
                                text_style "esgml_mm"
            else:
                if not git_del_queue:
                    textbutton "Очередь удаления пуста" at git_img_b:
                        style "esgml_mm"
                        text_style "esgml_mm"
                else:
                    for id in git_del_queue:
                        hbox spacing 24 yalign 0.5:
                            imagebutton auto 'res/git_del_%s.png' action [Function(git_del_queue.remove, id), SetVariable("git_not", git_info[id]["name"] + '\nубран из очереди'), Show("git_notice", dissolve)] at git_img_b yalign 0.5
                            textbutton git_info[id]["name"] action [Hide("git_qus", dissolve), Show('git_modnfo', dissolve, id)] at git_img_b yalign 0.5:
                                style "esgml_mm"
                                text_style "esgml_mm"

        vbar value YScrollValue("git_qu_menu") style "esgml_vbar"

    hbox yalign 0.95 xalign 0.5 spacing 96:
        if git_qu_tab == 'dwl':
            if git_queue:
                textbutton 'Загрузить' action [Function(git_qu_dwl)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"
                textbutton 'Очистить' action [Function(git_qu_clr)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"
        else:
            if git_del_queue:
                textbutton 'Удалить' action [Function(git_qu_del)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"
                textbutton 'Очистить' action [Function(git_del_qu_clr)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"
        textbutton 'Назад' action [Show('knz_git_dwnl_menu', dissolve), Hide('git_qus')] at git_img_b:
            style "esgml_bb"
            text_style "esgml_bb"

screen git_manual_index:
    modal False
    add "git_nfo"
    vbox xpos 0.05 ypos 0.05 yfill:
                    text "Ручное управление индексами":
                                style "esgml_nn"
                    side "r":
                        area (0.05, 0.05, 0.7, 0.675)
                        viewport id "git_ind_menu":
                            draggable True
                            mousewheel True
                            scrollbars None
                            has vbox
                            for id in git_mod_lists:
                                textbutton str(id) + " " + git_info[id]["name"] ypos -0.2125 action Show("git_debug_id", dissolve, id) at git_img_b:
                                    style "esgml_mm"
                                    text_style "esgml_mm"

    hbox yalign 0.975 xalign 0.5 spacing 96:
        textbutton 'Назад' action [Show('knz_git_dwnl_menu', dissolve), Hide('git_manual_index')] at git_img_b:
                style "esgml_bb"
                text_style "esgml_bb"


screen git_authors:
    modal False
    add "git_nfo"
    vbox xpos 0.05 ypos 0.05 yfill:

        text "Everlasting Summer Git Mods Loader":
                    style "esgml_nn"

        null height 5

        hbox xpos 0.025:

            text "Версия:":
                        style "esgml_nm"

            null width 5

            text esgml_ver:
                        style "esgml_nm"


        null height 20

        text "Загрузчик удалённых из\xa0мастерской Steam модов «Бесконечного лета».\nЕсли вы знаете мод, который мог\xa0бы пополнить нашу коллекцию, пожалуйста, напишите нам в\xa0официальную группу\xa0ВК." text_align 0.0 xpos 0.025:
                    style "esgml_nm"

        null height 20

        text "Ссылки:" xpos 0.025:
                    style "esgml_nm"


        textbutton "Официальная группа" xpos 0.05 action OpenURL('https://vk.com/esgml') at git_img_b:
                    style "esgml_nm"
                    text_style "esgml_nm"


        textbutton "GitHub проекта" xpos 0.05 action OpenURL('https://github.com/tsunderekun/esgml_steam') at git_img_b:
                    style "esgml_nm"
                    text_style "esgml_nm"

        null height 10

        text "Авторы:" xpos 0.025:
            style "esgml_nm"

        textbutton "Илья Кунц {i}aka Phos{/i}" xpos 0.05 action OpenURL('https://vk.com/id327507103') at git_img_b:
            style "esgml_nm"
            text_style "esgml_nm"

        textbutton "Константин Можейко {i}aka Лена{/i}" xpos 0.05 action OpenURL('https://vk.com/id18106410') at git_img_b:
            style "esgml_nm"
            text_style "esgml_nm"

        textbutton "Андрей Солодников {i}aka confect1on{/i}" xpos 0.05 action OpenURL('https://vk.com/id250093621') at git_img_b:
            style "esgml_nm"
            text_style "esgml_nm"

        null height 20

        textbutton "Проект распространяется по лицензии CC BY-NC-SA 4.0" xpos 0.025 action OpenURL('https://creativecommons.org/licenses/by-nc-sa/4.0/') at git_img_b:
            style "esgml_nm"
            text_style "esgml_nm"

        null height 50

        textbutton 'Назад' ypos 0.8 action [Show('knz_git_dwnl_menu', dissolve), Hide('git_authors')] at git_img_b:
                style "esgml_bb"
                text_style "esgml_bb"



init 999 python:
    config.archives.append('res_git')

screen git_modnfo(id):
    modal False
    add "git_nfo"
    text git_info[id]["name"] yalign 0.05 xalign 0.1:
        style "esgml_nn"
    hbox spacing 64 yalign 0.9 xalign 0.5:
            textbutton 'Назад' action [Show('knz_git_dwnl_menu', dissolve), Hide('git_modnfo')] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"


            if str(id) in persistent.git_mod_installed:
                textbutton 'Удалить' action [Function(generate_index, id), Function(renpy.call_in_new_context, 'deleter')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                if str(id) in git_del_queue:
                    textbutton 'В очереди удаления' action [Function(git_del_queue.remove, id), SetVariable("git_not", git_info[id]["name"] + '\nубран из очереди удаления'), Show("git_notice", dissolve)] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                else:
                    textbutton '+ В очередь' action [Function(git_del_queue.append, id), SetVariable("git_not", git_info[id]["name"] + '\nдобавлен в очередь удаления'), Show("git_notice", dissolve)] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
            else:
                textbutton 'Загрузить' action [Function(generate_index, id), Function(renpy.call_in_new_context, 'run_down2')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                if str(id) in git_queue:
                    textbutton 'В очереди загрузки' action [Function(git_queue.remove, id), SetVariable("git_not", git_info[id]["name"] + '\nубран из очереди загрузки'), Show("git_notice", dissolve)] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                else:
                    textbutton '+ В очередь' action [Function(git_queue.append, id), SetVariable("git_not", git_info[id]["name"] + '\nдобавлен в очередь загрузки'), Show("git_notice", dissolve)] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
    side "c":
        area (0.1, 0.175, 0.9, 0.65)
        viewport id "modnfo":
            xalign 0.5 yalign 0.175
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                hbox yalign 0.175 xalign 0.5 spacing 64:
                    $ _s1 = git_resolve_screen(id, 1, git_info[id].get('scr1'))
                    $ _s2 = git_resolve_screen(id, 2, git_info[id].get('scr2'))
                    $ _s3 = git_resolve_screen(id, 3, git_info[id].get('scr3'))
                    imagebutton idle im.Scale(_s1, 480, 270) hover im.Scale(_s1, 480, 270) action [Show('git_image', dissolve, _s1, id)] at git_img_c
                    imagebutton idle im.Scale(_s2, 480, 270) hover im.Scale(_s2, 480, 270) action [Show('git_image', dissolve, _s2, id)] at git_img_c
                    imagebutton idle im.Scale(_s3, 480, 270) hover im.Scale(_s3, 480, 270) action [Show('git_image', dissolve, _s3, id)] at git_img_c
                text git_info[id]['desc'] substitute False yalign 0.55 xalign 0.5:
                    style "esgml_ii"
                    xmaximum 0.90

screen git_image(img, id):
    add "git_nfo"
    add img:
        xalign 0.5
        yalign 0.5

    button:
        style 'blank_button'
        xpos 0
        ypos 0
        xfill True
        yfill True
        action [Hide('git_image')]

init python:
    from threading import Thread
    import os as git_os
    import shutil

    def generate_index (id):
        global tindex
        tindex = str(id)

    kprogress = None

    def git_clear_index():
        global git_not
        persistent.git_mod_installed = []
        git_not = "Индексы успешно очищены"
        renpy.show_screen('git_notice')

    def git_manual_index(id, mode):
        global git_not
        if mode == 1:
            if id not in persistent.git_mod_installed:
                persistent.git_mod_installed.append(id)
            git_not = "Индекс успешно добавлен"
        if mode == 0:
            if id in persistent.git_mod_installed:
                persistent.git_mod_installed.remove(id)
            git_not = "Индекс успешно очищен"
        renpy.show_screen('git_notice')


    def knz_dnwl_mod(target_path_or_name, filelink):
        global ch_pr, git_tset, git_last_error
        ch_pr = "Инициализация..."
        git_tset = False
        git_last_error = ""

        try:
            import urllib.request as urllib2
        except ImportError:
            import urllib2

        import ssl
        import time
        try:
            ssl_context = ssl._create_unverified_context()
        except Exception:
            ssl_context = None

        # Определяем путь к целевому файлу
        if git_os.path.isabs(target_path_or_name) or ('/' in target_path_or_name) or ('\\' in target_path_or_name):
            target_filepath = target_path_or_name
        else:
            target_filepath = git_os.path.join(git_destination, target_path_or_name)

        target_dir = git_os.path.dirname(target_filepath)
        if target_dir and not git_os.path.exists(target_dir):
            try:
                git_os.makedirs(target_dir)
            except Exception:
                pass

        filename = git_os.path.basename(target_filepath)
        part_filepath = target_filepath + ".part"

        try:
            if isinstance(filelink, unicode):
                filelink = filelink.encode('ascii')
        except Exception:
            pass

        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                if attempt > 1:
                    ch_pr = "Повтор ({}/{})...\nИмя файла: {}".format(attempt, max_attempts, filename)
                    time.sleep(1.5)

                req = urllib2.Request(str(filelink), headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                })
                if ssl_context is not None:
                    try:
                        response = urllib2.urlopen(req, context=ssl_context, timeout=60)
                    except TypeError:
                        response = urllib2.urlopen(req, timeout=60)
                else:
                    response = urllib2.urlopen(req, timeout=60)

                # Безопасный парсинг Content-Length
                total_bytes = 0
                try:
                    if hasattr(response, 'headers') and response.headers.get("Content-Length"):
                        total_bytes = int(response.headers.get("Content-Length"))
                    elif response.info() and response.info().getheader("Content-Length"):
                        total_bytes = int(response.info().getheader("Content-Length"))
                except Exception:
                    total_bytes = 0

                total_mb_str = "{:.2f}".format(total_bytes / (1024.0 * 1024.0)) if total_bytes > 0 else "???"

                CHUNK = 64 * 1024
                downloaded = 0

                with open(part_filepath, 'wb') as f:
                    while True:
                        chunk = response.read(CHUNK)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        dl_mb = downloaded / (1024.0 * 1024.0)
                        if total_bytes > 0:
                            pct = (float(downloaded) / total_bytes) * 100.0
                            ch_pr = "Загружено {:.2f} из {} МБ ({:.1f}%)\nИмя файла: {}".format(dl_mb, total_mb_str, pct, filename)
                        else:
                            ch_pr = "Загружено {:.2f} МБ\nИмя файла: {}".format(dl_mb, filename)

                # Атомарная замена файла
                if git_os.path.exists(target_filepath):
                    try:
                        git_os.remove(target_filepath)
                    except Exception:
                        pass

                git_os.rename(part_filepath, target_filepath)
                git_tset = git_os.path.isfile(target_filepath)
                return git_tset

            except Exception as e:
                git_last_error = str(e).replace('[', '[[').replace(']', ']]')
                if git_os.path.exists(part_filepath):
                    try:
                        git_os.remove(part_filepath)
                    except Exception:
                        pass
                if attempt == max_attempts:
                    git_tset = False
                    return False
        return False

    ###MOD CHECKER###

init -10 python:
    git_archives = []

    def _git_resolve_dest():
        global git_destination
        if 'git_destination' in globals() and git_destination:
            return git_destination
        import os as git_os
        _ws = git_os.path.normpath(git_os.path.join(renpy.config.basedir, '..', '..', 'workshop', 'content', '331470', '1515489831')) + '/'
        git_destination = _ws
        return _ws

    def rpa_check_append(rpaf, rpan):
        global git_archives
        try:
            import os as git_os
            dest = _git_resolve_dest()
            full_path = git_os.path.join(dest, rpaf)
            if git_os.path.isfile(full_path):
                if rpan not in renpy.config.archives:
                    renpy.config.archives.append(rpan)
                if rpan not in git_archives:
                    git_archives.append(rpan)
        except Exception:
            pass

    def rpa_check_varinst(git_mod_id, git_mod_name, rpaf):
        global mods
        try:
            import os as git_os
            dest = _git_resolve_dest()
            full_path = git_os.path.join(dest, rpaf)
            if git_os.path.isfile(full_path):
                mods[git_mod_id] = git_mod_name
        except Exception:
            pass

    ###MOD CONFIGURATORS###

init 10 python:
    for a in git_archives:
        if a not in renpy.config.archives:
            renpy.config.archives.append(a)
    try:
        mods["knz_dwnl_git"] = u"{font=res/esgml_new.ttf}Everlasting Summer GitHub Mods Loader{/font}"
    except Exception:
        pass
    try:
        modsImages["knz_dwnl_git"] = ("ESGML.png", False)
    except Exception:
        pass
