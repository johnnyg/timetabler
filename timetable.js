// Returns current week of the semester
function currentWeek() {
   var today = new Date();
   var diff = new Date (today.getTime()-O_WEEK.getTime());
   var week = Math.floor(diff.getTime() / (1000 * 60 * 60 * 24 * 7));
   if (today >= MID_BREAK) {
      week--;
   }
   return week;
}

// Returns the week the timetable is displaying for
function getWeek() {
   return document.title.match(/\d+/);
}

// Sets the week the timetable is displaying for
function setWeek(week) {
   document.title="Week "+week;
   window.status="Timetable for Week "+week;
}

// Adds a rule to the CSS stylesheet
function addCSSRule(name, text) {
   var styleSheet = document.styleSheets[0];
   if (styleSheet.insertRule) {
      styleSheet.insertRule(name+" {"+text+"}", styleSheet.cssRules.length);
   } else if (styleSheet.addRule) {
      styleSheet.addRule(name, text);
   } else {
      alert("ERROR: Cannot add CSS rule");
   }
}

// Removes a rule from the CSS stylesheet
function removeCSSRule(name) {
   var cssRules = [];
   if (document.styleSheets[0].cssRules) {
      cssRules = document.styleSheets[0].cssRules;
   } else if (document.styleSheets[0].rules) {
      cssRules = document.styleSheets[0].rules;
   } else {
      alert("ERROR: Cannot see CSS rules");
   }

   for (var i = 0, len = cssRules.length; i < len; i++) {
      if (cssRules[i].selectorText === name) {
         if (document.styleSheets[0].deleteRule) {
            document.styleSheets[0].deleteRule(i);
         } else if (document.styleSheets[0].removeRule) {
            document.styleSheets[0].removeRule(i);
         } else {
            alert("ERROR: Cannot remove CSS rule");
         }
         break;
      }
   }
}

// Displays the appropriate timetable for the given week
// if no week is given, uses current week
function displayTimetable(week) {

   if (week === undefined) {
      week = currentWeek();
   }

   if (week > 13) {
      window.location = "exam";
   }

   document.getElementById('prev').disabled = (week <= 1);
   document.getElementById('this').disabled = (week == currentWeek());
   document.getElementById('next').disabled = (week >= 13);

   if (getWeek() !== null) {
      removeCSSRule(".notWk"+getWeek());
   }
   addCSSRule(".notWk"+week, "display: none");

   // Make sure we do this last!
   setWeek(week);
}

function init(e) {
   displayTimetable();

   if (document.addEventListener) {
      document.getElementById('prev').addEventListener('click', function () {
         displayTimetable(parseInt(getWeek())-1);
      }, false);
      document.getElementById('this').addEventListener('click', function () {
         displayTimetable();
      }, false);
      document.getElementById('next').addEventListener('click', function () {
         displayTimetable(parseInt(getWeek())+1);
      }, false);
   } else {
      document.getElementById('prev').attachEvent('onclick', function () {
         displayTimetable(parseInt(getWeek())-1);
      });
      document.getElementById('this').attachEvent('onclick', function () {
         displayTimetable();
      });
      document.getElementById('next').attachEvent('onclick', function () {
         displayTimetable(parseInt(getWeek())+1);
      });
   }
}

if (currentWeek() > 13) {
   window.location = "exam";
}

if (window.addEventListener) {
   window.addEventListener('load', init, false);
} else if (document.addEventListener) {
   document.addEventListener('load', init, false);
} else if (window.attachEvent) {
   window.attachEvent('onload', init);
}
