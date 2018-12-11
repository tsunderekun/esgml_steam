init:
    $ mods["knz_dwnl_git"]=u"{font=res/esgml_new.otf}Everlasting Summer GitHub Mods Loader{/font}"
    $ esgml_ver = 'Electron 2.7b'

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



    $ style.esgml_mm = Style(style.default)
    $ style.esgml_mm.color = (255, 255, 255, 100)
    $ style.esgml_mm.hover_color = (255, 255, 255, 55)
    $ style.esgml_mm.size = 55
    $ style.esgml_mm.font = "res/esgml_new.otf"
    $ style.esgml_mm.text_align = 0.5

    $ style.esgml_bb = Style(style.esgml_mm)
    $ style.esgml_bb.text_align = 2
    $ style.esgml_bb.size = 72

    $ style.esgml_ii = Style(style.esgml_mm)
    $ style.esgml_ii.font = "res/esgml_descr.otf"
    $ style.esgml_ii.text_align = 0.5
    $ style.esgml_ii.size = 32
    $ style.esgml_ii.color = (255, 255, 255, 100)

    $ style.esgml_nn = Style(style.esgml_mm)
    $ style.esgml_nn.color = (255, 255, 255, 100)
    $ style.esgml_nn.size = 80

    $ style.esgml_nm = Style(style.esgml_nn)
    $ style.esgml_nm.size = 40

    $ style.esgml_mn = Style(style.esgml_nm)
    $ style.esgml_mn.size = 40
    $ style.esgml_mn.color = (255, 255, 255, 100)

    $ style.esgml_mmn = Style(style.esgml_mn)
    $ style.esgml_mmn.size = 80



    $ git_destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'


    $ git_descr = {
        'dwl' : {
                'desc':'Небольшой мод по одноимённому фанфику. События мода начинаются в седьмой день, когда Семён покидает Лену, думая лишь о том, чтобы поскорее вернуться домой. Но вернувшись в домик Лены, он видит, что Лена умирает...',
                'scr1':'git_screens/dwl (1).png',
                'scr2':'git_screens/dwl (2).png',
                'scr3':'git_screens/dwl (3).png'
                },
        'vkun' : {
                'desc':'Заблудившись в тумане, молодой солдат, находит вход в мифический, кишащий монстрами лагерь...',
                'scr1':'git_screens/vkun (1).png',
                'scr2':'git_screens/vkun (2).png',
                'scr3':'git_screens/vkun (3).png'
                },
        'ev' : {
                'desc':'Все мы уже давно хорошо знаем историю Семёна, переживавшего в "Совёнке" многочисленные циклы с разными исходами и результатами. Мы слышали множество вариантов предысторий и продолжений, альтернативных взглядов на старые события. И вот ещё один из них. Что будет, если в лагерь вместе с Семёном попадёт кто-то ещё? Человек, частично похожий на него, но при этом абсолютный ему антипод. Как он проживёт эти 7 дней и какое место займёт в них Семён? Узнаете, познакомившись с проектом "Бесконечные Каникулы". ',
                'scr1':'git_screens/ev (1).png',
                'scr2':'git_screens/ev (2).png',
                'scr3':'git_screens/ev (3).png'
                },
        'bm' : {
                'desc':'Мод повествует о жизни обычного московского студента Михаила, живущего скучной жизнью в своей небольшой квартире. Михаил часто прогуливает занятия и живет только сам для себя. Сможет ли нашего героя изменить к лучшему неделя в "Совёнке"? Он и сам этого не знает. Но, попав в лагерь, он начинает замечать странные вещи, которые всерьез его настораживают и даже пугают. Чем закончится его летнее приключение? Об этом вы узнаете из нашего мода. ',
                'scr1':'git_screens/bm (1).png',
                'scr2':'git_screens/bm (2).png',
                'scr3':'git_screens/bm (3).png'
                },
        'st' : {
                'desc':'Расскажет иную историю про парня по имени Семен. Который оказался не в самой обычной ситуации. - О чем мод? —-Об альтернативной реальности, в которую попал наш герой. Так же в моде есть множество отсылок из реальной жизни, с которым вы можете столкнуться. (И это не просто так, весь сценарий и исход событий будет зависеть от вас.) Оригинальный сценарий мода. Это стандартная семидневная смена в лагере Совёнок. В нем вы узнаете истинные помыслы главных героев игры. Выберитесь из цикла(С той которую вы выберите) А так же узнаете почему Семён потерял память.',
                'scr1':'git_screens/st (1).png',
                'scr2':'git_screens/st (2).png',
                'scr3':'git_screens/st (3).png'
                },
        'ls' : {
                'desc':'',
                'scr1':'git_screens/ls (1).png',
                'scr2':'git_screens/ls (2).png',
                'scr3':'git_screens/ls (3).png'
                },
        'la' : {
                'desc':'',
                'scr1':'git_screens/la (1).png',
                'scr2':'git_screens/la (2).png',
                'scr3':'git_screens/la (3).png'
                },
        'twat' : {
                'desc':'',
                'scr1':'',
                'scr2':'',
                'scr3':''
                },
        'v17' : {
                'desc':'',
                'scr1':'git_screens/v17 (1).png',
                'scr2':'git_screens/v17 (2).png',
                'scr3':'git_screens/v17 (3).png'
                },
        'emk1' : {
                'desc':'',
                'scr1':'git_screens/emk1 (1).png',
                'scr2':'git_screens/emk1 (2).png',
                'scr3':'git_screens/emk1 (3).png'
                },
        'rs' : {
                'desc':'Мод расскажет про альтернативное развитие событий уже известного всем романа. Пару неприятностей здесь всё-таки случилось. Но пугаться нечего, потому что почти у каждой истории есть хороший конец, и наша не исключение. \n Мод берёт своё начало сразу после окончания смены в лагере, где Семён прощается с Сэм.\n Модификация является представителем жанра триллер с отголосками романтики и драмы, а так же будет ориентироваться на вдумчивого читателя, который не ограничится написанным и раскроет ещё больше в своей фантазии.',
                'scr1':'git_screens/rs (1).png',
                'scr2':'git_screens/rs (2).png',
                'scr3':'git_screens/rs (3).png'
                },
        'hs' : {
                'desc':'Сюжет данного мода разворачивается во время второго визита главного героя в "Совёнок". В отличии от предыдущих витков все пионеры не потеряли память и помнят, что произошло прошлым лето, а Семён сделал этот выбор сознательно. Старые знакомые, увлекательная компания, замечательное лето... но не всё так гладко. Вскоре все узнают, что эта смена будет не совсем обычной, и им придётся бороться за то, чтобы увидеть её конец.\n • Вас ждёт увлекательное приключение с большим многообразием ответвлений и различных выборов, события одного и того же дня могут разворачиваться совершенно по другому.\n • Общайтесь с персонажами, но помните: ваши действия могут как улучшить взаимоотношения, так и испортить их.\n • Взаимодействуйте с миром в интерактивных заданиях. Наведите курсор на изображение на экране, чтобы взаимодействовать с ним.\n • Со временем сюжет будет уже не похож на простую прогулку по лагерю, а превратиться в суровое выживание, где от ваших выборов будет зависеть, кто сможет дойти до конца, а кто - нет. \n • Каждое событие имеет свои чёткие причины и последствия. Поэтому не спешите делать выбор и задумайтесь. \n Углубитесь в прошлое и узнайте причину происходящих здесь кошмаров. Сможете ли вы пройти через это испытание невредимым и спасти дорогих и близких людей? По силам ли вам спасти всех и разблокировать Героическую концовку?',
                'scr1':'git_screens/hs (1).png',
                'scr2':'git_screens/hs (2).png',
                'scr3':'git_screens/hs (3).png'
                },
        'idnh' : {
                'desc':'Наш главный герой, Иван Смирнов, обычный ученик колледжа на четвёртом году обучения, которому приспичило не спать четверо суток и играть в новеллу «Бесконечное лето». Казалось бы, с кем не бывает? Но в один момент, он засыпает у себя дома и видит сон, где двое мужчин обсуждают захоронение заживо какой-то девочки, что прокляла всю деревню. Проснувшись, Ваня идёт на кухню промыть нос, который был у него в крови, а потом неожиданно падает в обморок. Вдруг Ваня появляется в заброшеном пионерлагере «Совёнок» и… забывает всю свою прошлую жизнь.\n Пребывая малое количество времени в этом, казалось бы, райском и безлюдном месте, он натыкается на могилы умерших пионеров, в том числе и... свою! Что же случилось с ними и что он должен сделать, чтобы изменить череду событий в лучшую сторону? Однако его ещё и успевают убить… ',
                'scr1':'git_screens/idnh (1).png',
                'scr2':'git_screens/idnh (2).png',
                'scr3':'git_screens/idnh (3).png'
                },
    }


    $ mods_names = [
    ('dwl', "Дни с Леной", "git_dayswithlena.rpyc", "git_dayswithlena_res.rpa", "dayswithlena/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena_res.rpa", git_destination),

    ('vkun', "Совенок в тумане", "git_vkun_fog.rpyc", "VKUN_MOD.rpa", "vkun_fog/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_vkun_fog.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/VKUN_MOD.rpa", git_destination),

    ('ev', "Бесконечные Каникулы", "git_vacations_base.rpyc", "git_vacations.rpa", "git_vacations/", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations_base.rpyc", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations.rpa", git_destination),

    ('bm', "Большая Ошибка", "git_bm_base.rpyc", "git_bm.rpa", "git_bm/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm.rpa", git_destination),

    ('st', "Время Лета", "git_sumtime_base.rpyc", "git_sumtime.rpa", "git_sumtime/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime.rpa", git_destination),

    ('ls', "История Лены", "git_lena_story_base.rpyc", "git_lena_story.rpa", "git_lena_story/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story.rpa", git_destination),

    ('la' ,"Лена. Альтернативная концовка", "git_lena_alternate_base.rpyc", "git_lena_alternate.rpa", "git_lena_alternate/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate.rpa", git_destination),

    ('emk1', "Эпилог МК1", "emk1_base.rpyc", "emk1.rpa", "emk1/", "https://github.com/tsunderekun/es_gitmods/raw/master/emk1_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/emk1.rpa", git_destination),

    ('v17', "Где мои семнадцать лет?", "base_v17.rpyc", "git_v17.rpa", "v17/", "https://github.com/tsunderekun/es_gitmods/raw/master/base_v17.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_v17.rpa", git_destination),

    ('rs', "Чёрная страница из дневника Сэм", "rs_base.rpyc", "rs_common.rpa", "rs_base/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_common.rpa", git_destination),

    ('hs', "Ужасное Лето", "hs_base.rpyc", "hs_common.rpa", "hs_base/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_common.rpa", git_destination),

    ('idnh', "Re: I Do Not Have", "idnh_base.rpyc", "idnh_common.rpa", "idnh_base/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_idnh/idnh_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_idnh/idnh_common.rpa", git_destination),
    ]




