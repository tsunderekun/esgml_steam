init -100 python:
    import os, time
    try:
        if persistent.del_baserpa is not None:
            renpy.config.archives.remove(persistent.unbaserpa)
            os.remove(persistent.del_baserpa)
            time.sleep(5)
            persistent.del_baserpa = None
            persistent.unbaserpa = None
            time.sleep(5)
            renpy.utter_restart()
    except:
        pass


label deleter:
    stop music fadeout 5
    $ knz_git_mod_clean(knz_rpa_f, knz_rpyc_p)
