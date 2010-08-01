#!/usr/bin/env python
# Creates a timetable's HTML file

import ConfigParser
import pprint

DEFAULTS = {
    'type'  : 'class',
    'weeks' : '1-14'
}

config = ConfigParser.RawConfigParser(DEFAULTS)
config.read("timetable.conf")

activities = {}

for section in config.sections():
    (activity, sep, activity_type) = section.partition(':')
    if activity not in activities:
        activities[activity] = {}
    activities[activity][activity_type] = {}
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
        activities[activity][activity_type][option] = option_value

pprint.pprint(activities, width=120)
