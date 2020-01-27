/*jshint esversion: 6 */


$(document).ready(function() {
  // On first load, remove Ingredient(...) from name
  // The check is necessary because it shouldn't be cut when the form is validated
  var ingredients = $(".ul_pepper").children("li");
  if (
    ingredients
      .first()
      .find("input:visible:first")
      .val()
      .includes("Ingredient(")
  ) {
    ingredients.each(function() {
      ingredient = $(this).find("input:visible:first");
      ing_val = ingredient.val();
      ingredient.val(ing_val.substring(12, ing_val.length - 2));
    });
  }


  // Disable submit on enter
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

/* ELSE IF was not working, don't know why. */
$(window).on("resize load", function() {
  var width = $(window).width();
  if (width < 450) {
    $("#textarea_h4").attr("rows", "6");
    $("#textarea_p").attr("rows", "40");
    $(".recipe_step").attr("rows", "15");
  }
  if (width >= 450) {
    $("#textarea_h4").attr("rows", "5");
    $("#textarea_p").attr("rows", "30");
    $(".recipe_step").attr("rows", "10");
  }
  if (width >= 580) {
    $("#textarea_h4").attr("rows", "3");
    $("#textarea_p").attr("rows", "24");
    $(".recipe_step").attr("rows", "8");
  }
  if (width >= 1280) {
    $("#textarea_h4").attr("rows", "2");
    $("#textarea_p").attr("rows", "14");
    $(".recipe_step").attr("rows", "5");
  }
});

function add_item(link) {
  var list = "";
  var div = $(link)
    .parent()
    .attr("id");
  if (div == "steps") {
    list = $(link).siblings("ol");
  } else {
    list = $(link).siblings("ul");
  }
  var items = list.children("li");
  var n_items = items.length;
  var first_item = items.first();
  if (n_items == 1 && first_item.css("display") == "none") {
    first_item.css("display", "block");
  } else {
    var new_item = first_item.clone();
    // Change values
    new_item.find("input, textarea").each(function() {
      $(this).val("");
    });
    new_item
      .find("select")
      .first()
      .val("0");
    // Change IDS and names
    new_item.find("input, select, textarea").each(function() {
      var old_id = $(this).attr("id");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("id", new_id);
      $(this).attr("name", new_id);
    });

    //Change for attribute of associated label
    new_item.find("label").each(function() {
      var old_id = $(this).attr("for");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("for", new_id);
    });

    list.append(new_item);
    return new_item;
  }
}

function remove_item(link) {
  var items = "";
  var section = $(link)
    .closest("article")
    .attr("id");
  if (section == "steps") {
    items = $(link)
      .closest("ol")
      .children("li");
  } else {
    items = $(link)
      .closest("ul")
      .children("li");
  }
  var n_items = items.length;
  if (n_items == 1) {
    i = items.first();
    i.find("input, textarea").each(function() {
      $(this).val("");
    });
    i.find("select")
      .first()
      .val("0");
    i.css("display", "none");
  } else {
    var item_id = $(link)
      .siblings("input, textarea")
      .attr("id");
    var item_nr = parseInt(item_id.match(/[a-zA-Z]+-(\d+)-[a-zA-Z]+/)[1]);
    var item = "";
    if (item_nr < n_items - 1) {
      for (idx = item_nr + 1; idx < n_items; idx++) {
        item = items.eq(idx);
        item.find("input, select, textarea").each(function() {
          var old_id = $(this).attr("id");
          var new_id = old_id.replace(
            /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
            "$1" + (idx - 1).toString() + "$3"
          );
          $(this).attr("id", new_id);
          $(this).attr("name", new_id);
        });

        //Change for attribute of associated label
        item.find("label").each(function() {
          var old_id = $(this).attr("for");
          var new_id = old_id.replace(
            /(ingredients-)(\d+)(-[a-zA-Z]+)/,
            "$1" + (idx - 1).toString() + "$3"
          );
          $(this).attr("for", new_id);
        });
      }
    }
    $(link)
      .parent()
      .remove();
  }
}

function toggle_subrecipe_input() {
  $("#choose_subrecipe").toggle();
  $("#subrecipe_button").toggle();
  $("#anchor_add_step").toggle();
  let anchor = $("#anchor_add_subrecipe");
  anchor.text(anchor.text() == "Cancelar" ? "Añadir subreceta" : "Cancelar");
}

function add_subrecipe() {
  let input = $("#choose_subrecipe");
  let subrecipe = input.val();
  let obj = $("#all_subrecipes").find("option[value='" + subrecipe + "']");
  if(obj != null && obj.length > 0) {
    let added_item = add_item(input.siblings("a:contains(paso)"));
    input.val('');  // Remove input.
    toggle_subrecipe_input();
    added_item
      .find("textarea")
      .val(subrecipe)
      .attr("readonly", true)
      .addClass("is_subrecipe")
      .children("a")
      .attr("onclick", "remove_item(this)");
  }
  else {  // don't allow submission
    alert("La subreceta que has escrito no existe. Elige una de la lista.");
  }
}

function update_video() {
  $(".video-container")
    .find("iframe")
    .attr("src", $("#link_video").val());
}
