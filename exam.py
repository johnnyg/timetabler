#!/usr/bin/env python
# Creates a timetable webpage for a given timetable ini file

import ConfigParser
from cgi import escape
from datetime import datetime, time

class Exam(object):
    def __init__(self, name, options):
        # Parse name
        if '#' in name:
            name = name.partition('#')[0]

        date = datetime.strptime(options["date"], options["date_format"])
        start = datetime.strptime(options["start"], options["time_format"])
        end = datetime.strptime(options["end"], options["time_format"])

        self.__code = name
        self.__title = options["title"]
        self.__start = datetime.combine(date, start.time())
        self.__end = datetime.combine(date, end.time())
        self.__location = options["location"]
        self.__bring = options["bring"]

    @property
    def course(self):
        return self.__code + ": " + self.__title

    @property
    def location(self):
        return self.__location

    @property
    def date(self):
        suffix = "th"
        if self.__start.day < 10 or self.__start.day > 20:
            suffix = {
                1 : "st",
                2 : "nd",
                3 : "rd"
            }.get(self.__start.day % 10, "th")
        return self.__start.strftime("%%A, the %%d%s of %%B" % suffix)

    @property
    def start(self):
        return self.__start.strftime("%H:%M %p")

    @property
    def end(self):
        return self.__end.strftime("%H:%M %p")

    @property
    def bring(self):
        return self.__bring

def parse_config(config_file):

    config = ConfigParser.RawConfigParser({
        "date_format" : "%d/%m/%Y",
        "time_format" : "%H:%M"
    })
    config.read(config_file)

    exams = []

    for section in config.sections():
        exams.append(Exam(section, dict(config.items(section))))

    return exams

def exams_to_html(exams):

    now = datetime.now()
    semester = ((now.month-1)//6)+1

    html = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
   <title>Exam Timetable S%s '%s</title>
   <link rel="stylesheet" type="text/css" href="exam.css">
   <script type="text/javascript" src="exam.js"></script>
</head>
<body>
   <h1>Exam Timetable</h1>
   <h3 id="semester">Semester %s %s</h3>
   <table id="exams" summary="exam timetable">
      <tr>
         <th>Course</th>
         <th>Location</th>
         <th>Time Left</th>
         <th>Date</th>
         <th>Start Time</th>
         <th>End Time</th>
         <th>Bring</th>
      </tr>""" % (semester, now.strftime("%y"), semester, now.strftime("%Y"))

    for exam in exams:
        html += """
      <tr>
         <td>%s</td>
         <td>%s</td>
         <td></td>
         <td>%s</td>
         <td>%s</td>
         <td>%s</td>
         <td>%s</td>
      </tr>""" % (escape(exam.course), escape(exam.location), escape(exam.date),
                  escape(exam.start), escape(exam.end), escape(exam.bring))

    html += """
   </table>
</body>
</html>"""

    return html

if __name__ == "__main__":

    import sys

    for config_file in sys.argv[1:]:
        out_file = config_file.rpartition('.')[0] + ".html"
        try:
            exams = parse_config(config_file)
        except Exception, e:
            print "Error parsing %s: %s" % (config_file, e)
        else:
            try:
                f = open(out_file, "w")
                f.write(exams_to_html(exams))
            except Exception, e:
                print "Error writing to %s: %s" % (out_file, e)
            finally:
                f.close()