label knz_dwnl_git:
    $ config.mouse = {'default' : [("res/cursor.png", 0, 0)]}
    play music 'res/git_main.ogg' fadein 5
    if _return == "mm":
        $ config.mouse = {'default' : [("images/misc/mouse/1.png", 0, 0)]}
        return
    if persistent.evn_del == True:
        call screen non_supp_mod with dissolve
    else:
        call screen knz_git_dwnl_menu with dissolve

screen knz_info_screen(nfo_text, m_nfo_text):
    modal False
    add 'git_nfo'
    text nfo_text xalign 0.5 yalign 0.45 at git_img_u:
        style "esgml_nn"
    text m_nfo_text xalign 0.5 yalign 0.54 at git_img_u:
        style "esgml_nm"

screen non_supp_mod:
    modal False
    window:
        xalign 0 yalign 0
        background "git_nfo"
        text "Был удален более несовместимый мод \"[persistent.evn_deln]\"." xalign 0.5 yalign 0.45:
            style "esgml_nn"
        textbutton "Я понял. Продолжить." action [Function(renpy.call_in_new_context, 'esgml_countinue')] xalign 0.5 yalign 0.60 at git_img_b:
            style "esgml_bb"
            text_style "esgml_bb"

label esgml_countinue:

    $ persistent.evn_del = False
    $ persistent.evn_deln = ""
    jump knz_dwnl_git



