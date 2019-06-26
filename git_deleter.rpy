init -9999 python:

    # def nano_cleaner(baserpa, mfolder):
    #     import shutil, os
    #     destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
    #     shutil.rmtree(destination + mfolder, ignore_errors=True, onerror=None)
    #     try:
    #         persistent.del_baserpa = destination + baserpa
    #         persistent.unbaserpa = baserpa[:-4]
    #         persistent.evn_del = True
    #         persistent.evn_deln = "Бесконечные Кошмары"
    #     except OSError, e:
    #         persistent.evn_del = True
    #         persistent.evn_deln = "Бесконечные Кошмары"
    #
    # import os
    # try:
    #     destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
    #     file = open(destination + "nightmares.rpa")
    # except IOError as e:
    #     pass
    # else:
    #     with file:
    #         nano_cleaner ("nightmares.rpa", "nightmares/")


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
