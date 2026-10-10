init python:
    import os as _os
    import threading as _threading
    import traceback as _traceback
    import ssl as _git_ssl
    try:
        import urllib2 as _git_urllib
    except ImportError:
        import urllib.request as _git_urllib

    try:
        _git_ssl_ctx = _git_ssl._create_unverified_context()
    except Exception:
        _git_ssl_ctx = None

    _git_downloading_screens = set()

    def git_log(msg):
        pass

    def _git_bg_download_screen(url, local_path):
        try:
            req = _git_urllib.Request(str(url), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
            if _git_ssl_ctx is not None:
                try:
                    resp = _git_urllib.urlopen(req, context=_git_ssl_ctx, timeout=25)
                except TypeError:
                    resp = _git_urllib.urlopen(req, timeout=25)
            else:
                resp = _git_urllib.urlopen(req, timeout=25)
            data = resp.read()
            tdir = _os.path.dirname(local_path)
            if not _os.path.exists(tdir):
                _os.makedirs(tdir)
            with open(local_path, 'wb') as fp:
                fp.write(data)
            try:
                renpy.loader.lower_map.clear()
            except Exception:
                pass
            try:
                renpy.loader.cleardirfiles()
            except Exception:
                pass
            try:
                renpy.loader.loadable_cache.clear()
            except Exception:
                pass
            try:
                renpy.restart_interaction()
            except Exception:
                pass
            git_log("[ESGML] Downloaded screen: {} -> {}".format(url, local_path))
        except Exception as e:
            git_log("[ESGML] Failed to download screen {}: {}".format(url, str(e)))
        finally:
            _git_downloading_screens.discard(url)

    def git_get_destination():
        d = getattr(renpy.store, 'git_destination', None) or globals().get('git_destination')
        if d:
            return d
        try:
            ws = _os.path.normpath(_os.path.join(renpy.config.basedir, '..', '..', 'workshop', 'content', '331470', '1515489831')) + '/'
            if _os.path.exists(ws):
                return ws
            return _os.path.normpath(_os.path.join(renpy.config.gamedir, 'mods', 'esgml')) + '/'
        except Exception:
            return ''

    def git_resolve_screen(id_str, num, custom_scr=None):
        """
        Возвращает проверенный путь к скриншоту либо безопасную заглушку.
        Если передан URL (http/https), в фоне скачивает скриншот с репозитория в кэш!
        """
        dest = git_get_destination()
        if dest:
            dest_norm = _os.path.normpath(dest)
            if dest_norm not in renpy.config.searchpath:
                renpy.config.searchpath.append(dest_norm)

        if custom_scr:
            if custom_scr.startswith(('http://', 'https://')):
                ext = '.png'
                if '.jpg' in custom_scr.lower() or '.jpeg' in custom_scr.lower():
                    ext = '.jpg'
                rel_cache = 'git_screens/{} ({}){}'.format(id_str, num, ext)
                abs_cache = _os.path.normpath(_os.path.join(dest, rel_cache)) if dest else ''
                if abs_cache and _os.path.isfile(abs_cache):
                    try:
                        if renpy.loadable(rel_cache):
                            return rel_cache
                        renpy.loader.lower_map.clear()
                        renpy.loader.cleardirfiles()
                        renpy.loader.loadable_cache.clear()
                        if renpy.loadable(rel_cache):
                            return rel_cache
                    except Exception:
                        pass
                if abs_cache and custom_scr not in _git_downloading_screens:
                    _git_downloading_screens.add(custom_scr)
                    t = _threading.Thread(target=_git_bg_download_screen, args=(custom_scr, abs_cache))
                    t.daemon = True
                    t.start()
                return 'res/git_splash.png'
            else:
                try:
                    if renpy.loadable(custom_scr):
                        return custom_scr
                except Exception:
                    pass

        candidates = [
            'git_screens/{} ({}).png'.format(id_str, num),
            'git_screens/{} ({}).jpg'.format(id_str, num),
            'res/git_splash.png',
            'res/git_nfo.png',
        ]
        for c in candidates:
            try:
                if renpy.loadable(c):
                    return c
            except Exception:
                pass
        return 'res/git_splash.png'

    def git_easyrepo(id, links, name, desc=u'', scr1=None, scr2=None, scr3=None):
        global git_links, git_info, git_mod_lists
        try:
            if isinstance(id, unicode):
                id_str = id.encode('utf-8')
            else:
                id_str = str(id)
        except Exception:
            id_str = str(id)

        links_list = []
        for l in links:
            try:
                if isinstance(l, unicode):
                    links_list.append(l.encode('utf-8'))
                else:
                    links_list.append(str(l))
            except Exception:
                links_list.append(str(l))

        s1 = git_resolve_screen(id_str, 1, scr1)
        s2 = git_resolve_screen(id_str, 2, scr2)
        s3 = git_resolve_screen(id_str, 3, scr3)

        if id_str in git_mod_lists:
            # Уже добавлен, обновляем данные
            git_links[id_str] = links_list
            git_info[id_str] = {
                'name': name,
                'desc': desc,
                'scr1': s1,
                'scr2': s2,
                'scr3': s3
            }
            git_log("[ESGML] Updated repo: id={}, name={}".format(id_str, repr(name)))
            return

        git_links[id_str] = links_list
        git_info[id_str] = {
            'name': name,
            'desc': desc,
            'scr1': s1,
            'scr2': s2,
            'scr3': s3
        }
        git_mod_lists.append(id_str)
        git_log("[ESGML] Added repo: id={}, name={}, total={}".format(id_str, repr(name), len(git_mod_lists)))

    def git_load_custom_repos():
        """
        Автоматическое обнаружение и загрузка пользовательских репозиториев.
        Сканирует папку repos/ на наличие файлов .json, .py и .rpy.
        """
        import os as _os
        import json as _json

        dest = git_get_destination()
        repo_dirs = []

        # 1. repos рядом с файлом git_easyrepo.rpy
        try:
            curr_dir = _os.path.dirname(_os.path.abspath(__file__))
            cand_curr = _os.path.normpath(_os.path.join(curr_dir, 'repos'))
            if cand_curr not in repo_dirs:
                repo_dirs.append(cand_curr)
        except Exception:
            pass

        # 2. repos в целевой папке (workshop / esgml)
        if dest:
            d_repos = _os.path.normpath(_os.path.join(dest, 'repos'))
            if d_repos not in repo_dirs:
                repo_dirs.append(d_repos)

        # 3. repos в поисковых путях Ren'Py
        for sp in getattr(renpy.config, 'searchpath', []):
            cand = _os.path.normpath(_os.path.join(sp, 'repos'))
            if cand not in repo_dirs:
                repo_dirs.append(cand)

        # 4. Fallback пути
        try:
            fb1 = _os.path.normpath(_os.path.join(renpy.config.gamedir, 'mods', 'esgml', 'repos'))
            if fb1 not in repo_dirs:
                repo_dirs.append(fb1)
            fb2 = _os.path.normpath(_os.path.join(renpy.config.gamedir, 'repos'))
            if fb2 not in repo_dirs:
                repo_dirs.append(fb2)
        except Exception:
            pass

        for rdir in repo_dirs:
            if not _os.path.exists(rdir):
                try:
                    _os.makedirs(rdir)
                except Exception:
                    pass

            if _os.path.isdir(rdir):
                for fname in sorted(_os.listdir(rdir)):
                    fpath = _os.path.join(rdir, fname)
                    if not _os.path.isfile(fpath):
                        continue

                    fname_lower = fname.lower()

                    # Игнорируем файлы примеров, шаблоны и скрытые файлы
                    if 'example' in fname_lower or fname_lower.endswith('.example') or fname.startswith(('.', '_')):
                        continue

                    # 1. Загрузка JSON манифестов
                    if fname_lower.endswith('.json'):
                        try:
                            with open(fpath, 'rb') as jf:
                                raw_bytes = jf.read()
                            if raw_bytes.startswith(b'\xef\xbb\xbf'):
                                raw_bytes = raw_bytes[3:]
                            data = _json.loads(raw_bytes.decode('utf-8'))
                            if isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict) and 'id' in item and 'links' in item and 'name' in item:
                                        git_easyrepo(
                                            item['id'],
                                            item['links'],
                                            item['name'],
                                            item.get('desc', u''),
                                            item.get('scr1'),
                                            item.get('scr2'),
                                            item.get('scr3')
                                        )
                            elif isinstance(data, dict):
                                for mid, item in data.items():
                                    if isinstance(item, dict) and 'links' in item and 'name' in item:
                                        git_easyrepo(
                                            mid,
                                            item['links'],
                                            item['name'],
                                            item.get('desc', u''),
                                            item.get('scr1'),
                                            item.get('scr2'),
                                            item.get('scr3')
                                        )
                        except Exception as e:
                            git_log("[ESGML] Error parsing json {}: {}".format(fpath, str(e)))

                    # 2. Загрузка Python скриптов (.py)
                    elif fname_lower.endswith('.py'):
                        try:
                            with open(fpath, 'r') as pf:
                                py_code = pf.read()
                            exec(py_code, globals())
                            git_log("[ESGML] Executed python repo: {}".format(fpath))
                        except Exception as e:
                            git_log("[ESGML] Error executing py {}: {}".format(fpath, str(e)))

                    # 3. Загрузка Ren'Py скриптов (.rpy)
                    elif fname_lower.endswith('.rpy'):
                        try:
                            import textwrap as _textwrap
                            with open(fpath, 'rb') as rpf:
                                rpy_raw = rpf.read().decode('utf-8')
                            clean_lines = []
                            for line in rpy_raw.splitlines():
                                sline = line.strip()
                                if not sline or sline.startswith('#'):
                                    continue
                                if sline.startswith(('init ', 'init:')) or sline == 'python:':
                                    continue
                                clean_lines.append(line)
                            py_code = _textwrap.dedent('\n'.join(clean_lines))
                            exec(py_code, globals())
                            git_log("[ESGML] Executed rpy repo: {}".format(fpath))
                        except Exception as e:
                            git_log("[ESGML] Error executing rpy {}: {}".format(fpath, str(e)))

init 20 python:
    git_load_custom_repos()
