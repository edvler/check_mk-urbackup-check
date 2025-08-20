#!/usr/bin/env python3

# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk-urbackup-check
# License: GPLv2


from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    Metric,
    render,
    check_levels,
)
import time
from datetime import datetime

# Example agent output
# Format:
# root@urbackup-server:/usr/lib/check_mk_agent/plugins# ./urbackup_check
# <<<urbackup_check>>>
# FMT-PC;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# FMT-PC;;;;;imagebackup;;;;;C:;;;;;2023-04-10_14:03+0200;;;;;False
# FMT-PC;;;;;imagebackup;;;;;SYSVOL;;;;;2023-04-10_14:02+0200;;;;;False
# NB04;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# NB04;;;;;imagebackup;;;;;C:;;;;;2023-08-06_19:51+0200;;;;;True
# NB04;;;;;imagebackup;;;;;ESP;;;;;2023-08-06_19:51+0200;;;;;True
# NB04;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_19:50+0200;;;;;True
# Netphone;;;;;filebackup;;;;;filebackup;;;;;2023-08-06_08:26+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;C:;;;;;2023-08-07_02:00+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;ESP;;;;;2023-08-07_02:00+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-07_01:24+0200;;;;;True
# PC01;;;;;filebackup;;;;;filebackup;;;;;2023-08-06_23:07+0200;;;;;True
# PC01;;;;;imagebackup;;;;;C:;;;;;2023-08-06_20:56+0200;;;;;True
# PC01;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_20:56+0200;;;;;True
# PC02;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# PC02;;;;;imagebackup;;;;;C:;;;;;2023-08-06_19:06+0200;;;;;True
# PC02;;;;;imagebackup;;;;;ESP;;;;;2023-08-06_19:06+0200;;;;;True
# PC02;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_19:06+0200;;;;;True
# PC03;;;;;filebackup;;;;;filebackup;;;;;2023-08-07_00:17+0200;;;;;True
# PC03;;;;;imagebackup;;;;;C:;;;;;2023-08-06_16:39+0200;;;;;True
# PC03;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_16:39+0200;;;;;True
# PC04;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# PC04;;;;;imagebackup;;;;;C:;;;;;2023-08-06_18:03+0200;;;;;True
# PC04;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_18:03+0200;;;;;True
# PC05;;;;;filebackup;;;;;filebackup;;;;;2023-08-07_00:35+0200;;;;;True
# PC05;;;;;imagebackup;;;;;C:;;;;;2023-08-06_15:43+0200;;;;;True
# PC05;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_15:43+0200;;;;;True
# Roentgen-PC;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# Roentgen-PC;;;;;imagebackup;;;;;C:;;;;;2023-08-06_14:06+0200;;;;;True
# Roentgen-PC;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_14:06+0200;;;;;True
# pc-xx;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# pc-xx;;;;;imagebackup;;;;;C:;;;;;2023-08-06_09:17+0200;;;;;True
# pc-xx;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_09:16+0200;;;;;True
# <<<<FMT-PC>>>>
# <<<urbackup_check>>>
# FMT-PC;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# FMT-PC;;;;;imagebackup;;;;;C:;;;;;2023-04-10_14:03+0200;;;;;False
# FMT-PC;;;;;imagebackup;;;;;SYSVOL;;;;;2023-04-10_14:02+0200;;;;;False
# <<<<NB04>>>>
# <<<urbackup_check>>>
# NB04;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# NB04;;;;;imagebackup;;;;;C:;;;;;2023-08-06_19:51+0200;;;;;True
# NB04;;;;;imagebackup;;;;;ESP;;;;;2023-08-06_19:51+0200;;;;;True
# NB04;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_19:50+0200;;;;;True
# <<<<Netphone>>>>
# <<<urbackup_check>>>
# Netphone;;;;;filebackup;;;;;filebackup;;;;;2023-08-06_08:26+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;C:;;;;;2023-08-07_02:00+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;ESP;;;;;2023-08-07_02:00+0200;;;;;True
# Netphone;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-07_01:24+0200;;;;;True
# <<<<PC01>>>>
# <<<urbackup_check>>>
# PC01;;;;;filebackup;;;;;filebackup;;;;;2023-08-06_23:07+0200;;;;;True
# PC01;;;;;imagebackup;;;;;C:;;;;;2023-08-06_20:56+0200;;;;;True
# PC01;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_20:56+0200;;;;;True
# <<<<PC02>>>>
# <<<urbackup_check>>>
# PC02;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# PC02;;;;;imagebackup;;;;;C:;;;;;2023-08-06_19:06+0200;;;;;True
# PC02;;;;;imagebackup;;;;;ESP;;;;;2023-08-06_19:06+0200;;;;;True
# PC02;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_19:06+0200;;;;;True
# <<<<PC03>>>>
# <<<urbackup_check>>>
# PC03;;;;;filebackup;;;;;filebackup;;;;;2023-08-07_00:17+0200;;;;;True
# PC03;;;;;imagebackup;;;;;C:;;;;;2023-08-06_16:39+0200;;;;;True
# PC03;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_16:39+0200;;;;;True
# <<<<PC04>>>>
# <<<urbackup_check>>>
# PC04;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# PC04;;;;;imagebackup;;;;;C:;;;;;2023-08-06_18:03+0200;;;;;True
# PC04;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_18:03+0200;;;;;True
# <<<<PC05>>>>
# <<<urbackup_check>>>
# PC05;;;;;filebackup;;;;;filebackup;;;;;2023-08-07_00:35+0200;;;;;True
# PC05;;;;;imagebackup;;;;;C:;;;;;2023-08-06_15:43+0200;;;;;True
# PC05;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_15:43+0200;;;;;True
# <<<<Roentgen-PC>>>>
# <<<urbackup_check>>>
# Roentgen-PC;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# Roentgen-PC;;;;;imagebackup;;;;;C:;;;;;2023-08-06_14:06+0200;;;;;True
# Roentgen-PC;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_14:06+0200;;;;;True
# <<<<pc-xx>>>>
# <<<urbackup_check>>>
# pc-xx;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False
# pc-xx;;;;;imagebackup;;;;;C:;;;;;2023-08-06_09:17+0200;;;;;True
# pc-xx;;;;;imagebackup;;;;;SYSVOL;;;;;2023-08-06_09:16+0200;;;;;True
#
# If the date field contains "-" no backup was done for this machine.
# Fileok and imageok represents the status of the UrBackup Status page.
# --> No filebackup FMT-PC;;;;;filebackup;;;;;filebackup;;;;;-;;;;;False

