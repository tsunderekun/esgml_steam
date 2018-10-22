label run_down:
    stop music fadeout 5
    $ renpy.show("git_es_dwnl", layer='master')
    $ renpy.with_statement(fade, always=False)
    $ renpy.pause (5, hard=True)
    python:
        t2 = Thread(target=knz_dnwl_mod_base, args=(knz_rpyc_p, knz_rpyc_f, knz_rpyc_l))
        t3 = Thread(target=knz_dnwl_mod, args=(knz_rpa_f, knz_rpa_l))
        t2.start()
        t3.start()
        t2.join()
        t3.join()
        try:
            file = open(git_destination + knz_rpa_f)
            # file_s = git_destination + knz_rpa_f
        except IOError as e:
            renpy.hide_screen('knz_git_dwnl_menu')
            renpy.show("git_es_fail")
            renpy.with_statement(fade, always=False)
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst")
            renpy.with_statement(fade, always=False)
            renpy.utter_restart() 
        else:
            with file:
                renpy.hide_screen('knz_git_dwnl_menu')
                renpy.show("git_es_succ", layer='master')
                # files = os.path.getsize(file_s)
                # un (str(files))
                renpy.with_statement(fade, always=False)
                renpy.pause (5, hard=True)
                renpy.show("git_es_rst", layer='master')
                renpy.with_statement(fade, always=False)
                renpy.utter_restart()