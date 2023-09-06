#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Matthias Maderer
# E-Mail: edvler@edvler-blog.de
# URL: https://github.com/edvler/check_mk-urbackup-check
# License: GPLv2


from .agent_based_api.v1 import *
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


# default parameters
urbackup_check_default_levels = {'check_backup': 'check', 'backup_age': (93600, 108000), 'modi': 'use_backup_age', 'use_performance_data': 'enable'}

CLIENT_NAME=0
BACKUP_TYPE=1
LETTER=2
TIMESTAMP=3
URBACKUPSTATUS=4

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
        yield Service(item=check_name_urbackup(line_as_string), parameters=urbackup_check_default_levels)

# the check function (dummy)
def check_urbackup(item, params, section):
    #return 0 if check of backups should not be done
    if params['check_backup'] == 'ignore':
        yield (Result(state=State.OK, summary='check disabled by rule'))
        return

    for line in section:
        line_as_string=' '.join(map(str,line))
        machine_infos = line_as_string.split(";;;;;")

        if check_name_urbackup(line_as_string) == item:
            #if urbackup status is used ...
            if params['modi'] == 'use_urbackup_status':
                if machine_infos[URBACKUPSTATUS].lower() == 'true':
                    yield (Result(state=State.OK, summary='status reported by UrBackup is: True'))
                if machine_infos[URBACKUPSTATUS].lower() == 'false':
                    yield (Result(state=State.CRIT, summary='status reported by UrBackup is: False'))

            #if backup age is used
            if params['modi'] == 'use_backup_age':
                stamp = getDateFromString(machine_infos[TIMESTAMP])

                if stamp is None:
                    yield (Result(state=State.UNKNOWN, summary='No backup configured, no backup done yet or no last backup date reported by urbackup'))

                if stamp is not None:
                    #old = time.time() - time.mktime(stamp)
                    n = time.strftime('%Y-%m-%d_%H:%M%z',time.localtime())
                    cdt = datetime.strptime(n, '%Y-%m-%d_%H:%M%z')
                    olddt = cdt - stamp
                    old = olddt.total_seconds()
            
                    warn, crit = params['backup_age']
                    infotext = 'last ' + machine_infos[BACKUP_TYPE] + ': ' + render.datetime(stamp.timestamp()) + ' (Age: ' + render.timespan(old) + ' warn/crit at ' + render.timespan(warn) + '/' + render.timespan(crit) + ')'
                    
                    if "use_performance_data" not in params or params['use_performance_data'] == 'enable':
                        yield Metric('age', int(old), levels=(warn,crit), boundaries=(0, None))

                    if old >= crit:
                        yield (Result(state=State.CRIT, summary=infotext))
                        return
                    if old >= warn:
                        yield (Result(state=State.WARN, summary=infotext))
                        return

                    yield (Result(state=State.OK, summary=infotext))


register.check_plugin(
    name = "urbackup_check",
    service_name = "Urbackup %s",
    discovery_function = discovery_urbackup_check,
    check_function = check_urbackup,
    check_default_parameters = urbackup_check_default_levels,
    check_ruleset_name = "urbackup"
)

def getDateFromString(datetime_string):
    try:
        d = datetime.strptime(datetime_string,"%Y-%m-%d_%H:%M%z")
        return d
    except ValueError:
        return None

#thanks to https://gist.github.com/thatalextaylor/7408395
def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s%dd %dh %dm' % (sign_string, days, hours, minutes)
    elif hours > 0:
        return '%s%dh %dm' % (sign_string, hours, minutes)
    elif minutes > 0:
        return '%s%dm' % (sign_string, minutes)
    else:
        return '0m'
