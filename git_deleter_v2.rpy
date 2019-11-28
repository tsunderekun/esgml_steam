
init python:

    def knz_git_mod_clean(baserpa):
        import os as git_os
        global ch_pr
        ch_pr = ''
        renpy.hide_screen('knz_git_dwnl_menu')
        nfo_text = 'Удаление...'
        m_nfo_text = 'Выполняется удаление указанного мода, ожидайте.'
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        renpy.pause (1, hard=True)
        try:
            if git_os.path.isfile(str(git_destination + baserpa)):
                try:
                        renpy.config.archives.remove(baserpa[:-4])
                except:
                    pass
                git_os.remove(str(git_destination + baserpa))

            renpy.pause (2, hard=True)
            nfo_text = 'Файл удален.'
            m_nfo_text = 'Ожидайте, пожалуйста.'
            renpy.hide_screen('knz_info_screen')
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)
        except OSError, e:
            renpy.hide_screen('knz_info_screen')
            nfo_text = 'Ошибка!'
            m_nfo_text = 'Возможно, у\xa0вас проблемы с\xa0интернет-соединением, неверно настроен доступ\nк папкам Steam или\xa0неизвестная ошибка на\xa0сервере.'
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause (5, hard=True)


    def knz_git_rpyc_clean(mfolder):
        global ch_pr
        ch_pr = ''
        shutil.rmtree(git_destination + mfolder, ignore_errors=True, onerror=None)

    def git_del_parser(links):

        import os as git_os
        import urlparse
        persistent.git_mod_installed.remove(tindex)
        for x in links:
            url = x
            a = urlparse.urlparse(url)
            b = a.path
            filename, file_extension = git_os.path.splitext(b)
            name = git_os.path.basename(b)
            knz_git_mod_clean(name)
            if file_extension == ".rpyc":
                knz_git_rpyc_clean(tindex)

label deleter:
    stop music fadeout 5
    $ git_del_parser(git_links[tindex])
    call screen knz_git_dwnl_menu with dissolve
