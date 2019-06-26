# -*- coding: utf-8 -*-
repofiles = []

def modsparser(filename, listin, git_destination):
    import codecs
    try:
        with codecs.open(filename, encoding = 'UTF-8') as file_object:
            for line in file_object:
                line = line.rstrip('\n')
                mid, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l = map(str, line.split(" | "))
                name = name.encode('utf8')
                listin.append((mid, name, rpyc_f, rpa_f, rpyc_p, rpyc_l, rpa_l, git_destination))
    except IOError as er:
        print(u'Can\'t open the "{0}" file'.format(er.filename))
    print listin

def txtlist(git_destination, listin):
    import glob, os
    for file in glob.glob(git_destination + "*.mlrepo"):
        repofiles.append(file)
    for item in repofiles:
        modsparser(item, listin, git_destination)
