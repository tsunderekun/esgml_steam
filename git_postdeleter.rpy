init -9999 python:

    import time
    import os as git_os
    try:
        if persistent.git_mod_deleting_id is not None:
            for id in persistent.git_mod_deleting_id:
                time.sleep(5)
                time.sleep(5)
                renpy.config.archives.remove(id)
        if persistent.git_mod_deleting is not None:
            for id in persistent.git_mod_deleting:
                if git_os.path.isfile(id):
                    git_os.remove(id)
                    time.sleep(5)
                    time.sleep(5)
        persistent.git_mod_deleting_id = []
        persistent.git_mod_deleting = []
        # renpy.utter_restart()
    except:
        pass
        # renpy.config.archives = []
