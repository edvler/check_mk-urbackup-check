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
            ('backup_age',
             Tuple(title = "Age of Backup before changing to warn or error",
                   elements = [
                       Age(title=_("Warning if backup is older than"), default_value = 93600, display = [ "minutes" ], help=_("If the backup is older as the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")),
                       Age(title=_("Critical if backup is older than"), default_value = 108000, display = [ "minutes" ], help=_("If the backup is older as the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")),
                   ]
		  )
            ),
            ( "modi",
              DropdownChoice(
                  title = _("Use the status from UrBackup (see startpage) or use backup age for checks"),
                  help=_("Choose how the status of the backup should be determined"),
                  choices = [
                     ( "use_backup_age",   _("Use the warning an critical limits given under backup_age") ),
                     ( "use_urbackup_status",   _("Use the status of the UrBackup Status Page") ),
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
