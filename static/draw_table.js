
function create_table(parent_id, table_id, rows_list) {
    parent = document.getElementById(parent_id)
    tab = document.createElement("table");
    tab.id = table_id
    th = document.createElement("thead");
    tr = document.createElement("tr");
    for (row in rows_list){
        row_head = document.createElement("th");
        row_head.innerHTML = rows_list[row]
        th.appendChild(row_head);
    }
    tab.appendChild(th);
    tab.className = "table table-striped";
    parent.appendChild(tab);
}
function update_table_rows(id, rows_list, data) {

}
function update_table_columns (id, rows_list)