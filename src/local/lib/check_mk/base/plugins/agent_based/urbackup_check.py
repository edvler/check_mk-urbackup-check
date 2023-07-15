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
# "{name};;;;;{filestamp};;;;;{fileok};;;;;{imagestamp};;;;;{imageok}"
#
# <<<urbackup-check>>>
# FMT-PC;;;;;-;;;;;False;;;;;-;;;;;False
# NB03;;;;;-;;;;;False;;;;;2017-05-15_08:51;;;;;False
# PC01;;;;;2018-02-16_18:05;;;;;False;;;;;2018-02-16_19:26;;;;;True
# PC02;;;;;2018-02-19_07:44;;;;;True;;;;;2018-02-19_07:56;;;;;True
# PC03;;;;;2018-02-12_00:08;;;;;False;;;;;2017-05-15_09:36;;;;;False
# PC04;;;;;-;;;;;False;;;;;2018-01-01_00:00;;;;;False
# PC05;;;;;2017-10-02_00:08;;;;;False;;;;;2018-02-17_12:02;;;;;True
# pc-xx;;;;;-;;;;;False;;;;;2017-05-15_09:16;;;;;False
# swyx01;;;;;2018-02-19_00:02;;;;;True;;;;;2018-02-19_00:50;;;;;True
#
# If the date field contains "-" no backup was done for this machine.
# Fileok and imageok represents the status of the UrBackup Status page.

# default parameters
urbackup_check_default_levels = {'check_backup': 'check', 'backup_age': (93600, 108000), 'modi': 'use_backup_age'}

# the inventory function (dummy)
def discovery_urbackup_check(section):
    # loop over all output lines of the agent
    for line in section:
        arr_backups = line[0].split(';;;;;')
        machine_name = arr_backups[0]
        yield Service(item=machine_name + ' filebackup', parameters=urbackup_check_default_levels)
        yield Service(item=machine_name + ' imagebackup', parameters=urbackup_check_default_levels)

# the check function (dummy)
def check_urbackup(item, params, section):
    #extract machine_name and backup_type
    machine_name = item[:-11].strip()
    backup_type = item[-11:].strip()

    #return 0 if check of backups should not be done
    if params['check_backup'] == 'ignore':
        yield (Result(state=State.OK, summary=backup_type + ' check disabled by rule'))
        return

    for line in section:
        machine_infos = line[0].split(";;;;;")

        if machine_infos[0] == machine_name:
            stamp = None
            status = None

            #get status and timestamp depending on type
            if backup_type == 'filebackup':
                status = machine_infos[2]
                stamp = getDateFromString(machine_infos[1])

            if backup_type == 'imagebackup':
                status = machine_infos[4]
                stamp = getDateFromString(machine_infos[3])

            #if urbackup status is used ...
            if params['modi'] == 'use_urbackup_status':
                if status == 'True':
                    yield (Result(state=State.OK, summary='status reported by UrBackup is: True'))
                if status == 'False':
                    yield (Result(state=State.CRIT, summary='status reported by UrBackup is: False'))

            #if backup age is used
            if params['modi'] == 'use_backup_age':
                if stamp is None:
                    yield (Result(state=State.CRIT, summary='no ' + backup_type + ' done yet'))

                if stamp is not None:
                    #old = time.time() - time.mktime(stamp)
                    n = time.strftime('%Y-%m-%d_%H:%M%z',time.localtime())
                    cdt = datetime.strptime(n, '%Y-%m-%d_%H:%M%z')
                    olddt = cdt - stamp
                    old = olddt.total_seconds()
            
                    warn, crit = params['backup_age']
                    infotext = 'last ' + backup_type + ': ' + render.datetime(stamp.timestamp()) + ' (Age: ' + render.timespan(old) + ' warn/crit at ' + render.timespan(warn) + '/' + render.timespan(crit) + ')'

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
