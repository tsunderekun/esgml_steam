init -1:
    $ git_links = {}
    $ git_info = {}
    $ git_mod_lists = []

init:
    $ git_qu_lock = False
    $ git_last_error = ""

init python:
    import os as git_os
    import shutil
    try:
        import urllib.parse as urlparse
    except ImportError:
        import urlparse

    def git_parser(links):
        global ready_ma, git_tset, git_last_error
        ready_ma = False
        git_tset = True
        git_last_error = ""

        try:
            # Убеждаемся, что целевая папка загрузки существует
            if not git_os.path.exists(git_destination):
                git_os.makedirs(git_destination)

            for x in links:
                url = x
                a = urlparse.urlparse(url)
                b = a.path
                filename, file_extension = git_os.path.splitext(b)
                name = git_os.path.basename(b)

                if file_extension == ".rpyc":
                    rpyc_dest = git_os.path.join(git_destination, tindex)
                    if not git_os.path.exists(rpyc_dest):
                        git_os.makedirs(rpyc_dest)
                    target_filepath = git_os.path.join(rpyc_dest, name)
                else:
                    target_filepath = git_os.path.join(git_destination, name)

                ok = knz_dnwl_mod(target_filepath, x)
                if not ok:
                    git_tset = False
                    break

        except Exception as e:
            git_tset = False
            git_last_error = str(e).replace('[', '[[').replace(']', ']]')
        finally:
            ready_ma = True


label run_down2:
    stop music fadeout 3
    python:
        global ready_ma, ready_m, git_tset, git_last_error
        ready_ma = False
        ready_m = False
        git_tset = False
        git_last_error = ""

        nfo_text = 'Загружаю...'
        m_nfo_text = 'Ожидайте, идёт загрузка выбранного мода.\nСходите чай заварите, например ;)'
        renpy.hide_screen('knz_git_dwnl_menu')
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)

        renpy.invoke_in_thread(git_parser, git_links[tindex])

        # Ожидаем завершения фонового потока без жесткой блокировки
        while not ready_ma:
            renpy.pause(0.2)

        renpy.hide_screen('knz_info_screen')

        if git_tset:
            if tindex not in persistent.git_mod_installed:
                persistent.git_mod_installed.append(tindex)
            nfo_text = 'Загружено!'
            m_nfo_text = 'Операция прошла успешно!'
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause(1.5)
            renpy.hide_screen('knz_info_screen')
        else:
            nfo_text = 'Ошибка!'
            safe_err = git_last_error.replace('[', '[[').replace(']', ']]') if git_last_error else ''
            err_detail = ('\nДетали: ' + safe_err) if safe_err else ''
            m_nfo_text = 'Возможно, у вас проблемы с интернет-соединением, неверно настроен доступ\nк папкам Steam или неизвестная ошибка на сервере.' + err_detail
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause(2.5)
            renpy.hide_screen('knz_info_screen')

        ready_ma = False
        ready_m = False

    if git_tset and not git_qu_lock:
        call screen git_restart_prompt("Мод успешно загружен!", "Для появления мода в списке требуется перезагрузка игры.\nПерезагрузить сейчас?")

    if not git_qu_lock:
        call screen knz_git_dwnl_menu with dissolve
