
function create_table(parent_id, table_id, column_list) {
    parent = document.getElementById(parent_id)
    tab = document.createElement("table");
    tab.id = table_id
    th = document.createElement("thead");
    tr = document.createElement("tr");
    for (column in column_list){
        col_head = document.createElement("th");
        col_head.innerHTML = column_list[column_list[column]]
        th.appendChild(col_head);
    }
    tab.appendChild(th);
    tab.className = "table table-striped";
    parent.appendChild(tab);
}
function update_table_columns(table, column_list) {
    for (column in column_list){
        var col = table.column( $(table).attr(column_list[column]) );
        col.visible(false)
    }
}
function update_table_data (id, data){

    
}


function sub_DataTable(table_id, data) {
    $('#'+table_id).DataTable({
        "data": JSON.parse(data),
        retrive :true, searching : false, info : false, paging : false, 
      "aaSorting": [],
      responsive : true,
        columns: [
            {data: "type"},
            {data: "D"},
            {data: "R1"},
            {data: "R2"},
            {data: "R3"}
          ]
        }
        )
}

function format ( table_id ) {
    // `d` is the original data object for the row
    return '<table id="'+table_id+'" class="display" border="0" style="padding-left:50px; width:50%;">'+
    '<thead>'+
    '<tr>'+
    '<th>Gene</th>'+
    '<th>D</th>'+
    '<th>R1</th>'+
    '<th>R2</th>'+
    '<th>R3</th>'+          
    '</tr>'+
    '</thead>'+
    '</table>';
}


var $range = $(".js-range-slider"),
    $from = $(".from"),
    $to = $(".to"),
    range,
    min = $range.data('min'),
    max = $range.data('max'),
    from,
    to;

var updateValues = function () {
    $from.prop("value", from);
    $to.prop("value", to);
};

$range.ionRangeSlider({
    onChange: function (data) {
      from = data.from;
      to = data.to;
      updateValues();
    }
});

range = $range.data("ionRangeSlider");
var updateRange = function () {
    range.update({
        from: from,
        to: to
    });
};

$from.on("input", function () {
    from = +$(this).prop("value");
    if (from < min) {
        from = min;
    }
    if (from > to) {
        from = to;
    }
    updateValues();    
    updateRange();
});

$to.on("input", function () {
    to = +$(this).prop("value");
    if (to > max) {
        to = max;
    }
    if (to < from) {
        to = from;
    }
    updateValues();    
    updateRange();
});