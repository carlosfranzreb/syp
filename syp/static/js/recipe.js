function change_quantities(select) {
  /*
  Changes the quantities of the ingredients
  unit id in value: 1 -> g, 2 -> mL, 3 -> tazas
  */

  var before = $(select).attr("data-before");
  var after = $(select).children("option:selected").val();

  $(".ul_pepper").children("li").each(function() {
    var text = $(this).text();

    // Rounding for 'taza', 'cucharada' and 'cucharadita'
    if ($.inArray($(this).val(), [3, 5, 6, 7]) >= 0) {
      var number = parseFloat(text.match(/\d+(\.\d+)?/))
      var new_number = round_half((number / before) * after);

      if ($.inArray($(this).val(), [3, 6, 7]) >= 0) {
        if (new_number == 1 && text.slice(-1) == 's') {  // remove "s" if amount == 1
          var text = text.slice(0, -1);
        } else if (number == 1) {  // add "s" if amount was 1
            var text = text + "s";
        }

      } else if ($(this).val() == 5) {  // Plural for 'unidad' ends in 'es'
        if (new_number == 1 && text.slice(-2) == 'es') {  // remove "es" if amount == 1
          var text = text.slice(0, -2);
        } else if (number == 1) {  // add "es" if amount was 1
            var text = text + "es";
        }
      }

    } else if ($.inArray($(this).val(), [1, 2]) >= 0) {  // Rounding for g and mL
      var number = parseInt(text.match(/\d+/), 10);
      var new_number = round_5((number / before) * after);
    }

    var new_text = text.replace(number, new_number);
    $(this).text(new_text);

  });

  if (before == "1") { // "Personas" if it was 1 person
    $("#text-person").html("personas");
  }

  if (after == "1") { // "Persona" if now 1 person
    $("#text-person").html("persona");
  }

  $(select).attr("data-before", after);
}


function round_5(x) { // Rounds number to the nearest 5
  return (x % 5) >= 2.5 ? parseInt(x / 5) * 5 + 5 : parseInt(x / 5) * 5;
}


function round_half(x) { // Rounds number to the 0.5
  return Math.round(x * 2) / 2;
}


$(document).ready(function() {
  /*
  Checks if units 'cucharada', 'cucharadita', 'unidad' and 'taza'
  should be in plural. If so, correct the mistakes.
  */
  $(".ul_pepper").children("li").each(function() {
    var text = $(this).text();

    // Rounding for 'taza', 'cucharada' and 'cucharadita'
    if ($.inArray($(this).val(), [3, 5, 6, 7]) >= 0) {
      var number = parseFloat(text.match(/\d+(\.\d+)?/))

      if (number != 1) {
        if ($.inArray($(this).val(), [3, 6, 7]) >= 0) {  // add "s"
          var text = text + "s";
        } else {  // Plural for 'unidad' ends in 'es'
          var text = text + "es";
        }
      }
    }

    $(this).text(text);

  });
});
