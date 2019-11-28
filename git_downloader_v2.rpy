init -1:
    $ git_links = {}
    $ git_info = {}
    $ git_mod_lists = []

init:
    $ git_qu_lock = False

init python:
    def git_parser(links):

        import os as git_os
        import urlparse, shutil
        for x in links:
            url = x
            a = urlparse.urlparse(url)
            b = a.path
            filename, file_extension = git_os.path.splitext(b)
            name = git_os.path.basename(b)
            if file_extension == ".rpyc":
                rpyc_dest = git_destination + tindex
                git_os.mkdir(rpyc_dest)
                knz_dnwl_mod(name, x)
                shutil.move(git_destination + name, git_destination + tindex + '/' + name)
            else:
                knz_dnwl_mod(name, x)
        global ready_ma
        ready_ma = True
        persistent.git_mod_installed.append(tindex)


label run_down2:
    stop music fadeout 5
    python:
        nfo_text = 'Загружаю...'
        m_nfo_text = 'Ожидайте, идёт загрузка выбранного мода.\nСходите чай заварите, например ;)'
        renpy.hide_screen('knz_git_dwnl_menu')
        renpy.invoke_in_thread(git_parser, git_links[tindex])
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        # $ renpy.pause (5, hard=True)
        while True:
            renpy.pause(1, hard=True)
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            if ready_ma == True:
                break
        renpy.hide_screen('knz_info_screen')
        if git_tset == True:
            nfo_text = 'Загружено!'
            m_nfo_text = 'Операция прошла успешно!'
        else:
            nfo_text = 'Ошибка!'
            m_nfo_text = 'Возможно, у\xa0вас проблемы с\xa0интернет-соединением, неверно настроен доступ\nк папкам Steam или\xa0неизвестная ошибка на\xa0сервере.'
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        renpy.pause (5, hard=True)
        ready_ma = False
        ready_m = False
    if git_qu_lock == False:
        call screen knz_git_dwnl_menu with dissolve
