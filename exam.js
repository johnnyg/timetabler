function countdown(to, from) {
   // "Constants" used for calculating difference
   var SECOND = 1000;
   var MINUTE = 60 * SECOND;
   var HOUR = 60 * MINUTE;
   var DAY = 24 * HOUR;

   // If from isn't specified, use the current time
   if (from === undefined) {
      from = new Date();
   }

   // Calculate time difference in ms
   var diff = to-from;
   var timeLeft = "";

   // Only create string if event hasn't occured yet
   if (diff >= 0) {
      // Calculate time difference in human form
      var days = Math.floor(diff / DAY);
      if (days < 10) days = "0"+days;
      days += days == "01" ? " day" : " days";
      var hours = Math.floor((diff % DAY) / HOUR);
      if (hours < 10) hours = "0"+hours;
      var minutes = Math.floor((diff % HOUR) / MINUTE);
      if (minutes < 10) minutes = "0"+minutes;
      var seconds = Math.floor((diff % MINUTE) / SECOND);
      if (seconds < 10) seconds = "0"+seconds;

      timeLeft = days+", "+hours+":"+minutes+":"+seconds;
   }

   return timeLeft;
}

function updateCountdowns(exams) {
   var now = new Date();
   var table = document.getElementById('exams').tBodies[0];
   var toDelete = 0;

   // Update countdowns
   for (var i = 0, len = exams.length; i < len; i++) {
      var node = exams[i]["node"];
      var date = exams[i]["date"];
      if (date >= now) {
         node.nodeValue = countdown(date, now);
      } else {
         var row = node.parentNode.parentNode;
         row.parentNode.removeChild(row);
         toDelete++;
      }
   }

   // Delete expired exams
   exams.splice(0, toDelete);
}

function init(e) {

   var year = document.getElementById('semester').firstChild.nodeValue.split(' ').slice(-1);
   var courses = document.getElementById('exams').tBodies[0];
   var exams = [];

   for (var i = 1, len = courses.rows.length; i < len; i++) {
      var col = courses.rows[i].cells;
      var date = col[3].firstChild.nodeValue;
      var time = col[4].firstChild.nodeValue;
      date = date.replace(/\b(the|of)\b/g, '');
      date = date.replace(/\b(\d{1,2})(st|nd|rd|th)\b/, '$1');
      if (!col[2].hasChildNodes()) {
         col[2].appendChild(document.createTextNode(""));
      }
      exams.push({ "node" : col[2].firstChild, "date" : new Date(date+" "+time+" "+year) });
   }

   // Update Countdowns every 500ms (0.5s)
   updateCountdowns(exams);
   setInterval(function () {
      updateCountdowns(exams);
   }, 500);
}

if (window.addEventListener) {
   window.addEventListener('load', init, false);
} else if (document.addEventListener) {
   document.addEventListener('load', init, false);
} else if (window.attachEvent) {
   window.attachEvent('onload', init);
}
