# Author: Matthias Maderer
# E-Mail: edvler@edvler-blog.de
# URL: https://github.com/edvler/check_mk_urbackup-check
# License: GPLv2

register_check_parameters(
    subgroup_os,
    "urbackup",
    _("UrBackup"),
    Dictionary(
        elements = [
            ("check_backup",
             DropdownChoice(
                 title = _("Enable (default) or disable check of backup"),
                 help=_("If disabled is choosen, the check will always return OK. To enable checks of the backup, select enable. This is usefull if you have clients in UrBackup, for which no regular backups are done and you dont want them to be checked."),
                 choices = [
                     ("ignore", _("disable")),
                     ("check", _("enable")),
                 ]
             )
            ),
            ("modi",
             DropdownChoice(
                 title = _("Modi: use the status provided by UrBackup (see Status Webpage of Urbackup), or use backup age (default) as check criteria"),
                 help=_("Choose how the status of the backup should be determined."),
                 choices = [
                     ("use_backup_age", _("Backup age: Use the warning an critical limits given under Age of Backup")),
                     ("use_urbackup_status", _("UrBackup status: Use the status of the UrBackup Status Page")),
                 ]
             )
            ),
            ('backup_age',
             Tuple(
                 title = "Age of Backup before changing to warn (default 26h) or error (default 30h). This parameters are only used, if modi Backup Age is choosen!",
                 elements = [
                     Age(title=_("Warning at or above a backupage of"),
                         default_value = 93600,
                         display = [ "minutes" ],
                         help=_("If the backup is older than the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")
                     ),
                     Age(title=_("Critical at or above a backupage of"),
                         default_value = 108000,
                         display = [ "minutes" ],
                         help=_("If the backup is older than the specified time, the check changes to critical. (24h=1440m; 26h=1560m)")
                     ),
                 ]
             )
            ),
        ]
    ),
    TextAscii(
        title = _("Description"),
        allow_empty = True
    ),
    match_type = "dict",
)
