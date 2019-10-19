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
  // Update subrecipe options for subrecipes
  $("#subrecipes li input").each(function() {
    $("#all_subrecipes option[value='" + $(this).val() + "']").remove();
  });
  // Update subrecipe options for the steps
  var select = $("#choose_subrecipe");
  var all_subrecipes = [];
  $("#subrecipes ul li").each(function() {
    all_subrecipes.push(
      $(this)
        .find("input")
        .val()
    );
  });
  var used_subrecipes = [];
  $("#steps ol li textarea")
    .filter(".is_subrecipe")
    .each(function() {
      used_subrecipes.push($(this).val());
    });
  var subrecipes = all_subrecipes.filter(x => !used_subrecipes.includes(x));
  for (idx = 0; idx < subrecipes.length; idx++) {
    select.append(new Option(subrecipes[idx], subrecipes[idx]));
  }
  select.val(
    select
      .children("option")
      .first()
      .val()
  );
  update_subrecipe_anchor();

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
    var new_item = "";
    if (div == "subrecipes") {
      new_item = $("#blueprint_subrecipes")
        .children(0)
        .clone();
    } else {
      new_item = first_item.clone();
    }
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
    if (section == "subrecipes") {
      $(link)
        .parent()
        .remove();
    } else {
      i = items.first();
      i.find("input, textarea").each(function() {
        $(this).val("");
      });
      i.find("select")
        .first()
        .val("0");
      i.css("display", "none");
    }
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

function add_subrecipe_steps() {
  $("#choose_subrecipe").css("display", "block");
}

function set_subrecipe_step() {
  // Subrecipe is added to the steps and removed from the options
  var select = $("#choose_subrecipe");
  var added_item = add_item(select.siblings("a:contains(paso)"));
  select.css("display", "none");
  var selected_option = select.find("option:selected");

  added_item
    .find("textarea")
    .val(selected_option.text())
    .attr("readonly", true)
    .addClass("is_subrecipe");
  added_item
    .children("a")
    .attr("onclick", "remove_item(this); update_subrecipe_options(this)");
  selected_option.remove();
  select.val(
    select
      .children("option")
      .first()
      .val()
  );
  update_subrecipe_anchor();
}

function remove_subrecipe(link) {
  var subrecipe = $(link)
    .siblings("input")
    .val();
  var is_removable = true;
  $("#steps ol li textarea")
    .filter(".is_subrecipe")
    .each(function() {
      if ($(this).val() == subrecipe) {
        is_removable = false;
        alert(
          "No se puede borrar la subreceta '" +
            subrecipe +
            "', porque está en los pasos de la receta."
        );
      }
    });
  if (is_removable == true) {
    $("#all_subrecipes").append(new Option("", subrecipe));
    // Remove subrecipe from step options
    // $("#choose_subrecipe option[value='" + subrecipe + "']").remove();
    $("#choose_subrecipe option").each(function() {
      if ($(this).val() == subrecipe) {
        $(this).remove();
      }
    });
    update_subrecipe_anchor();
    remove_item(link);
  }
}

function add_subrecipe_to_step_options(link, from_subrecipe = false) {
  var subrecipe = "";
  if (from_subrecipe == true) {
    // Subrecipe was added to subrecipes
    subrecipe = $(link).val();
  } else {
    // Subrecipe was removed from steps
    subrecipe = $(link)
      .siblings("textarea")
      .val();
  }
  var select = $("#choose_subrecipe");
  select.append(new Option(subrecipe, subrecipe));
  select.val(
    select
      .children("option")
      .first()
      .val()
  );
  update_subrecipe_anchor();
}

function update_subrecipe_options(item) {
  var before = $(item).attr("data-before");
  if (before != "None") {
    $("#all_subrecipes").append(new Option("", before)); // add_subrecipe_to_subrecipe_options
    $("#choose_subrecipe option[value='" + before + "']").remove(); // remove_subrecipe_from_step_options
  }
  $("#all_subrecipes option[value='" + $(item).val() + "']").remove(); // remove_subrecipe_from_subrecipe_options
  add_subrecipe_to_step_options(item, (from_subrecipe = true));
  $(item).attr("data-before", $(item).val()); // Update data-before
  update_subrecipe_anchor();
}

function update_subrecipe_anchor() {
  var select = $("#choose_subrecipe");
  select.css("display", "none");
  var link = $("#anchor_add_subrecipe");
  var options = select.children("option");
  if (options.length == 1 && link.text() == "Añadir subreceta") {
    link
      .text("Subrecetas incluidas")
      .css("color", "#599A00")
      .attr("onclick", "");
  } else if (options.length > 1 && link.text() == "Subrecetas incluidas") {
    link
      .text("Añadir subreceta")
      .css("color", "#F56A6A")
      .attr("onclick", "add_subrecipe_steps()");
  }
}

function update_video() {
  $(".video-container")
    .find("iframe")
    .attr("src", $("#video_link").val());
}
