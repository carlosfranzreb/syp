/*jshint esversion: 6 */

/* Remove 'Último cambio' column on mobile */
function resize_table() {
    let table = document.getElementById('overview_table');
    let col_nr;  // Find col nr. of last change
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        if (table.rows[0].cells[i].textContent.trim() == 'Último cambio') {
            col_nr = i;
            break;
        }
    }
    let display = window.outerWidth < 600 ? 'none' : 'block';
    if (table.rows[0].cells[col_nr].style.display == display)
        return;  // display already correct
    for (let i = 0; i < table.rows.length; i++)
        table.rows[i].cells[col_nr].style.display = display;   
}

window.addEventListener('load', resize_table);
window.addEventListener('resize', resize_table);
