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
        ignored_elements=("use_performance_data",),
        migrate=lambda model: { #force defaults for with model.get(...,DEFAULT)
            'check_backup': _migrate_check_backup(model.get('check_backup',True)),
            'backup_age': migrate_to_upper_float_levels(model.get('backup_age',('fixed',(1.5 * 86400.0, 2 * 86400.0)))),
            'modi': _migrate_modi(model.get('modi',('use_backup_age',None))),
        },
        elements = {
            'check_backup': DictElement(
                required=True,
                parameter_form=BooleanChoice(    
                    title=Title('Enable or disable check of backup (checked is enabled)'),                
                    prefill=DefaultValue(True),
                )
            ),

            'modi': DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title('Modi: use the status provided by UrBackup (see Status Webpage of Urbackup), or use level from this check'),
                    prefill=DefaultValue("use_backup_age"),
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

rule_spec_urbackup = CheckParameters(
    name="urbackup",
    topic=Topic.STORAGE,
    parameter_form=_parameter_urbackup,
    title=Title("Urbackup Check"),
    condition=HostAndItemCondition(item_title=Title("Urbackup Service item")),
)