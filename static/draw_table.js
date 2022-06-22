(function($) {
  var CheckboxDropdown = function(el) {
    var _this = this;
    this.isOpen = false;
    this.areAllChecked = false;
    this.$el = $(el);
    this.$label = this.$el.find('.dropdown-label');
    this.$checkAll = this.$el.find('[data-toggle="check-all"]').first();
    this.$inputs = this.$el.find('[type="checkbox"]');
    
    this.onCheckBox();
    
    this.$label.on('click', function(e) {
      e.preventDefault();
      _this.toggleOpen();
    });
    
    this.$checkAll.on('click', function(e) {
      e.preventDefault();
      _this.onCheckAll();
    });
    
    this.$inputs.on('change', function(e) {
      _this.onCheckBox();
    });
  };
  
  CheckboxDropdown.prototype.onCheckBox = function() {
    this.updateStatus();
  };
  
  CheckboxDropdown.prototype.updateStatus = function() {
    var checked = this.$el.find(':checked');
    disp_txt = checked.parent('label').text();
    
    this.areAllChecked = false;
    this.$checkAll.html('Check All');
    
    if(checked.length <= 0) {
      this.$label.html('Select Options');
    }
    else if(checked.length === 1) {
      this.$label.html(disp_txt);
    }
    else if(checked.length === this.$inputs.length) {
      this.$label.html(disp_txt);
      this.areAllChecked = true;
      this.$checkAll.html('Uncheck All');
    }
    else {
      this.$label.html(disp_txt);
    }
  };
  
  CheckboxDropdown.prototype.onCheckAll = function(checkAll) {
    if(!this.areAllChecked || checkAll) {
      this.areAllChecked = true;
      this.$checkAll.html('Uncheck All');
      this.$inputs.prop('checked', true);
    }
    else {
      this.areAllChecked = false;
      this.$checkAll.html('Check All');
      this.$inputs.prop('checked', false);
    }
    
    this.updateStatus();
    update_filter_code();
  };
  
  CheckboxDropdown.prototype.toggleOpen = function(forceOpen) {
    var _this = this;
    
    if(!this.isOpen || forceOpen) {
       this.isOpen = true;
       this.$el.addClass('on');
      $(document).on('click', function(e) {
        if(!$(e.target).closest('[data-control]').length) {
         _this.toggleOpen();
        }
      });
    }
    else {
      this.isOpen = false;
      this.$el.removeClass('on');
      $(document).off('click');
    }
  };
  
  var checkboxesDropdowns = document.querySelectorAll('[data-control="checkbox-dropdown"]');
  for(var i = 0, length = checkboxesDropdowns.length; i < length; i++) {
    new CheckboxDropdown(checkboxesDropdowns[i]);
  }
})(jQuery);



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

