label run_down:
    stop music fadeout 5
    $ renpy.show("git_es_dwnl", layer='master')
    $ renpy.with_statement(fade, always=False)
    $ renpy.pause (5, hard=True)
    if  id == 'twat':
        $ knz_dnwl_mod_base(knz_rpyc_p, knz_rpyc_f, knz_rpyc_l)
        $ knz_dnwl_another('tw_credits.txt','')
        $ knz_dnwl_mod(knz_rpa_f, knz_rpa_l)
    else:
        $ knz_dnwl_mod_base(knz_rpyc_p, knz_rpyc_f, knz_rpyc_l)
        $ knz_dnwl_mod(knz_rpa_f, knz_rpa_l)