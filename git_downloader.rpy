label run_down:
    stop music fadeout 5
    python:
        # t2 = Thread(target=knz_dnwl_mod_base, args=(knz_rpyc_p, knz_rpyc_f, knz_rpyc_l))
        # t3 = Thread(target=knz_dnwl_mod, args=(knz_rpa_f, knz_rpa_l))
        # t2.start()
        # t3.start()
        # t2.join()
        # t3.join()
        renpy.invoke_in_thread(knz_dnwl_mod_base, knz_rpyc_p, knz_rpyc_f, knz_rpyc_l )
        renpy.invoke_in_thread(knz_dnwl_mod, knz_rpa_f, knz_rpa_l )
        nfo_text = 'Загружаю...'
        m_nfo_text = 'Ожидайте, идёт загрузка выбранного мода.\nСходите чай заварите, например ;)'
        renpy.hide_screen('knz_git_dwnl_menu')
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        # $ renpy.pause (5, hard=True)
        while True:
            renpy.pause(1, hard=True)
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            if ready_m and ready_ma == True:
                break


        try:
            file = open(git_destination + knz_rpa_f)
        except IOError as e:
            renpy.hide_screen('knz_info_screen')
            nfo_text = 'Ошибка!'
            m_nfo_text = 'Возможно, у вас проблемы с интернет-соединением, неверно настроен доступ\nк папкам Steam или неизвестная ошибка на сервере.'
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst")
            ready_ma = False
            ready_m = False
            renpy.utter_restart()
        else:
            with file:
                renpy.hide_screen('knz_info_screen')
                nfo_text = 'Загружено!'
                m_nfo_text = 'Операция прошла успешно!'
                renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
                renpy.pause (5, hard=True)
                nfo_text = 'Перезагрузка...'
                m_nfo_text = 'Ожидайте, пожалуйста.'
                renpy.hide_screen('knz_info_screen')
                renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
                renpy.pause (5, hard=True)
                ready_ma = False
                ready_m = False
                renpy.utter_restart()
