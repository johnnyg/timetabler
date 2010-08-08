#!/usr/bin/env python
# Creates a timetable webpage for a given timetable ini file

import ConfigParser

class Event(object):
    def __init__(self, title, options):
        # Parse title
        if '#' in title:
            title = title.partition('#')[0]

        # Parse weeks
        if options["weeks"] == "odd":
            options["weeks"] = range(1,14,2)
        elif options["weeks"] == "even":
            options["weeks"] = range(2,14,2)
        else:
            weeks = []
            for week in options["weeks"].split(','):
                (first, last) = week.partition('-')[::2]
                if not last:
                    last = first
                weeks.extend(range(int(first),int(last)+1))
            options["weeks"] = weeks

        # Parse time
        (day, time) = options["time"].partition(' ')[::2]
        (start, end) = time.partition('-')[::2]
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
        options["time"] = "%s %d-%d" % (day, start, end)

        (self.__name, self.__type) = title.partition(':')[::2]
        self.__location = options["location"]
        self.__weeks = options["weeks"]
        self.__time = options["time"]

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def location(self):
        return self.__location

    @property
    def start(self):
        return int(self.__time.partition(' ')[2].partition('-')[0])

    @property
    def finish(self):
        return int(self.__time.partition(' ')[2].partition('-')[2])

    @property
    def day(self):
        return self.__time.partition(' ')[0]

    @property
    def weeks(self):
        return self.__weeks

    def __str__(self):
        if self.__type:
            s = "%s (%s)" % (self.__name, self.__type)
        else:
            s = self.__name
        return s

    def __repr__(self):
        return str(self)

def parse_config(config_file):

    config = ConfigParser.RawConfigParser({
        'type'  : 'class',
        'weeks' : '1-14'
    })
    config.read(config_file)

    timetable = {}

    for section in config.sections():
        event = Event(section, dict(config.items(section)))
        for hour in xrange(event.start, event.finish):
            timetable.setdefault(hour, {}).setdefault(event.day, []).append(event)

    return timetable

if __name__ == "__main__":

    import sys

    print parse_config(sys.argv[1])
