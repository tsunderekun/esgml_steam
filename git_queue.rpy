init python:
    def git_qu_dwl():
        git_qu_lock = True
        global git_qu_lock
        for qu in git_queue:
            generate_index(qu)
            renpy.call_in_new_context('run_down2')
        git_qu_clr()
        git_qu_lock = False
        global git_qu_lock
        renpy.call_in_new_context('knz_dwnl_git')
    def git_qu_clr():
        git_queue = []
        global git_queue
