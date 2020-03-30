/*jshint esversion: 6 */


function toggle_filters(anchor) {
    /** Open select below the given anchor. */
    let filters = anchor.nextElementSibling;
    let all_filters = document.getElementsByClassName('filters');
    if (filters.style.display == 'none') {
        close_filters(all_filters);
        filters.style.display = 'block';
        anchor.className = 'icon fas fa-times';
        anchor.style.color = '#f56a6a';
    } else {
        close_filters(all_filters);
    }
}

function close_filters(all_filters) {
    /** Used by toggle_filters() to close all filters. */
    for (let item of all_filters) {
        item.style.display = 'none';
        let anchor = item.previousElementSibling;     
        anchor.className = 'icon fas fa-filter';
        anchor.style.color = '#3d4449';
    }
}