screen knz_git_dwnl_menu:
    $ import os as git_os
    modal False
    window:
        xalign 0 yalign 0
        background "git_nfo"
        vbox xpos 0.0725 ypos 0.175 yfill:

            text "Everlasting Summer Git Mods Loader":
                        style "esgml_mmn"
            null height 10
            text "Свободный репозиторий модов для Бесконечного Лета":
                        style "esgml_mn"

    side "c r":
        area (0.05, 0.225, 0.9, 0.675)
        viewport id "git_mods_menu":
            draggable True
            mousewheel True
            scrollbars None

            has vbox
            for id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination in mods_names:
                hbox spacing 10 ypos:

                    if git_os.path.isfile(destination + rpa_f):
                        add 'res/git_dwl_inactive.png' xalign 0.01
                    else:
                        imagebutton auto 'res/git_dwl_%s.png' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'run_down')] at git_img_b xalign 0.01


                    if git_os.path.isfile(destination + rpa_f):
                        imagebutton auto 'res/git_del_%s.png' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'deleter')] at git_img_b xalign 0
                    else:
                        add 'res/git_del_inactive.png' xalign 0

                    textbutton name ypos -0.2125  action [Show('git_modnfo', dissolve, id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination)] at git_img_b:
                        style "esgml_mm"
                        text_style "esgml_mm"

    hbox yalign 0.975 xalign 0.5 spacing 144:
        if 'NLT_tl' in globals():
            textbutton 'NLT Modpack' action [Function(renpy.call_in_new_context, 'NLT_toolbox')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
        else:
            textbutton 'NLT Modpack' action [OpenURL('steam://url/CommunityFilePage/847728687')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"

        textbutton 'Главное меню' action [SetField(config, "mouse", {'default' : [('images/misc/mouse/1.png', 0, 0)]}), Return("mm")] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"


        textbutton 'Выход' action [Quit (confirm=False)] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"

        textbutton '©' action [Function(renpy.call_in_new_context, 'go_to_git_authors')] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"

label go_to_git_authors:
    if _return == "mm":
        return
    call screen git_authors with fade

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

        text "Загрузчик удаленных модов для Бесконечного лета. \nСоздан для того, чтобы вы могли играть в удаленные моды. \nА также, вы всегда можете помочь нам с их добавлением \nперейдя в официальную группу." text_align 0.0 xpos 0.025:
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

        null height 20

        textbutton "Проект распространяется под лицензией CC BY-NC-SA 4.0" xpos 0.025 action OpenURL('https://creativecommons.org/licenses/by-nc-sa/4.0/') at git_img_b:
            style "esgml_nm"
            text_style "esgml_nm"

        null height 50

        textbutton 'Назад' ypos 0.8 action [Show('knz_git_dwnl_menu', dissolve), Hide('git_modnfo')] at git_img_b:
                style "esgml_bb"
                text_style "esgml_bb"



screen git_modnfo(id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination):
    modal False
    add "git_nfo"
    text name yalign 0.05 xalign 0.1:
        style "esgml_nn"
    hbox spacing 64 yalign 0.9 xalign 0.5:
            textbutton 'Назад' action [Show('knz_git_dwnl_menu', dissolve), Hide('git_modnfo')] at git_img_b:
                    style "esgml_bb"
                    text_style "esgml_bb"


            if git_os.path.isfile(destination + rpa_f):
                textbutton 'Удалить' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'deleter')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                textbutton 'Уже загружен':
                        style "esgml_bb"
                        text_style "esgml_bb"
            else:
                textbutton 'Загрузить' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'run_down')] at git_img_b:
                        style "esgml_bb"
                        text_style "esgml_bb"
                textbutton 'Не установлен':
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
                    imagebutton idle im.Scale(git_descr[id]['scr1'], 480, 270) hover im.Scale(git_descr[id]['scr1'], 480, 270) action [Show('git_image', dissolve, git_descr[id]['scr1'], id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination)] at git_img_c
                    imagebutton idle im.Scale(git_descr[id]['scr2'], 480, 270) hover im.Scale(git_descr[id]['scr2'], 480, 270) action [Show('git_image', dissolve, git_descr[id]['scr2'], id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination)] at git_img_c
                    imagebutton idle im.Scale(git_descr[id]['scr3'], 480, 270) hover im.Scale(git_descr[id]['scr3'], 480, 270) action [Show('git_image', dissolve, git_descr[id]['scr3'], id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination)] at git_img_c
                text git_descr[id]['desc'] yalign 0.55 xalign 0.5:
                    style "esgml_ii"
                    xmaximum 0.90


