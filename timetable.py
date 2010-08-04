#!/usr/bin/env python
# Creates a timetable's HTML file

import ConfigParser
import pprint

DEFAULTS = {
    'type'  : 'class',
    'weeks' : '1-14'
}

config = ConfigParser.RawConfigParser(DEFAULTS)
config.read("timetable.ini")

activities = {}

for section in config.sections():
    (activity, sep, activity_type) = section.partition(':')
    activities.setdefault(activity, {})[activity_type] = {}
    for option in config.options(section):
        option_value = config.get(section, option)
        if option == "weeks":
            if option_value == "odd":
                option_value = range(1,14,2)
            elif option_value == "even":
                option_value = range(2,14,2)
            else:
                weeks = []
                for week in option_value.split(','):
                    (first, sep, last) = week.partition('-')
                    if not last:
                        last = first
                    weeks.extend(range(int(first),int(last)+1))
                option_value = weeks
        elif option == "time":
            (day, sep, time) = option_value.partition(' ')
            (start, sep, end) = time.partition('-')
            if end.endswith("pm"):
                offset = 12
                end = end.replace("pm","")
            else:
                offset = 0
                end = end.replace("am","")
            end = (int(end) + offset) % 24
            if start.endswith("am"):
                offset = 0
                start = start.replace("am", "")
            elif start.endswith("pm"):
                offset = 12
                start = start.replace("pm", "")
            start = (int(start) + offset) % 24
            option_value = "%s %d-%d" % (day, start, end)
        activities[activity][activity_type][option] = option_value

pprint.pprint(activities, width=120)
