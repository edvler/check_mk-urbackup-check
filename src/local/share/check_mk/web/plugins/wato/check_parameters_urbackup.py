#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author: Matthias Maderer
# E-Mail: edvler@edvler-blog.de
# URL: https://github.com/edvler/check_mk_urbackup-check
# License: GPLv2

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    Tuple,
    Age,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)

def _parameter_urbackup_check():
    return Dictionary(
        required_keys=['check_backup'],
        elements = [
            ("check_backup",
             DropdownChoice(
                 title = _("Enable (default) or disable check of backup"),
                 help=_("If disabled is choosen, the check will always return OK. To enable checks of the backup, select enable. This is usefull if you have clients in UrBackup, for which no regular backups are done and you dont want them to be checked."),
                 choices = [
                     ("ignore", _("disable")),
                     ("check", _("enable")),
                 ],
                 default_value='check',	
             )
            ),
            ("modi",
             DropdownChoice(
                 title = _("Modi: use the status provided by UrBackup (see Status Webpage of Urbackup), or use backup age (default) as check criteria"),
                 help=_("Choose how the status of the backup should be determined."),
                 choices = [
                     ("use_backup_age", _("Backup age: Use the warning an critical limits given under Age of Backup")),
                     ("use_urbackup_status", _("UrBackup status: Use the status of the UrBackup Status Page")),
                 ],
                 default_value='use_backup_age'
             )
            ),
            ('backup_age',
             Tuple(
                 title = "Age of Backup before changing to warn (default 26h) or error (default 30h). This parameters are only used, if modi Backup Age is choosen!",
                 elements = [
                     Age(title=_("Warning at or above a backupage of"),
                         default_value = 93600,
                         help=_("If the backup is older than the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")
                     ),
                     Age(title=_("Critical at or above a backupage of"),
                         default_value = 108000,
                         help=_("If the backup is older than the specified time, the check changes to critical. (24h=1440m; 26h=1560m)")
                     ),
                 ]
            )
          ),
        ]
    )

def _itemspec_urbackup_check():
    return DropdownChoice(
                 title = _("Filter by Backup-Type"),
                 help=_("Filter by type of backup"),
                 choices = [
                     ("filebackup", _("UrBackup Filebackup")),
                     ("imagebackup", _("UrBackup Imagebackup")),
                 ],
                 default_value='imagebackup'
             )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='urbackup',
        group=RulespecGroupCheckParametersApplications,
        item_spec=lambda: TextAscii(title=_('Urbackup Service item'), ),
        #item_spec=_itemspec_urbackup_check,
        match_type='dict',
        parameter_valuespec=_parameter_urbackup_check,
        title=lambda: _("Urbackup Check"),
    ))

