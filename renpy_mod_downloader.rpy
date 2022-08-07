init:
    $ mods["knz_dwnl_git"]=u"{font=res/esgml_new.ttf}Everlasting Summer GitHub Mods Loader{/font}"
    $ esgml_ver = '4.0.8 RC3 Isatis'
    $ ch_pr = ''
    $ ready_ma = False
    $ ready_m = False
    # $ tindex = ''
    if persistent.git_mod_installed == None:
        $ persistent.git_mod_installed = []
    transform git_img_b():
        parallel:
            on idle:
                easeout_back 0.75 zoom 1.0
            on hover:
                easein_back 0.75 zoom 1.25
            on update:
                easeout_back 0.75 zoom 1.0
        parallel:
            on idle:
                easein 0.75 alpha 1.0
            on hover:
                easein 0.75 alpha 0.5
            on update:
                easein 0.75 alpha 1.0

    transform git_img_c():
        on idle:
            easein 0.75 alpha 1.0
        on hover:
            easein 0.75 alpha 0.5
        on update:
            easein 0.75 alpha 1.0

    transform git_img_u():
        easein 2 alpha 0
        easein 2 alpha 1.0




    image git_nfo = "res/git_nfo.png"
    $ nfo_text = ''
    $ m_nfo_text = ''
    $ git_queue = []



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

    $ tindex = ''
    $ git_not = ''
    $ git_not1 = ''
    $ global tindex

    $ git_destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'


label knz_dwnl_git:
    window hide
    $ config.mouse = {'default' : [("res/cursor.png", 0, 0)]}
    show black with dspr
    show image "res/git_warn.png" with dspr
    $ renpy.pause(5)
    show black with dspr
    play sound 'res/git_start.ogg'
    show image "res/git_splash.png" with dspr
    $ renpy.pause(2)
    play music 'res/git_main.ogg' fadein 5
    if _return == "mm":
        $ config.mouse = {'default' : [("images/misc/mouse/1.png", 0, 0)]}
        return
    call screen knz_git_dwnl_menu with dissolve

screen knz_info_screen(nfo_text, m_nfo_text):
    modal False
    add 'git_nfo'
    vbox xalign 0.5 yalign 0.5:
        text nfo_text xalign 0.5 at git_img_u:
            style "esgml_nn"
        null height 20
        text m_nfo_text xalign 0.5 at git_img_u:
            style "esgml_nm"
        null height 10
        text ch_pr xalign 0.5 at git_img_u:
            style "esgml_nm"




