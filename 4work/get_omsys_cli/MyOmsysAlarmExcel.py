
class MyOmsysAlarmExcel():
    def __init__(self, alarm_name, alarm_name_suffix,alarm_desc,alarm_id, alarm_type,alarm_severity):
        suffix_map = {
            "interface":"接口"
        }
        if alarm_name_suffix != None:
            self.id = alarm_name + "_" + alarm_name_suffix
            self.title_en = alarm_name + "(" + alarm_name_suffix + ")"
            self.title_zh = alarm_name + "（" + suffix_map[alarm_name_suffix] + "）"
            self.id = self.id.lower()
        else:
            self.id = alarm_name.lower()
            self.title_zh = alarm_name
            self.title_en = alarm_name
        self.alarmdesc = alarm_desc
        self.alarm_id = alarm_id
        self.alarm_type = alarm_type
        self.alarm_severity = alarm_severity

    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc