init 2:
    python:
            def git_easyrepo(id, links, name, desc):
                if str(id) in git_mod_lists:
                    raise Exception('Такой индекс существует, добавление мода в ESGML не является возможным. Ваш индекс: {}'.format(id))
                global git_links
                global git_info
                global git_mod_lists
                git_links[id] = links
                git_info[id] = {
                'name': name,
                'desc': desc,
                'scr1': 'git_screens/{} (1).png'.format(id),
                'scr2': 'git_screens/{} (2).png'.format(id),
                'scr3': 'git_screens/{} (3).png'.format(id)
                }
                git_mod_lists.append(id)
                pass