screen knz_git_dwnl_menu:
    $ import os as git_os
    $ import urlparse
    modal False

    window:
        xalign 0 yalign 0
        background "git_nfo"
        vbox xpos 0.05 ypos 0.175 yfill:

            text "Everlasting Summer Git Mods Loader":
                        style "esgml_mmn"
            null height 10
            text "Свободный репозиторий модов «Бесконечного лета»":
                        style "esgml_mn"
    side "r":
        area (0.05, 0.20, 0.8, 0.675)
        viewport id "git_mods_menu":
            draggable True
            mousewheel True
            scrollbars None
            has vbox
            for id in git_mod_lists:
                hbox spacing 10 ypos:

                    if str(id) in persistent.git_mod_installed:
                        add 'res/git_dwl_inactive.png' xalign 0.01
                    else:
                        imagebutton auto 'res/git_dwl_%s.png' action [Function(generate_index, id), SetScreenVariable("tindex", str(id)), Function(renpy.call_in_new_context, 'run_down2')] at git_img_b xalign 0.01


                    if str(id) in persistent.git_mod_installed:
                        add 'res/git_qu_inactive.png' xalign 0.01
                    elif str(id) in git_queue:
                        add 'res/git_qu_inactive.png' xalign 0.01
                    else:
                        imagebutton auto 'res/git_qu_%s.png' action [Function(git_queue.append, id), SetVariable("git_not", git_info[id]["name"] + '\nдобавлен в очередь загрузки'), Show("git_notice", dissolve)] at git_img_b xalign 0.01
                    #
                    #
                    if str(id) in persistent.git_mod_installed:
                        imagebutton auto 'res/git_del_%s.png' action [Function(generate_index, id), Function(renpy.call_in_new_context, 'deleter')] at git_img_b xalign 0
                    else:
                        add 'res/git_del_inactive.png' xalign 0

                    textbutton git_info[id]["name"] ypos -0.2125 action [Hide("knz_git_dwnl_menu", dissolve), Show('git_modnfo', dissolve, id)] at git_img_b:
                        style "esgml_mm"
                        text_style "esgml_mm"

                    # textbutton git_info[name]["name"] ypos -0.2125  action [Show('git_modnfo', dissolve, id)] at git_img_b:
                    #     style "esgml_mm"
                    #     text_style "esgml_mm"
    frame background Frame(Solid("0008")) left_padding 25 right_padding 25 bottom_padding 20 top_padding 25 xalign 0.5 ypos 0.900 xminimum 1920 xmaximum 1920:
        grid 6 1 spacing 96 xalign 0.5:

            imagebutton auto 'res/git_main_%s.png' action [SetField(config, "mouse", {'default' : [('images/misc/mouse/1.png', 0, 0)]}), MainMenu(confirm=False)] hovered [SetVariable("git_not1", "Вернуться в главное меню"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b

            imagebutton auto 'res/git_qu1_%s.png' action [Function(renpy.call_in_new_context, 'go_to_git_qu')] hovered [SetVariable("git_not1", "Очередь загрузки"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b

            imagebutton auto 'res/git_nlt_%s.png' action [Show("git_debug", dissolve)] hovered [SetVariable("git_not1", "Меню отладки"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b

            imagebutton auto 'res/git_rst_%s.png' action [Function(renpy.utter_restart)]  hovered [SetVariable("git_not1", "Перезагрузить"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b

            imagebutton auto 'res/git_nfo_%s.png' action [Function(renpy.call_in_new_context, 'go_to_git_authors')] hovered [SetVariable("git_not1", "Информация о моде"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b

            imagebutton auto 'res/git_exit_%s.png' action [Quit (confirm=False)]  hovered [SetVariable("git_not1", "Выйти из БЛ"), Show("git_notice_d", dissolve)] unhovered [SetScreenVariable("git_not1", " "), Hide("git_notice_d", dissolve)] at git_img_b


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
    timer 5.0 action Hide("git_notice", dissolve)

screen git_notice_d():
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.875 left_padding 10 right_padding 10 bottom_padding 10 top_padding 10:
        textbutton git_not1:
            style "esgml_not"
            text_style "esgml_not"

screen git_debug():
    frame background Frame(Solid("0008")) xalign 0.5 yalign 0.5 left_padding 25 right_padding 25 bottom_padding 25 top_padding 25:
        vbox:
            textbutton "Меню отладки" xalign 0.5:
                style "esgml_notb"
                text_style "esgml_notb"
            null height 25
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
            null height 25
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
    vbox xpos 0.05 ypos 0.05 yfill:
                    text "Очередь загрузки модов":
                                style "esgml_nn"
                    side "r":
                        area (0.05, 0.05, 0.7, 0.675)
                        viewport id "git_qu_menu":
                            draggable True
                            mousewheel True
                            scrollbars None
                            has vbox
                            if not git_queue:
                                textbutton "Очередь пуста" ypos -0.2125 at git_img_b:
                                    style "esgml_mm"
                                    text_style "esgml_mm"


                            else:
                                for id in git_queue:
                                    textbutton git_info[id]["name"] ypos -0.2125 at git_img_b:
                                        style "esgml_mm"
                                        text_style "esgml_mm"
    hbox yalign 0.975 xalign 0.5 spacing 96:
        if git_queue:
            textbutton 'Загрузить' action [Function(git_qu_dwl)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"
            textbutton 'Очистить' action [Function(git_qu_clr)] at git_img_b:
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
        textbutton 'Назад' action [Show('knz_git_dwnl_menu', dissolve), Hide('git_qus')] at git_img_b:
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

        textbutton 'Назад' ypos 0.8 action [Show('knz_git_dwnl_menu', dissolve), Hide('git_modnfo')] at git_img_b:
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
                textbutton '(уже загружен)':
                        style "esgml_bb"
                        text_style "esgml_bb"
            else:
                textbutton 'Загрузить' action [Function(generate_index, id), SetScreenVariable("tindex", str(id)), Function(renpy.call_in_new_context, 'run_down2')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                textbutton '(не загружен)':
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
                    imagebutton idle im.Scale(git_info[id]['scr1'], 480, 270) hover im.Scale(git_info[id]['scr1'], 480, 270) action [Show('git_image', dissolve, git_info[id]['scr1'], id)] at git_img_c
                    imagebutton idle im.Scale(git_info[id]['scr2'], 480, 270) hover im.Scale(git_info[id]['scr2'], 480, 270) action [Show('git_image', dissolve, git_info[id]['scr2'], id)] at git_img_c
                    imagebutton idle im.Scale(git_info[id]['scr3'], 480, 270) hover im.Scale(git_info[id]['scr3'], 480, 270) action [Show('git_image', dissolve, git_info[id]['scr3'], id)] at git_img_c
                text git_info[id]['desc'] yalign 0.55 xalign 0.5:
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
        tindex = str(id)
        global tindex

    kprogress = None

    def git_clear_index():
        persistent.git_mod_installed = []
        git_not = "Индексы успешно очищены"
        global git_not
        renpy.show_screen('git_notice')
        # git_not = ""
        # global git_not

    def git_manual_index(id, mode):
        if mode == 1:
            persistent.git_mod_installed.append(id)
            git_not = "Индекс успешно добавлен"
        if mode == 0:
            persistent.git_mod_installed.remove(id)
            git_not = "Индекс успешно очищен"
        global git_not
        renpy.show_screen('git_notice')
        # git_not = ""
        # global git_not


    def knz_dnwl_mod(filename, filelink):

        global ch_pr
        ch_pr = "Инициализация..."
        ready_ma = False
        import urllib2, ssl
        try:
            ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = ssl._create_unverified_context
        opener = urllib2.build_opener()
        opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")]
        response = opener.open(filelink)
        CHUNK = 16 * 1024
        meta = response.info()
        ch_full_4 = meta.getheaders("Content-Length")
        ch_ful_4 = "".join(ch_full_4)
        ch_full_3 = float(ch_ful_4)
        ch_full_2 = (ch_full_3 / 1000) / 1000
        ch_full_1 = round(ch_full_2, 2)
        ch_full = str(ch_full_1)
        with open(filename, 'wb') as f:
            while True:
                ch_pr_b = float(git_os.stat(filename).st_size)
                ch_pr_mb = (ch_pr_b / 1000) / 1000
                ch_pr_r = round(ch_pr_mb, 2)
                ch_pr_st = str(ch_pr_r)
                ch_real_2 = (ch_pr_mb / ch_full_1 * 100)
                ch_real_1 = round(ch_real_2, 1)
                ch_real = str(ch_real_1) #Item::progress = double(Item::bytes_processed) / Item::total_bytes * 100;
                ch_pr = "Загружено " + ch_pr_st  + " из " + ch_full + " МБ (" + ch_real + "%)" + "\nИмя файла: " + str(filename)
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
        git_tset = git_os.path.isfile(filename)
        global git_tset
        shutil.move(filename, git_destination + filename)
        ch_pr_b = float(git_os.stat(git_destination + filename).st_size)
        ch_pr_mb = (ch_pr_b / 1000) / 1000
        ch_pr_r = round(ch_pr_mb, 2)
        ch_pr_st = str(ch_pr_r)
        ch_pr = "Загружено " + ch_pr_st + " из " + ch_full + " МБ (" + ch_real + "%)" + "\nИмя файла: " + str(filename)

    ###MOD CHECKER###

init -10 python:
    git_archives = []
    def rpa_check_append(rpaf, rpan):
        import os as git_os
        global git_archives
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        try:
            file = open(destination + rpaf)
        except IOError as e:
            pass
        else:
            with file:
                config.archives.append(rpan)
                git_archives.append(rpan)




    def rpa_check_varinst(git_mod_id, git_mod_name, rpaf):
        global mods
        import os as git_os
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        try:
            file = open(destination + rpaf)
        except IOError as e:
            pass
        else:
            with file:
                    mods[git_mod_id]=git_mod_name

    ###MOD CONFIGURATORS###


init 10 python:
    for a in git_archives:
        config.archives.append(a)
    try:
        modsImages["knz_dwnl_git"] = ("ESGML.png", False)
    except:
        pass
