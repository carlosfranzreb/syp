/* ELSE IF was not working, don't know why. */
$(window).on('resize load', function(){
      var width = $(window).width()
      if (width < 450) {
        $('#textarea_h4').attr("rows", "6");
        $('#textarea_p').attr("rows", "40");
      }
      if (width >= 450) {
        $('#textarea_h4').attr("rows", "5");
        $('#textarea_p').attr("rows", "30");
      }
      if (width >= 580) {
        $('#textarea_h4').attr("rows", "3");
        $('#textarea_p').attr("rows", "24");
      }
      if (width >= 1280) {
        $('#textarea_h4').attr("rows", "2");
        $('#textarea_p').attr("rows", "14");
      }
});
