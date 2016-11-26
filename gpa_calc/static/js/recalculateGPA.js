$(function() {
  $('#recalculate-gpa').bind('click', function() {
    courses = [];
    $('#grades-table tr').each(function(i, row) {
      if (i == 0) { return true; } // Skip header row
      course_data = {};
      let include = false;

      $(this).children().each(function(j, cell) {
        // Only include in list if course affects GPA and checkbox is checked
        if ($(this).attr('class') == 'affects_gpa') {
          if (!$(this).empty() && $(this).find('input').checked) {
            include = true;
          }
          course_data[$(this).attr('class')] = include;
        }
        else {
          course_data[$(this).attr('class')] = $(this).html();
        }
      });
      if (include) { courses.push(course_data); }
      console.log(course_data);
    });
    // $.getJSON($SCRIPT_ROOT + '/_recalculate_gpa', {

      // a: $('input[name="a"]').val(),
      // b: $('input[name="b"]').val()
    // }, function(data) {
      // $("#result").text(data.result);
    // });
    return false;
  });
});
