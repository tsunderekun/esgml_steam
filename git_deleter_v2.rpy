init python:
    import os as git_os
    import shutil
    try:
        import urllib.parse as urlparse
    except ImportError:
        import urlparse

    if persistent.git_mod_deleting is None:
        persistent.git_mod_deleting = []
    if persistent.git_mod_deleting_id is None:
        persistent.git_mod_deleting_id = []

    def knz_git_mod_clean(baserpa):
        global ch_pr
        ch_pr = ''
        renpy.hide_screen('knz_git_dwnl_menu')
        nfo_text = 'Удаление...'
        m_nfo_text = 'Выполняется удаление указанного мода, ожидайте.'
        renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
        renpy.pause(0.5)

        target_file = git_os.path.join(git_destination, baserpa)
        arc_id = baserpa[:-4] if baserpa.endswith('.rpa') else baserpa

        try:
            # Отключаем архив из конфига Ren'Py, если он там есть
            if arc_id in renpy.config.archives:
                try:
                    renpy.config.archives.remove(arc_id)
                except ValueError:
                    pass

            if git_os.path.isfile(target_file):
                # Пытаемся удалить сразу
                try:
                    git_os.remove(target_file)
                except (OSError, IOError):
                    # Если файл заблокирован процессом Windows, откладываем удаление
                    if target_file not in persistent.git_mod_deleting:
                        persistent.git_mod_deleting.append(target_file)
                    if arc_id not in persistent.git_mod_deleting_id:
                        persistent.git_mod_deleting_id.append(arc_id)

            nfo_text = 'Файл удалён.'
            m_nfo_text = 'Мод успешно удалён из игры.'
            renpy.hide_screen('knz_info_screen')
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause(1.5)
        except OSError as e:
            renpy.hide_screen('knz_info_screen')
            nfo_text = 'Ошибка!'
            safe_err = str(e).replace('[', '[[').replace(']', ']]')
            m_nfo_text = 'Не удалось удалить файл:\n{}'.format(safe_err)
            renpy.show_screen('knz_info_screen', nfo_text, m_nfo_text)
            renpy.pause(2.5)

    def knz_git_rpyc_clean(mfolder):
        global ch_pr
        ch_pr = ''
        folder_path = git_os.path.join(git_destination, mfolder)
        if git_os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

    def git_del_parser(links):
        if tindex in persistent.git_mod_installed:
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
    stop music fadeout 3
    $ git_del_parser(git_links[tindex])
    if not git_qu_lock:
        call screen git_restart_prompt("Мод успешно удалён!", "Файлы мода удалены с компьютера.\nДля полного отключения требуется перезагрузка игры.\nПерезагрузить сейчас?")
        call screen knz_git_dwnl_menu with dissolve
