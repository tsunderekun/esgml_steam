init python:
    git_qu_lock = True
    def git_qu_dwl():
        for qu in git_queue:
            generate_index(qu)
            renpy.call_in_new_context('run_down2')
        renpy.call_in_new_context('knz_dwnl_git')
    def git_qu_clr():
        git_queue = []
        global git_queue
