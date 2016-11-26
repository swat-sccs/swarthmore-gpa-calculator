$(function() {
  function isEmpty(el){
    return !$.trim(el.html())
  }

  $('#recalculate-gpa').bind('click', function() {
    courses = [];
    $('#grades-table tr').each(function(i, row) {
      if (i == 0) { return true; } // Skip header row
      course_data = {};
      let include = false;

      $(this).children().each(function(j, cell) {
        // Only include in list if course affects GPA and checkbox is checked
        if ($(this).attr('class') == 'affects_gpa') {
          if (!isEmpty($(this)) && $(this).children().first().is(':checked')) {
            include = true;
          }
          course_data[$(this).attr('class')] = include;
        }
        else {
          course_data[$(this).attr('class')] = $(this).html();
        }
      });
      if (include) { courses.push(course_data); }
    });
    $.getJSON($SCRIPT_ROOT + '/_recalculate_gpa', 
      {course_list: JSON.stringify(courses)}, 
      function(data) {
        $('#wa-query').attr('href', data.wa_query);

        $('#gpa').css('display', 'none');
        $('#gpa').html(data.latex);
        MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'gpa']);
        MathJax.Hub.Queue(function() {
          $('#gpa').css('display', 'inline');
        });
      }
    );
    return false;
  });
});
