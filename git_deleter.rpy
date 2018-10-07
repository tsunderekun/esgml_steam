init -54 python:
    import os, time
    try: 
        if persistent.del_baserpa is not None:
            os.remove(persistent.del_baserpa)
            time.sleep(5)
            persistent.del_baserpa = None
            time.sleep(5)
            renpy.utter_restart()
    except:
        persistent.del_baserpa = None


label deleter:
    stop music fadeout 5
    $ renpy.show("git_es_del", layer='master')
    $ renpy.with_statement(fade, always=False)
    $ renpy.pause (5, hard=True)
    $ knz_git_mod_clean(knz_rpa_f, knz_rpyc_p)