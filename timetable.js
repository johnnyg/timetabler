// Returns current week of the semester
function currentWeek() {

   var week0 = new Date("February 21, 2010");
   var midBreak = new Date("April 4, 2010");
   var today = new Date();
   var diff = new Date (today.getTime()-week0.getTime());
   var week = Math.floor(diff.getTime() / (1000 * 60 * 60 * 24 * 7));
   if (today >= midBreak) {
      week--;
   }
   return week;
}

// Returns the week the timetable is displaying for
function getWeek() {

   return document.title.match(/-?\d+/);
}

// Returns whether or not number is odd
function isOdd(num) {

   return num % 2 == 1;
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

// Show Odd Week Classes
function showOddClasses() {
   removeCSSRule(".odd");
}

// Show Even Week Classes
function showEvenClasses() {
   removeCSSRule(".even");
}

// Hide Odd Week Classes
function hideOddClasses() {
   addCSSRule(".odd", "display: none");
}

// Hide Even Week Classes
function hideEvenClasses() {
   addCSSRule(".even", "display: none");
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

   var init = (getWeek() === null);
   var update = (init || (isOdd(week) != isOdd(getWeek())));

   document.title="Johnny G's Timetable for Week "+week;
   window.status="Johnny G's Timetable for Week "+week;

   if (!init && update) {
      if (isOdd(week)) {
         showOddClasses();
      } else {
         showEvenClasses();
      }
   }

   if (update) {
      if (isOdd(week)) {
         hideEvenClasses();
      } else {
         hideOddClasses();
      }
   }
}

function init(e) {

   displayTimetable();

   if (document.addEventListener) {
      document.getElementById('prev').addEventListener('click', function () { displayTimetable(parseInt(getWeek())-1); }, false);
      document.getElementById('this').addEventListener('click', function () { displayTimetable(); }, false);
      document.getElementById('next').addEventListener('click', function () { displayTimetable(parseInt(getWeek())+1); }, false);
   } else {
      document.getElementById('prev').attachEvent('onclick', function () { displayTimetable(parseInt(getWeek())-1); });
      document.getElementById('this').attachEvent('onclick', function () { displayTimetable(); });
      document.getElementById('next').attachEvent('onclick', function () { displayTimetable(parseInt(getWeek())+1); });
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
