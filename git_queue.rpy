init python:
    git_qu_lock = False

    def git_qu_dwl():
        global git_qu_lock, git_queue
        git_qu_lock = True
        queue_copy = list(git_queue)
        for qu in queue_copy:
            generate_index(qu)
            renpy.call_in_new_context('run_down2')
        git_qu_clr()
        git_qu_lock = False
        renpy.call_in_new_context('git_qu_post_label')

    def git_qu_clr():
        global git_queue
        git_queue = []

    def git_qu_del():
        global git_qu_lock, git_del_queue
        git_qu_lock = True
        queue_copy = list(git_del_queue)
        for qu in queue_copy:
            generate_index(qu)
            renpy.call_in_new_context('deleter')
        git_del_qu_clr()
        git_qu_lock = False
        renpy.call_in_new_context('git_qu_del_post_label')

    def git_del_qu_clr():
        global git_del_queue
        git_del_queue = []

label git_qu_post_label:
    call screen git_restart_prompt("Очередь загрузки завершена!", "Все выбранные моды успешно загружены на компьютер.\nДля их появления в списке требуется перезагрузка.\nПерезагрузить игру сейчас?")
    call screen knz_git_dwnl_menu with dissolve

label git_qu_del_post_label:
    call screen git_restart_prompt("Очередь удаления завершена!", "Все выбранные моды успешно удалены с компьютера.\nДля применения изменений требуется перезагрузка игры.\nПерезагрузить сейчас?")
    call screen knz_git_dwnl_menu with dissolve
