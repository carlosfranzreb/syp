$(document).ready(function() {
    $(".ul_pepper")
        .children("li")
        .each(function() {
            var span = $(this).find("span");
            var text = span.text();
            var number = text.match(/\d+(\.\d+)?/);
            if (number != null) {
                nr = number[0];
                span.text(text.replace(nr, prettify(parseFloat(nr))));
            }
        });
});

function change_quantities(select) {
    var before = 2;
    var after = $(select)
        .children("option:selected")
        .val();

    $(".ul_pepper")
        .children("li")
        .each(function() {
            var span = $(this).find("span");
            var text = span.text();
            var str_nr = $(this).attr("data-before");

            if ($.inArray($(this).val(), [1, 2]) >= 0) {
                // Rounding for g and mL
                var number = parseInt(str_nr);
                var new_number = round_5((number / before) * after);
            } else {
                var number = parseFloat(str_nr);
                var new_number = round_quarter((number / before) * after);
            }
            if (new_number != 0) {
                if (new_number <= 1) {
                    // from plural to singular
                    unit = $(this).attr("data-singular");
                } else {
                    // from singular to plural
                    unit =
                        $(this).attr("data-singular") +
                        $(this).attr("data-plural");
                }
                new_text = text.replace(
                    /(.+)(\s[a-zA-Z]+)/,
                    prettify(new_number) + " " + unit
                );
                span.text(new_text);
            }
        });

    n_persons = $(select).attr("data-before");
    if (n_persons == "1") {
        // "Personas" if it was 1 person
        $("#text-person").html("personas");
    }
    if (after == "1") {
        // "Persona" if now 1 person
        $("#text-person").html("persona");
    }
    $(select).attr("data-before", after);
}

function round_5(x) {
    // Rounds number to the nearest 5th unit
    return x % 5 >= 2.5 ? parseInt(x / 5) * 5 + 5 : parseInt(x / 5) * 5;
}

function round_quarter(x) {
    // Rounds number to the 0.25
    return Math.round(x * 4) / 4;
}

function prettify(x) {
    // Change decimals to 1/2 and remove if .0
    if (Number.isInteger(x)) {
        return parseInt(x);
    }

    if (Number.isInteger(x - 0.25)) {
        decimal = "\u00BC";
    } else if (Number.isInteger(x - 0.5)) {
        decimal = "\u00BD";
    } else if (Number.isInteger(x - 0.75)) {
        decimal = "\u00BE";
    }

    int = Math.floor(x);
    if (int > 0) {
        return int + " " + decimal;
    } else {
        return decimal;
    }
}
