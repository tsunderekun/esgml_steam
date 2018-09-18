init:

    $ mods["knz_dwnl_git"]=u"Everlasting Summer GitHub Mods Loader"
    image git_es_dwnl = "res/git_es_dwnl.png"
    image git_es_del = "res/git_es_del.png"
    image git_es_fail = "res/git_es_fail.png"
    image git_es_succ = "res/git_es_succ.png"
    image git_es_rst = "res/git_es_rst.png"
    image git_es_dwnl = "res/git_es_dwnl.png"
    
    
init 999 python:
    config.archives.append('res_git') 
    

init python:

    def knz_dnwl_mod_base(mfolder, baserpyc, rpyclink):

        import urllib2, os, shutil
        
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/' + mfolder

        path = renpy.config.basedir + '/../../workshop/content/331470/1515489831/' + mfolder
        
        os.mkdir(path)
        

        filedata = urllib2.urlopen(rpyclink)  
        datatowrite = filedata.read()
        
        with open(destination + baserpyc, 'wb') as f:  
            f.write(datatowrite)

    def knz_dnwl_mod(baserpa, rpalink):

        import urllib2, os
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        filedata = urllib2.urlopen(rpalink)  
        datatowrite = filedata.read()

        with open(destination + baserpa, 'wb') as f:  
            f.write(datatowrite)
        
        
        try:
            file = open(destination + baserpa)
        except IOError as e:
            renpy.show("git_es_fail")
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst")
            renpy.utter_restart() 
        else:
            with file:
                renpy.show("git_es_succ", layer='master')
                renpy.pause (5, hard=True)
                renpy.show("git_es_rst", layer='master')
                renpy.utter_restart() 
                
                
    def knz_git_mod_clean(baserpa, mfolder):
        import os, shutil
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        shutil.rmtree(renpy.config.basedir + '/../../workshop/content/331470/1515489831/' + mfolder, ignore_errors=True, onerror=None) 
        
        try:
            os.remove(destination + baserpa)
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst", layer='master')
            renpy.utter_restart() 
        except OSError, e:
            renpy.show("git_es_fail")
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst", layer='master')
            renpy.utter_restart() 
            

label knz_dwnl_git:
    call screen knz_git_dwnl_menu
    
                
                
screen knz_git_dwnl_menu:
    modal False
    imagemap: 
            ground "res/git_es_idle.png"   
            hover "res/git_es_hover.png" 
            alpha True
            
            hotspot (692, 400, 44, 42) action [Hide ('knz_git_dwnl_menu'), Jump("run_down")]
            hotspot (744, 401, 42, 42) action [Hide ('knz_git_dwnl_menu'), Jump("deleter")]
            hotspot (693, 339, 43, 41) action [Hide ('knz_git_dwnl_menu'), Jump("dwl_run_down")]
            hotspot (742, 339, 44, 41) action [Hide ('knz_git_dwnl_menu'), Jump("dwl_deleter")]
            hotspot (1776, 935, 115, 114) action [Hide ('knz_git_dwnl_menu'), Jump("restart_git")]
            hotspot (1636, 937, 114, 113) action Quit (confirm=False)
            
    ### EVERLASTING NIGHTMARES ###
            
label run_down:
    $ renpy.show("git_es_dwnl", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_dnwl_mod_base('nightmares/', 'evn_git_base.rpyc', 'https://github.com/tsunderekun/es_gitmods/raw/master/evn_git_base.rpyc')
    $ knz_dnwl_mod('nightmares.rpa','https://github.com/tsunderekun/es_gitmods/raw/master/Nightmares.rpa')
    
label deleter:
    $ renpy.show("git_es_del", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_git_mod_clean('nightmares.rpa', 'nightmares/')
    
label restart_git:
    $ renpy.show("git_es_rst", layer='master')
    $ renpy.pause (5, hard=True)
    $ renpy.utter_restart() 
    
    ### DAYS WITH LENA ###
    
label dwl_run_down:
    $ renpy.show("git_es_dwnl", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_dnwl_mod_base('dayswithlena/','git_dayswithlena.rpyc','https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena.rpyc')
    $ knz_dnwl_mod('git_dayswithlena_res.rpa', 'https://github.com/tsunderekun/es_gitmods/raw/master/git_dayswithlena_res.rpa')
    
label dwl_deleter:
    $ renpy.show("git_es_del", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_git_mod_clean('git_dayswithlena_res.rpa', 'dayswithlena/')
    
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
