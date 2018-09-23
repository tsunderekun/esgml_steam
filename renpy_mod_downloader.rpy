init:

    $ style.esgml_mm = Style(style.default)
    $ style.esgml_mm.color = '#79b2c6'
    $ style.esgml_mm.hover_color = '#ffffff'
    $ style.esgml_mm.size = 55
    $ style.esgml_mm.font = "res/esgml_font.otf"
    $ style.esgml_mm.text_align = 0.5
    
    $ style.esgml_bb = Style(style.esgml_mm)
    $ style.esgml_bb.text_align = 2
    $ style.esgml_bb.size = 72
            # for name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l: 
    $ git_destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
                
    $ mods_names = [
    ("Бесконечные кошмары", "evn_git_base.rpyc", "nightmares.rpa", "nightmares/", "https://github.com/tsunderekun/es_gitmods/raw/master/evn_git_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/Nightmares.rpa", git_destination),
    
    ("Дни с Леной", "git_dayswithlena.rpyc", "git_dayswithlena_res.rpa", "dayswithlena/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena_res.rpa", git_destination),
    
    ("Совенок в тумане", "git_vkun_fog.rpyc", "VKUN_MOD.rpa", "vkun_fog/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_vkun_fog.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/VKUN_MOD.rpa", git_destination),
    
    ("Бесконечные Каникулы", "git_vacations_base.rpyc", "git_vacations.rpa", "git_vacations/", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations_base.rpyc", "https://master.dl.sourceforge.net/project/esmgl-mods/git_vacations.rpa", git_destination),
    
    ("Большая Ошибка", "git_bm_base.rpyc", "git_bm.rpa", "git_bm/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_bm/git_bm.rpa", git_destination),
    
    ("Время Лета", "git_sumtime_base.rpyc", "git_sumtime.rpa", "git_sumtime/", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime_base.rpyc", "https://gitlab.com/tsunderekun/esgml_mods/raw/master/git_sumtime/git_sumtime.rpa", git_destination),
    
    ("История Лены", "git_lena_story_base.rpyc", "git_lena_story.rpa", "git_lena_story/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_story.rpa", git_destination),
    
    ("Лена. Альтернативная концовка", "git_lena_alternate_base.rpyc", "git_lena_alternate.rpa", "git_lena_alternate/", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate_base.rpyc", "https://github.com/tsunderekun/es_gitmods/raw/master/git_lena_alternate.rpa", git_destination),
    ]
    
    $ mods["knz_dwnl_git"]=u"Everlasting Summer GitHub Mods Loader"

    image git_es_del = "res/git_es_del.png"
    image git_es_fail = "res/git_es_fail.png"
    image git_es_succ = "res/git_es_succ.png"
    image git_es_rst = "res/git_es_rst.png"
    image git_es_dwnl = "res/git_es_dwnl.png"
    
label knz_dwnl_git:
    call screen knz_git_dwnl_menu
    
screen knz_git_dwnl_menu:
    $ import os.path
    modal False
    window:
        background "res/git_es.png"
    side "c r":
        area (0.05, 0.225, 0.9, 0.675)
        viewport id "git_mods_menu":
            draggable True
            mousewheel True
            scrollbars None
            
            has grid 2 len(mods_names)
            for name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, destination in mods_names:
                textbutton name xalign 0 xmaximum 0.9: #action:
                    style "esgml_mm"
                    text_style "esgml_mm"
                hbox xpos 0.630 spacing 10:
                    
                    if os.path.isfile(destination + rpa_f):
                        add 'res/git_dwl_inactive.png' xalign 0.90
                    else:
                        imagebutton auto 'res/git_dwl_%s.png' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'run_down')] xalign 0.90

                        
                    if os.path.isfile(destination + rpa_f):
                        imagebutton auto 'res/git_del_%s.png' action [Function(knz_get_data, rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l), Function(renpy.call_in_new_context, 'deleter')] xalign 0.91
                    else:
                        add 'res/git_del_inactive.png' xalign 0.91
                        
    hbox yalign 0.975 xalign 0.5 spacing 144:
        textbutton 'NLT Modpack' action [OpenURL('steam://url/CommunityFilePage/847728687')]:
                    style "esgml_bb"
                    text_style "esgml_bb"
                    
        textbutton 'Главное меню' action [Return()]:
                    style "esgml_bb"
                    text_style "esgml_bb"
                        
        textbutton 'Выход' action [Quit (confirm=False)]:
                    style "esgml_bb"
                    text_style "esgml_bb"
                    
                        
                  
init 999 python:
    config.archives.append('res_git') 
    

    
init python:
    import time
    config.image_cache_size_mb = 1536
    def knz_dnwl_mod_base(mfolder, baserpyc, rpyclink):

        import urllib2, os, shutil
        
        destination = git_destination + mfolder
        
        os.mkdir(destination)
        
        filedata = urllib2.urlopen(rpyclink)  
        datatowrite = filedata.read()
        
        with open(destination + baserpyc, 'wb') as f:  
            f.write(datatowrite)

    def knz_dnwl_mod(baserpa, rpalink):

        import os, wget

        s=rpalink
        filename = wget.download(s)
        os.rename(filename, git_destination + baserpa)
        
        try:
            file = open(git_destination + baserpa)
        except IOError as e:
            renpy.hide_screen('knz_git_dwnl_menu')
            renpy.show("git_es_fail")
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst")
            renpy.utter_restart() 
        else:
            with file:
                renpy.hide_screen('knz_git_dwnl_menu')
                renpy.show("git_es_succ", layer='master')
                renpy.pause (5, hard=True)
                renpy.show("git_es_rst", layer='master')
                renpy.utter_restart() 
                
                
    def knz_git_mod_clean(baserpa, mfolder):
    
    
        import os, shutil
        shutil.rmtree(git_destination + mfolder, ignore_errors=True, onerror=None) 
        
        try:
            os.remove(git_destination + baserpa)
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst", layer='master')
            renpy.utter_restart() 
        except OSError, e:
            renpy.show("git_es_fail")
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst", layer='master')
            renpy.utter_restart()
            
            
    def knz_get_data(rpyc_p, rpyc_f, rpyc_l, rpa_f, rpa_l):
        global knz_rpyc_p
        global knz_rpyc_f
        global knz_rpyc_l
        global knz_rpa_f
        global knz_rpa_l
        knz_rpyc_f = rpyc_f
        knz_rpyc_l = rpyc_l
        knz_rpyc_p = rpyc_p
        knz_rpa_f = rpa_f
        knz_rpa_l = rpa_l
            

   
    ###MOD CHECKER###
    
init -10 python:
    def rpa_check_append(rpaf, rpan):
        import os
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        try:
            file = open(destination + rpaf)
        except IOError as e:
            print(u'Sorry, senpai, file not downloaded(((')
        else:
            with file:
                config.archives.append(rpan) 

    def rpa_check_varinst(git_mod_id, git_mod_name, rpaf):
        global mods
        import os
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        try:
            file = open(destination + rpaf)
        except IOError as e:
            print(u'Sorry, senpai, file not downloaded(((')
        else:
            with file:
                mods[git_mod_id]=git_mod_name
