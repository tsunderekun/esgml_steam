init -9999 python:
    import time
    import os as git_os

    # Безопасная очистка архивов и удаление модов при запуске
    try:
        if persistent.git_mod_deleting_id:
            for arc_id in list(persistent.git_mod_deleting_id):
                if arc_id in renpy.config.archives:
                    try:
                        renpy.config.archives.remove(arc_id)
                    except ValueError:
                        pass
            persistent.git_mod_deleting_id = []

        if persistent.git_mod_deleting:
            remaining_files = []
            for fpath in persistent.git_mod_deleting:
                if git_os.path.isfile(fpath):
                    deleted = False
                    # Пытаемся удалить сразу (на холодном старте файл свободен)
                    # Если заблокирован Windows, делаем пару коротких попыток с паузой 0.3с
                    for _ in range(3):
                        try:
                            git_os.remove(fpath)
                            deleted = True
                            break
                        except (OSError, IOError):
                            time.sleep(0.3)
                    if not deleted:
                        remaining_files.append(fpath)
            persistent.git_mod_deleting = remaining_files
    except Exception:
        pass
