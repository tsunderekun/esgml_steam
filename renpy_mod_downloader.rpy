init:
    $ mods["knz_dwnl_git"]=u"{font=res/esgml_new.otf}Everlasting Summer GitHub Mods Loader{/font}"
    $ esgml_ver = 'Electron 2.8'
    $ ch_pr = ''
    $ ready_ma = False
    $ ready_m = False
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
                'desc':'\nНебольшой мод по\xa0одноимённому фанфику.\n\nСобытия мода начинаются с\xa0седьмого дня пребывания в\xa0лагере, когда Семён покидает Лену, думая\xa0лишь\xa0о\xa0том, как\xa0поскорее попасть домой. Но\xa0вернувшись в\xa0домик Лены, он\xa0видит, что\xa0она умирает...\n',
                'scr1':'git_screens/dwl (1).png',
                'scr2':'git_screens/dwl (2).png',
                'scr3':'git_screens/dwl (3).png'
                },
        'vkun' : {
                'desc':'\nЗаблудившись в\xa0тумане, молодой солдат находит мифический, кишащий монстрами лагерь...\n',
                'scr1':'git_screens/vkun (1).png',
                'scr2':'git_screens/vkun (2).png',
                'scr3':'git_screens/vkun (3).png'
                },
        'ev' : {
                'desc':'\nВсе мы хорошо знаем историю Семёна, пережившего в\xa0«Совёнке» множество циклов с\xa0различными исходами. Мы\xa0слышали массу вариантов предыстории и\xa0продолжения, альтернативных взглядов на\xa0произошедшие события. Этот\xa0рассказ —\xa0один из\xa0таких вариантов.\n\nЧто\xa0будет, если\xa0вместе с\xa0Семёном в\xa0лагерь попадёт кто-то\xa0ещё? Человек, частично похожий на\xa0него, но\xa0при\xa0этом его абсолютный антипод. Как\xa0он проживёт эти 7\xa0дней, и\xa0какое место займёт в\xa0них Семён? Узнаете, познакомившись с\xa0данным модом.\n',
                'scr1':'git_screens/ev (1).png',
                'scr2':'git_screens/ev (2).png',
                'scr3':'git_screens/ev (3).png'
                },
        'bm' : {
                'desc':'\nЭто история обычного московского студента Михаила, живущего обычной скучной жизнью в\xa0небольшой квартире. Михаил\xa0часто прогуливает занятия и\xa0живёт, в\xa0общем-то, сам\xa0для\xa0себя. Попав в\xa0неизвестный для\xa0себя лагерь, он\xa0замечает странные вещи, которые всерьёз его\xa0настораживают и даже пугают.\n\nЧем\xa0закончится его летнее приключение? Сможет\xa0ли неделя в\xa0«Совёнке» изменить нашего героя к\xa0лучшему? Он\xa0и\xa0сам этого не\xa0знает.\n',
                'scr1':'git_screens/bm (1).png',
                'scr2':'git_screens/bm (2).png',
                'scr3':'git_screens/bm (3).png'
                },
        'st' : {
                'desc':'\nОтличная от\xa0оригинальной история парня по\xa0имени Семён, который\xa0оказался не\xa0в\xa0самой обычной для\xa0него ситуации —\xa0в\xa0альтернативной реальности.\n\nМод\xa0повествует о\xa0стандартной семидневной смене в\xa0лагере «Совёнок». Здесь\xa0вы\xa0найдёте множество отсылок, с\xa0которыми можете столкнуться в\xa0реальной жизни (и\xa0это не\xa0просто\xa0так: весь сценарий и\xa0исход событий будет зависеть от\xa0вас), узнаете истинные помыслы героев игры, покинете цикл с\xa0той девушкой, которую\xa0выберите сами, а\xa0также узнаете, почему Семён потерял память.\n',
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
                'desc':'\nМод расскажет об\xa0альтернативном развитии событий уже известного всем романа. Однако\xa0главного героя здесь всё-таки ждёт пара неприятностей. Но\xa0пугаться нечего, потому\xa0что почти у\xa0каждой истории есть хороший конец, и\xa0эта —\xa0не\xa0исключение. \n\n История берёт своё начало сразу после окончания смены в\xa0лагере, когда\xa0Семён прощается с\xa0Сэм. Это\xa0триллер с\xa0отголосками романтики и\xa0драмы, ориентированный на\xa0читателя вдумчивого и\xa0открытого к\xa0полёту фантазии.\n',
                'scr1':'git_screens/rs (1).png',
                'scr2':'git_screens/rs (2).png',
                'scr3':'git_screens/rs (3).png'
                },
        'hs' : {
                'desc':'\nСюжет данного мода разворачивается во\xa0время второго визита главного героя в\xa0«Совёнок». Однако на\xa0этот\xa0раз все пионеры лагеря помнят события прошлого лета. Но,\xa0в\xa0отличие от\xa0остальных, Семён\xa0сделал этот\xa0выбор сознательно. Его\xa0ждут старые знакомые, увлекательная компания, замечательное лето... но\xa0не\xa0всё пройдёт гладко. Для\xa0героев мода эта\xa0смена окажется не\xa0совсем обычной, и\xa0им придётся бороться за\xa0то, чтобы увидеть её\xa0конец.\n\n • Погружайтесь в\xa0увлекательное приключение с\xa0большим количеством ответвлений и\xa0различных выборов (события одного и\xa0того\xa0же дня могут разворачиваться совершенно по-разному).\n • Общайтесь с\xa0персонажами, но помните: ваши действия могут как улучшить отношения с\xa0ними, так\xa0и\xa0испортить.\n • Взаимодействуйте с\xa0миром в\xa0интерактивных заданиях (наводите курсор на\xa0изображение на\xa0экране, чтобы взаимодействовать с\xa0элементами сцены).\n • Со\xa0временем сюжет мода перестанет быть похожим на\xa0простую прогулку по\xa0лагерю и\xa0превратится в\xa0суровую игру на\xa0выживание, где\xa0от\xa0ваших действий будет зависеть, кто\xa0из\xa0героев сможет дойти до\xa0конца смены. \n • Каждое событие имеет свои чёткие причины и\xa0последствия. Поэтому не\xa0спешите и\xa0хорошенько обдумывайте каждое своё\xa0решение. \n\n Углубитесь в\xa0прошлое и\xa0узнайте причину происходящих в\xa0лагере кошмаров. Сможет\xa0ли Семён пройти через\xa0это\xa0испытание и\xa0остаться невредимым? По\xa0силам\xa0ли ему спасти дорогих и\xa0близких\xa0себе людей, а\xa0вам —\xa0разблокировать Героическую концовку?\n',
                'scr1':'git_screens/hs (1).png',
                'scr2':'git_screens/hs (2).png',
                'scr3':'git_screens/hs (3).png'
                },
        'idnh' : {
                'desc':'\nГлавный герой мода —\xa0Иван Смирнов, обычный\xa0ученик колледжа на\xa0четвёртом году обучения, которому\xa0приспичило не\xa0спать четверо суток подряд и\xa0играть в\xa0новеллу «Бесконечное лето». Казалось\xa0бы, с\xa0кем не\xa0бывает? Но\xa0однажды он засыпает у\xa0себя дома и\xa0видит сон, в\xa0котором двое мужчин обсуждают захоронение заживо какой-то девочки, что\xa0прокляла всю\xa0деревню. Проснувшись, Ваня идёт на\xa0кухню промыть затёкший кровью нос и\xa0неожиданно падает в\xa0обморок... \n\nПридя\xa0в\xa0себя, он\xa0оказывается в\xa0заброшенном пионерлагере «Совёнок». Ваня забывает всю\xa0свою\xa0прошлую жизнь. Проведя в\xa0этом казалось\xa0бы райском и\xa0безлюдном месте какое-то время, он\xa0однажды натыкается на\xa0могилы умерших пионеров, в\xa0том\xa0числе и\xa0свою.\n\nЧто\xa0же случилось с\xa0ними? И\xa0что он должен сделать, чтобы изменить череду событий в\xa0лучшую сторону?\n',
                'scr1':'git_screens/idnh (1).png',
                'scr2':'git_screens/idnh (2).png',
                'scr3':'git_screens/idnh (3).png'
                },
        '8dl' : {
                'desc':'\nЭтот мод —\xa0альтернативный взгляд на\xa0историю и\xa0вселенную игры. Он\xa0содержит собственный оригинальный сценарий, множество новых иллюстраций, а\xa0также имеет почти\xa0полностью переосмысленное музыкальное сопровождение.\n',
                'scr1':'git_screens/8dl (1).jpg',
                'scr2':'git_screens/8dl (2).png',
                'scr3':'git_screens/8dl (3).jpg'
                },
    }


    $ mods_names = [
    ('8dl', "7 дней лета («амбальская» версия)", "7dl_esgml_init.rpyc", "7dl.rpa", "7dl/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/7dl/7dl_esgml_init.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/7dl/7dl.rpa", git_destination),

    ('dwl', "Дни с Леной", "git_dayswithlena.rpyc", "git_dayswithlena_res.rpa", "dayswithlena/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena_res.rpa", git_destination),

    ('vkun', "Совёнок в тумане", "git_vkun_fog.rpyc", "VKUN_MOD.rpa", "vkun_fog/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_vkun_fog.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/VKUN_MOD.rpa", git_destination),

    ('ev', "Бесконечные каникулы", "git_vacations_base.rpyc", "git_vacations.rpa", "git_vacations/", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations_base.rpyc", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations.rpa", git_destination),

    ('bm', "Большая ошибка", "git_bm_base.rpyc", "git_bm.rpa", "git_bm/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm.rpa", git_destination),

    ('st', "Время лета", "git_sumtime_base.rpyc", "git_sumtime.rpa", "git_sumtime/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime.rpa", git_destination),

    ('ls', "История Лены", "git_lena_story_base.rpyc", "git_lena_story.rpa", "git_lena_story/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story.rpa", git_destination),

    ('la' ,"Лена. Альтернативная концовка", "git_lena_alternate_base.rpyc", "git_lena_alternate.rpa", "git_lena_alternate/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate.rpa", git_destination),

    ('emk1', "Эпилог МК1", "emk1_base.rpyc", "emk1.rpa", "emk1/", "https://github.com/tsunderekun/es_gitmods/raw/master/emk1_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/emk1.rpa", git_destination),

    ('v17', "Где мои семнадцать лет?", "base_v17.rpyc", "git_v17.rpa", "v17/", "https://github.com/tsunderekun/es_gitmods/raw/master/base_v17.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_v17.rpa", git_destination),

    ('rs', "Чёрная страница из дневника Сэм", "rs_base.rpyc", "rs_common.rpa", "rs_base/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_common.rpa", git_destination),

    ('hs', "Ужасное лето", "hs_base.rpyc", "hs_common.rpa", "hs_base/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_common.rpa", git_destination),

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
    text ch_pr xalign 0.5 yalign 0.61 at git_img_u:
        style "esgml_nm"

screen non_supp_mod:
    modal False
    window:
        xalign 0 yalign 0
        background "git_nfo"
        text "Был удалён более несовместимый мод \"[persistent.evn_deln]\"." xalign 0.5 yalign 0.45:
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
            text "Свободный репозиторий модов «Бесконечного лета»":
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

        null height 20

        textbutton "Проект распространяется по лицензии CC BY-NC-SA 4.0" xpos 0.025 action OpenURL('https://creativecommons.org/licenses/by-nc-sa/4.0/') at git_img_b:
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
                textbutton '(уже загружен)':
                        style "esgml_bb"
                        text_style "esgml_bb"
            else:
                textbutton 'Загрузить' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'run_down')] at git_img_b:
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
        global ready_m
        ready_m = False
        destination = git_destination + mfolder
        git_os.mkdir(destination)
        from urllib2 import urlopen
        response = urlopen(rpyclink)
        CHUNK = 16 * 1024
        with open(baserpyc, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    ready_m = True
                    break
                f.write(chunk)
        git_os.rename(baserpyc, destination + baserpyc)

    def knz_dnwl_mod(baserpa, rpalink):
        global ready_ma
        global ch_pr
        ch_pr = "Инициализация..."
        ready_ma = False
        from urllib2 import urlopen
        response = urlopen(rpalink)
        CHUNK = 16 * 1024
        meta = response.info()
        ch_full_4 = meta.getheaders("Content-Length")
        ch_ful_4 = "".join(ch_full_4)
        ch_full_3 = float(ch_ful_4)
        ch_full_2 = (ch_full_3 / 1000) / 1000
        ch_full_1 = round(ch_full_2, 2)
        ch_full = str(ch_full_1)
        with open(baserpa, 'wb') as f:
            while True:
                ch_pr_b = float(git_os.stat(baserpa).st_size)
                ch_pr_mb = (ch_pr_b / 1000) / 1000
                ch_pr_r = round(ch_pr_mb, 2)
                ch_pr_st = str(ch_pr_r)
                ch_real_2 = (ch_pr_mb / ch_full_1 * 100)
                ch_real_1 = round(ch_real_2, 1)
                ch_real = str(ch_real_1) #Item::progress = double(Item::bytes_processed) / Item::total_bytes * 100;
                ch_pr = "Загружено " + ch_pr_st  + " из " + ch_full + " МБ (" + ch_real + "%)"

                chunk = response.read(CHUNK)
                if not chunk:
                    ready_ma = True
                    break
                f.write(chunk)
        git_os.rename(baserpa, git_destination + baserpa)
        ch_pr_b = float(git_os.stat(git_destination + baserpa).st_size)
        ch_pr_mb = (ch_pr_b / 1000) / 1000
        ch_pr_r = round(ch_pr_mb, 2)
        ch_pr_st = str(ch_pr_r)
        ch_pr = "Загружено " + ch_pr_st + " из " + ch_full + " МБ (" + ch_real + "%)"


    def knz_git_mod_clean(baserpa, mfolder):
        global ch_pr
        ch_pr = ''
        shutil.rmtree(git_destination + mfolder, ignore_errors=True, onerror=None)
        renpy.hide_screen('knz_git_dwnl_menu')
        nfo_text = 'Удаление...'
        m_nfo_text = 'Выполняется удаление указанного мода, ожидайте.'
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        renpy.pause (1, hard=True)
        try:
            persistent.del_baserpa = git_destination + baserpa
            persistent.unbaserpa = baserpa[:-4]
            renpy.pause (2, hard=True)
            nfo_text = 'Перезагрузка...'
            m_nfo_text = 'Ожидайте, пожалуйста.'
            renpy.hide_screen('knz_info_screen')
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)
            renpy.utter_restart()
        except OSError, e:
            renpy.hide_screen('knz_info_screen')
            nfo_text = 'Ошибка!'
            m_nfo_text = 'Возможно, у\xa0вас проблемы с\xa0интернет-соединением, неверно настроен доступ\nк папкам Steam или\xa0неизвестная ошибка на\xa0сервере.'
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
