#!/usr/bin/env python
# Creates a timetable webpage for a given timetable ini file

import ConfigParser

class Event(object):
    def __init__(self, name, options):
        # Parse name
        if '#' in name:
            name = name.partition('#')[0]

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

        (self.__name, self.__form) = name.partition(':')[::2]
        self.__category = options["type"]
        self.__location = options["location"]
        self.__weeks = options["weeks"]
        self.__time = options["time"]

    @property
    def name(self):
        return self.__name

    @property
    def form(self):
        return self.__form

    @property
    def category(self):
        return self.__category

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
        return repr(self)

    def __repr__(self):
        if self.__form:
            s = "%s (%s)" % (self.__name, self.__form)
        else:
            s = self.__name
        return s

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

def timetable_to_html(timetable):
    html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
   <title>Johnny G's Timetable</title>
   <link rel="stylesheet" type="text/css" href="timetable.css" />
   <script type="text/javascript" src="timetable.js"></script>
</head>

<body>
   <table summary="timetable">
       <tr>
          <th class="header">Hour</th>

          <th class="header">Monday</th>

          <th class="header">Tuesday</th>

          <th class="header">Wednesday</th>

          <th class="header">Thursday</th>

          <th class="header">Friday</th>
       </tr>"""

    for hour in sorted(timetable):
        html += """

       <tr>
          <th>%d:00 %s</th>""" % ((hour % 12, hour)[hour == 12], ("am", "pm")[hour >= 12])

        for day in ("Mon", "Tue", "Wed", "Thu", "Fri"):
            weeks = set()
            for event in timetable[hour].get(day, []):
                weeks.update(event.weeks)
                if event.start == hour:
                    html += """

          <td class="%s" rowspan="%d">
             %s<br />
             %s<br />
             %s
          </td>""" % (' '.join([event.category] + ["notWk%d" % week for week in set(range(1,14)) - set(event.weeks)]),
                      (event.finish - event.start) % 24, event.name, event.form, event.location)


            if len(weeks) < 14:
                classes = ' '.join(["notWk%d" % week for week in weeks])
                if classes:
                    classes = ' class="%s"' % classes
                html += """

          <td%s></td>""" % classes

        html += """
       </tr>"""

    html += """
   </table>

   <div>
       <input type="submit" value="previous week" id="prev" />
       <input type="submit" value="this week" id="this" />
       <input type="submit" value="next week" id="next" />
   </div>
</body>
</html>"""

    return html

if __name__ == "__main__":

    import sys

    for config_file in sys.argv[1:]:
        out_file = config_file.rpartition('.')[0] + ".html"
        try:
            timetable = parse_config(config_file)
        except Exception, e:
            print "Error parsing %s: %s" % (config_file, e)
        else:
            try:
                f = open(out_file, "w")
                f.write(timetable_to_html(timetable))
            except Exception, e:
                print "Error writing to %s: %s" % (out_file, e)
            finally:
                f.close()
