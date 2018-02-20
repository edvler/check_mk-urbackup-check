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
            ( "check_backup",
              DropdownChoice(
                  title = _("Ignore or check the backup of this machine"),
		  help=_("If this is set to ignore, the check will always be {ok}. To enable backup checks use the check option."),
                  choices = [
                     ( "ignore",   _("ignore missing backups") ),
                     ( "check",   _("check for backups") ),
                  ]
              )
	    ),
            ( "modi",
              DropdownChoice(
                  title = _("Use the status from UrBackup (see status Webpage in Urbackup), or use backup age for checks"),
                  help=_("Choose how the status of the backup should be determined"),
                  choices = [
                     ( "use_backup_age",   _("Backup age: Use the warning an critical limits given under backup_age") ),
                     ( "use_urbackup_status",   _("UrBackup status: Use the status of the UrBackup Status Page") ),
                  ]
              )
            ),
            ('backup_age',
             Tuple(title = "Age of Backup before changing to warn or error (this parameters are only used, if - Backup age - modi is choosen!)",
                   elements = [
                       Age(title=_("Warning at or above backupage"), default_value = 93600, display = [ "minutes" ], help=_("If the backup is older as the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")),
                       Age(title=_("Critical at or above backupage"), default_value = 108000, display = [ "minutes" ], help=_("If the backup is older as the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")),
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
