# [Check MK](https://mathias-kettner.de/check_mk.html) Plugin to check [UrBackup](http://www.urbackup.org) backups

# Installation

## On the Monitoring Server where Check_mk is installed:
For a detailed description how to work with mkp's goto [https://mathias-kettner.de/cms_mkps.html](https://mathias-kettner.de/cms_mkps.html).

### Short tasks
0. Login with your site user (user has the same name as the CMK-Site)
1. copy the urbackup-check*.mkp (see [dist](dist) folder) to your Check_mk server into the /tmp folder.
2. mkp install /tmp/urbackup-check*.mkp (replace * with the current version)
3. Check if installation worked
```
SITEUSER@monitoring01:/opt/omd# find . -name urbackup-check
./sites/XXXX/var/check_mk/packages/urbackup-check
./sites/XXXX/local/share/check_mk/checks/urbackup-check
./sites/XXXX/local/share/check_mk/checkman/urbackup-check
./sites/XXXX/local/share/check_mk/agents/plugins/urbackup-check
```
4. Goto your Check_mk webinterface. Choose WATO -> Host & Service Parameters. Search for urbackup.

## On the UrBackup Server (NOT THE CHECK_MK SERVER!):
1. Install UrBackup API. (https://github.com/uroni/urbackup-server-python-web-api-wrapper)
```
  On Ubuntu 16.04.4: apt-get install python3-pip && pip3 install urbackup-server-web-api-wrapper
```
2. Copy the plugin script [check_mk/agents/plugins/urbackup-check](check_mk/agents/plugins/urbackup-check) into /usr/lib/check_mk_agent/plugins/
3. chmod 755 /usr/lib/check_mk_agent/plugins/urbackup-check
4. Create urbackup-check.ini in $MK_CONFDIR folder (usually /etc/check_mk). See Template [etc/check_mk/urbackup-check.ini](etc/check_mk/urbackup-check.ini)
5. Execute the script: /usr/lib/check_mk_agent/plugins/urbackup-check. If everythings works the output should look like this
```
root@urbackup-server:/usr/lib/check_mk_agent/plugins# ./urbackup-check
<<<urbackup-check>>>
FMT-PC;;;;;-;;;;;False;;;;;-;;;;;False
NB03;;;;;-;;;;;False;;;;;2017-05-15_08:51;;;;;False
PC01;;;;;2018-02-22_18:05;;;;;False;;;;;2018-02-22_18:36;;;;;True
PC02;;;;;2018-02-23_08:19;;;;;True;;;;;2018-02-23_08:57;;;;;True
PC03;;;;;2018-02-12_00:08;;;;;False;;;;;2017-05-15_09:36;;;;;False
PC04;;;;;-;;;;;False;;;;;2018-01-01_00:00;;;;;False
PC05;;;;;2017-10-02_00:08;;;;;False;;;;;2018-02-17_12:02;;;;;True
pc-xx;;;;;-;;;;;False;;;;;2017-05-15_09:16;;;;;False
swyx01;;;;;2018-02-23_00:02;;;;;True;;;;;2018-02-23_01:01;;;;;True
```

## Functions of the plugin
![](https://github.com/edvler/check_mk-urbackup-check/blob/master/docs/urbackup-check_man-page.png)

## Services screenshot
![](https://github.com/edvler/check_mk-urbackup-check/blob/master/docs/example-services-screenshot.png)
