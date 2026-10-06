# ==============================================================================
# ESGML (Everlasting Summer Git Mods Loader) — БАЗОВЫЙ РЕПОЗИТОРИЙ МОДОВ
# ==============================================================================
# Этот файл является встроенным каталогом модов по умолчанию и примером оформления.
#
# ЧТОБЫ ДОБАВИТЬ СОБСТВЕННЫЕ РЕПОЗИТОРИИ:
# Не редактируйте этот файл напрямую! Вместо этого:
# 1. Положите ваш файл .rpy, .py или .json в папку repos/
#    (например, repos/my_mods.rpy или repos/my_mods.json).
# 2. Либо создайте отдельный файл git_repo_<name>.rpy рядом с этим файлом.
# 3. ESGML автоматически подключит ваши моды при запуске игры.
# ==============================================================================

init 5 python:
    git_easyrepo(
        'la',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate_base.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate.rpa"),
        'Лена. Альтернативная концовка',
        ''
    )

    git_easyrepo(
        'ls',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story_base.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story.rpa"),
        'История Лены',
        ''
    )

    git_easyrepo(
        'dwl',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena_res.rpa"),
        'Дни с Леной',
        u'\nНебольшой мод по\xa0одноимённому фанфику.\n\nСобытия мода начинаются с\xa0седьмого дня пребывания в\xa0лагере, когда Семён покидает Лену, думая\xa0лишь\xa0о\xa0том, как\xa0поскорее попасть домой. Но\xa0вернувшись в\xa0домик Лены, он\xa0видит, что\xa0она умирает...\n'
    )

    git_easyrepo(
        'bm',
        ("https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm_base.rpyc",
         "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm.rpa"),
        'Большая ошибка',
        u'\nЭто история обычного московского студента Михаила, живущего обычной скучной жизнью в\xa0небольшой квартире. Михаил\xa0часто прогуливает занятия и\xa0живёт, в\xa0общем-то, сам\xa0для\xa0себя. Попав в\xa0неизвестный для\xa0себя лагерь, он\xa0замечает странные вещи, которые всерьёз его\xa0настораживают и даже пугают.\n\nЧем\xa0закончится его летнее приключение? Сможет\xa0ли неделя в\xa0«Совёнке» изменить нашего героя к\xa0лучшему? Он\xa0и\xa0сам этого не\xa0знает.\n'
    )

    git_easyrepo(
        'vkun',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/git_vkun_fog.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/VKUN_MOD.rpa"),
        'Совёнок в тумане',
        u'\nЗаблудившись в\xa0тумане, молодой солдат находит мифический, кишащий монстрами лагерь...\n'
    )

    git_easyrepo(
        'st',
        ("https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime_base.rpyc",
         "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime.rpa"),
        'Время лета',
        u'\nОтличная от\xa0оригинальной история парня по\xa0имени Семён, который\xa0оказался не\xa0в\xa0самой обычной для\xa0него ситуации —\xa0в\xa0альтернативной реальности.\n\nМод\xa0повествует о\xa0стандартной семидневной смене в\xa0лагере «Совёнок». Здесь\xa0вы\xa0найдёте множество отсылок, с\xa0которыми можете столкнуться в\xa0реальной жизни (и\xa0это не\xa0просто\xa0так: весь сценарий и\xa0исход событий будет зависеть от\xa0вас), узнаете истинные помыслы героев игры, покинете цикл с\xa0той девушкой, которую\xa0выберите сами, а\xa0также узнаете, почему Семён потерял память.\n'
    )

    git_easyrepo(
        'emk1',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/emk1_base.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/emk1.rpa"),
        'Эпилог МК1',
        ''
    )

    git_easyrepo(
        'v17',
        ("https://github.com/tsunderekun/es_gitmods/raw/master/base_v17.rpyc",
         "https://github.com/tsunderekun/es_gitmods/raw/master/git_v17.rpa"),
        'Где мои семнадцать лет?',
        ''
    )

    git_easyrepo(
        'rs',
        ("https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_base.rpyc",
         "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_rs/rs_common.rpa"),
        'Чёрная страница из дневника Сэм',
        u'\nМод расскажет об\xa0альтернативном развитии событий уже известного всем романа. Однако\xa0главного героя здесь всё-таки ждёт пара неприятностей. Но\xa0пугаться нечего, потому\xa0что почти у\xa0каждой истории есть хороший конец, и\xa0эта —\xa0не\xa0исключение. \n\n История берёт своё начало сразу после окончания смены в\xa0лагере, когда\xa0Семён прощается с\xa0Сэм. Это\xa0триллер с\xa0отголосками романтики и\xa0драмы, ориентированный на\xa0читателя вдумчивого и\xa0открытого к\xa0полёту фантазии.'
    )

    git_easyrepo(
        'hs',
        ("https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_base.rpyc",
         "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_hs/hs_common.rpa"),
        'Ужасное лето',
        u'\nСюжет данного мода разворачивается во\xa0время второго визита главного героя в\xa0«Совёнок». Однако на\xa0этот\xa0раз все пионеры лагеря помнят события прошлого лета. Но,\xa0в\xa0отличие от\xa0остальных, Семён\xa0сделал этот\xa0выбор сознательно. Его\xa0ждут старые знакомые, увлекательная компания, замечательное лето... но\xa0не\xa0всё пройдёт гладко. Для\xa0героев мода эта\xa0смена окажется не\xa0совсем обычной, и\xa0им придётся бороться за\xa0то, чтобы увидеть её\xa0конец.\n'
    )

    git_easyrepo(
        'idnh',
        ("https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_idnh/idnh_base.rpyc",
         "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_idnh/idnh_common.rpa"),
        'Re: I Do Not Have',
        u'\nГлавный герой мода —\xa0Иван Смирнов, обычный\xa0ученик колледжа на\xa0четвёртом году обучения, которому\xa0приспичило не\xa0спать четверо суток подряд и\xa0играть в\xa0новеллу «Бесконечное лето». Казалось\xa0бы, с\xa0кем не\xa0бывает? Но\xa0однажды он засыпает у\xa0себя дома и\xa0видит сон, в\xa0котором двое мужчин обсуждают захоронение заживо какой-то девочки, что\xa0прокляла всю\xa0деревню. Проснувшись, Ваня идёт на\xa0кухню промыть затёкший кровью нос и\xa0неожиданно падает в\xa0обморок... \n\nПридя\xa0в\xa0себя, он\xa0оказывается в\xa0заброшенном пионерлагере «Совёнок». Ваня забывает всю\xa0свою\xa0прошлую жизнь. Проведя в\xa0этом казалось\xa0бы райском и\xa0безлюдном месте какое-то время, он\xa0однажды натыкается на\xa0могилы умерших пионеров, в\xa0том\xa0числе и\xa0свою.\n\nЧто\xa0же случилось с\xa0ними? И\xa0что он должен сделать, чтобы изменить череду событий в\xa0лучшую сторону?\n'
    )
