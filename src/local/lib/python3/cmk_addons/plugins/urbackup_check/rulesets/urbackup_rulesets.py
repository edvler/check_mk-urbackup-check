#!/usr/bin/env python3

# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk_urbackup-check
# License: GPLv2

from cmk.rulesets.v1 import (
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    migrate_to_upper_float_levels,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    FixedValue,
    )
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)

def _migrate_check_backup(model):    
    if isinstance(model, str):
        if model == "check":
            return True
        elif model == "ignore":
            return False
    return model

def _migrate_modi(model):
    if isinstance(model, str):
        return (model, None)
    return model

def _parameter_urbackup():
    return Dictionary(
        ignored_elements=("use_performance_data"),
        migrate=lambda model: { #force defaults for with model.get(...,DEFAULT)
            'check_backup': _migrate_check_backup(model.get('check_backup',True)),
            'backup_age': migrate_to_upper_float_levels(model.get('backup_age',('fixed',(1.5 * 86400.0, 2 * 86400.0)))),
            'modi': _migrate_modi(model.get('modi',('use_backup_age',None))),
        },
        elements = {
            'check_backup': DictElement(
                required=True,
                parameter_form=BooleanChoice(    
                    #migrate=lambda model: _migrate_check_backup(model),
                    title=Title('Enable or disable check of backup (checked is enabled)'),                
                    prefill=DefaultValue(True),
                )
            ),

            'modi': DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title('Modi: use the status provided by UrBackup (see Status Webpage of Urbackup), or use level from this check'),
                    prefill=DefaultValue("use_backup_age"),
                    #migrate= not needed! name of elements = values set with old plugin versions
                    elements=[
                        CascadingSingleChoiceElement(
                            name="use_backup_age",          
                            title=Title("Use levels defined in this check"),
                            parameter_form=FixedValue(value=None)
                        ),
                        CascadingSingleChoiceElement(
                            name="use_urbackup_status",
                            title = Title('Use the status of the UrBackup Status Page'),
                            parameter_form=FixedValue(value=None)
                        )                      
                    ]
                )
            ),

            'backup_age': DictElement(
                parameter_form=SimpleLevels(
                    title = Title('Age of Backup before changing to warn or critical. This parameters are only used, if modi "Use levels defined in this check" is choosen!'),
                    #migrate = lambda model: migrate_to_upper_float_levels(model),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = InputHint(
                        value=(1.5 * 86400.0, 2 * 86400.0),
                    )
                )
            ),
        }
    )

# def _parameter_urbackup_check():
#     return Dictionary(
#         required_keys=['check_backup'],
#         elements = [
#             ("use_performance_data",
#              DropdownChoice(
#                  title = _("Enable (default) to collect metrics (create a graph for backup age)"),
#                  help=_("If enabled, backup age is provided as metric to check_mk. You may want to disable this, if you have many hosts."),
#                  choices = [
#                      ("enable", _("enable")),
#                      ("disable", _("disable")),
#                  ],
#                  default_value='enable',
#              )
#             ),
#             ("check_backup",
#              DropdownChoice(
#                  title = _("Enable (default) or disable check of backup"),
#                  help=_("If disabled is choosen, the check will always return OK. To enable checks of the backup, select enable. This is usefull if you have clients in UrBackup, for which no regular backups are done and you dont want them to be checked."),
#                  choices = [
#                      ("ignore", _("disable")),
#                      ("check", _("enable")),
#                  ],
#                  default_value='check',	
#              )
#             ),
#             ("modi",
#              DropdownChoice(
#                  title = _("Modi: use the status provided by UrBackup (see Status Webpage of Urbackup), or use backup age (default) as check criteria"),
#                  help=_("Choose how the status of the backup should be determined."),
#                  choices = [
#                      ("use_backup_age", _("Backup age: Use the warning an critical limits given under Age of Backup")),
#                      ("use_urbackup_status", _("UrBackup status: Use the status of the UrBackup Status Page")),
#                  ],
#                  default_value='use_backup_age'
#              )
#             ),
#             ('backup_age',
#              Tuple(
#                  title = "Age of Backup before changing to warn (default 26h) or error (default 30h). This parameters are only used, if modi Backup Age is choosen!",
#                  elements = [
#                      Age(title=_("Warning at or above a backupage of"),
#                          default_value = 93600,
#                          help=_("If the backup is older than the specified time, the check changes to warning. (24h=1440m; 26h=1560m)")
#                      ),
#                      Age(title=_("Critical at or above a backupage of"),
#                          default_value = 108000,
#                          help=_("If the backup is older than the specified time, the check changes to critical. (24h=1440m; 26h=1560m)")
#                      ),
#                  ]
#             )
#           ),
#         ]
#     )

# def _itemspec_urbackup_check():
#     return DropdownChoice(
#                  title = _("Filter by Backup-Type"),
#                  help=_("Filter by type of backup"),
#                  choices = [
#                      ("filebackup", _("UrBackup Filebackup")),
#                      ("imagebackup", _("UrBackup Imagebackup")),
#                  ],
#                  default_value='imagebackup'
#              )

# rulespec_registry.register(
#     CheckParameterRulespecWithItem(
#         check_group_name='urbackup',
#         group=RulespecGroupCheckParametersApplications,
#         item_spec=lambda: TextAscii(title=_('Urbackup Service item'), ),
#         #item_spec=_itemspec_urbackup_check,
#         match_type='dict',
#         parameter_valuespec=_parameter_urbackup_check,
#         title=lambda: _("Urbackup Check"),
#     ))

rule_spec_urbackup = CheckParameters(
    name="urbackup",
    topic=Topic.STORAGE,
    parameter_form=_parameter_urbackup,
    title=Title("Urbackup Check"),
    condition=HostAndItemCondition(item_title=Title("Urbackup Service item")),
)