CLIENT_NAME=0
BACKUP_TYPE=1
LETTER=2
TIMESTAMP=3
URBACKUPSTATUS=4

def getDateFromString(datetime_string):
    try:
        d = datetime.strptime(datetime_string,"%Y-%m-%d_%H:%M%z")
        return d
    except ValueError:
        return None

def params_parser(params):
    params_new = {}

    for p in params:
        if params[p] is not None and isinstance(params[p], tuple):
            if params[p][0] in ("fixed", "no_levels", "predictive"): #e.g ('fixed', (1, 1)) - New Check_MK 2.4 format
                params_new[p] = params[p]            
            elif isinstance(params[p][0], (int, float)) and isinstance(params[p][1], (int, float)):
                params_new[p] = ('fixed', (params[p][0], params[p][1]))
            else:
                params_new[p] = params[p]
        else:
            if isinstance(params[p], str) and p == 'check_backup':
                params_new[p] = False if params[p] == 'ignore' else True
            elif isinstance(params[p], str) and p == 'modi':
                params_new[p] = (params[p], None)
            else:   
                params_new[p] = params[p]

    
    return params_new

def check_name_urbackup(check_line):
    arr_backups = check_line.split(';;;;;')
    machine_name = arr_backups[CLIENT_NAME]
    type_bkp = arr_backups[BACKUP_TYPE]    

    if type_bkp == "filebackup":
        return machine_name + ' filebackup'

    if type_bkp == "imagebackup":
        return machine_name + ' imagebackup ' + arr_backups[LETTER]

# the inventory function (dummy)
def discovery_urbackup_check(section):
    # loop over all output lines of the agent
    for line in section:
        line_as_string=' '.join(map(str,line))
        yield Service(item=check_name_urbackup(line_as_string))

# the check function (dummy)
def check_urbackup(item, params, section):
    params_cmk_24 = params_parser(params)

    #return 0 if check of backups should not be done
    if params_cmk_24['check_backup'] == False:
        yield (Result(state=State.OK, summary='check disabled by rule'))
        return

    for line in section:
        line_as_string=' '.join(map(str,line))
        machine_infos = line_as_string.split(";;;;;")

        if check_name_urbackup(line_as_string) == item:
            #if urbackup status is used ...
            if params_cmk_24['modi'][0] == 'use_urbackup_status':
                if machine_infos[URBACKUPSTATUS].lower() == 'true':
                    yield (Result(state=State.OK, summary='status reported by UrBackup is: True'))
                if machine_infos[URBACKUPSTATUS].lower() == 'false':
                    yield (Result(state=State.CRIT, summary='status reported by UrBackup is: False'))

            #if backup age is used
            if params_cmk_24['modi'][0] == 'use_backup_age':
                stamp = getDateFromString(machine_infos[TIMESTAMP])

                if stamp is None:
                    yield (Result(state=State.UNKNOWN, summary='No backup configured, no backup done yet or no last backup date reported by urbackup'))

                if stamp is not None:
                    #old = time.time() - time.mktime(stamp)
                    n = time.strftime('%Y-%m-%d_%H:%M%z',time.localtime())
                    cdt = datetime.strptime(n, '%Y-%m-%d_%H:%M%z')
                    olddt = cdt - stamp
                    old = olddt.total_seconds()
            
                    levels = params_cmk_24['backup_age']
                    if levels == None or levels ==("no_levels", None):
                        yield (Result(state=State.OK, summary="No check levels defined!"))
                        return
                    
                    if 'backup_age' not in params_cmk_24:
                        yield (Result(state=State.UNKNOWN, summary="No backup_age defined, but - Use levels defined in this check - are choosen in rules!"))
                        return

                    warn, crit = params_cmk_24['backup_age'][1]
                    infotext = 'last ' + machine_infos[BACKUP_TYPE] + ': ' + render.datetime(stamp.timestamp()) + ' (Age: ' + render.timespan(old) + ' warn/crit at ' + render.timespan(warn) + '/' + render.timespan(crit) + ')'
                    
                    yield Metric('age', int(old), levels=(warn,crit), boundaries=(0, None))

                    if old >= crit:
                        yield (Result(state=State.CRIT, summary=infotext))
                        return
                    if old >= warn:
                        yield (Result(state=State.WARN, summary=infotext))
                        return

                    yield (Result(state=State.OK, summary=infotext))


check_plugin_urbackup_check = CheckPlugin(
    name = "urbackup_check",
    service_name = "Urbackup %s",
    discovery_function = discovery_urbackup_check,
    check_function = check_urbackup,
    check_default_parameters = {
                                'modi': ('use_backup_age',None),
                                'check_backup': True,
                                'backup_age': (1.5 * 86400.0, 2 * 86400.0),
                                },
    check_ruleset_name = "urbackup"
)