screen git_image(img, id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination):
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
        action [Hide('git_image'), Show('git_modnfo', dissolve, id, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination)]



init 999 python:
    config.archives.append('res_git')



init python:
    from threading import Thread
    import os as git_os
    import shutil

    kprogress = None
    knz_rpyc_p = None
    knz_rpyc_f = None
    knz_rpyc_l = None
    knz_rpa_f = None
    knz_rpa_l = None

    def knz_get_data(rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l):
        global knz_rpyc_p
        global knz_rpyc_f
        global knz_rpyc_l
        global knz_rpa_f
        global knz_rpa_l
        knz_rpyc_f = rpyc_f
        knz_rpyc_l = rpyc_l
        knz_rpyc_p = rpyc_p
        knz_rpa_f = rpa_f
        knz_rpa_l = rpa_l


    def knz_dnwl_mod_base(mfolder, baserpyc, rpyclink):

        # global f_percent
        destination = git_destination + mfolder
        git_os.mkdir(destination)
        from urllib2 import urlopen
        response = urlopen(rpyclink)
        CHUNK = 16 * 1024
        with open(baserpyc, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
        git_os.rename(baserpyc, destination + baserpyc)

    def knz_dnwl_mod(baserpa, rpalink):

        from urllib2 import urlopen
        response = urlopen(rpalink)
        CHUNK = 16 * 1024
        with open(baserpa, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
        git_os.rename(baserpa, git_destination + baserpa)


    def knz_git_mod_clean(baserpa, mfolder):
        shutil.rmtree(git_destination + mfolder, ignore_errors=True, onerror=None)
        renpy.hide_screen('knz_git_dwnl_menu')
        nfo_text = 'Удаление'
        m_nfo_text = 'Выполняется удаление указанного мода, ожидайте...'
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        renpy.pause (1, hard=True)
        try:
            persistent.del_baserpa = git_destination + baserpa
            persistent.unbaserpa = baserpa[:-4]
            renpy.pause (2, hard=True)
            nfo_text = 'Перезагрузка'
            m_nfo_text = 'Ожидайте, пожалуйста.'
            renpy.hide_screen('knz_info_screen')
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)
            renpy.utter_restart()
        except OSError, e:
            renpy.hide_screen('knz_info_screen')
            nfo_text = 'Ошибка!'
            m_nfo_text = 'Мы не знаем, как это произошло... Возможно ошибка на сервере.\nМожет быть, у вас проблемы c атрибутами папок...'
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)
            renpy.utter_restart()


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
