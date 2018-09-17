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
    def knz_dnwl_mod_base():

        import urllib2, os, shutil
        
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/nightmares/'

        path = renpy.config.basedir + '/../../workshop/content/331470/1515489831/' + 'nightmares/'
        
        os.mkdir(path)
        

        filedata = urllib2.urlopen('https://github.com/tsunderekun/es_gitmods/raw/master/evn_git_base.rpyc')  
        datatowrite = filedata.read()
        
        with open(destination + 'evn_git_base.rpyc', 'wb') as f:  
            f.write(datatowrite)

    def knz_dnwl_mod():

        import urllib2, os
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        filedata = urllib2.urlopen('https://github.com/tsunderekun/es_gitmods/raw/master/Nightmares.rpa')  
        datatowrite = filedata.read()

        with open(destination + 'Nightmares.rpa', 'wb') as f:  
            f.write(datatowrite)
        
        
        try:
            file = open(destination + 'Nightmares.rpa')
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
                
                
    def knz_git_mod_clean():
        import os, shutil
        destination = renpy.config.basedir + '/../../workshop/content/331470/1515489831/'
        shutil.rmtree(renpy.config.basedir + '/../../workshop/content/331470/1515489831/' + 'nightmares/', ignore_errors=True, onerror=None) 
        
        try:
            os.remove(destination + 'Nightmares.rpa')
            renpy.pause (5, hard=True)
            renpy.show("git_es_rst", layer='master')
            renpy.utter_restart() 
        except OSError, e:  ## if failed, report it back to the user ##
            renpy.show("git_es_fail")
            os.remove(destination + 'Nightmares.rpa')
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
            
            hotspot (707, 393, 380, 101) action [Hide ('knz_git_dwnl_menu'), Jump("run_down")]
            hotspot (1110, 392, 385, 103) action [Hide ('knz_git_dwnl_menu'), Jump("deleter")]
            hotspot (1522, 959, 381, 105) action [Hide ('knz_git_dwnl_menu'), Jump("restart_git")]
label run_down:
    $ renpy.show("git_es_dwnl", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_dnwl_mod_base()
    $ knz_dnwl_mod()
    
label deleter:
    $ renpy.show("git_es_del", layer='master')
    $ renpy.pause (5, hard=True)
    $ knz_git_mod_clean()
    
label restart_git:
    $ renpy.show("git_es_rst", layer='master')
    $ renpy.pause (5, hard=True)
    $ renpy.utter_restart() 