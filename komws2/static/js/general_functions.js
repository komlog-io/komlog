
function drag_start(e) {
    console.log('drag started');
    var window=$(this).parent();
    var id=window.attr('id');
    var obj_left=window.offset().left;
    var obj_top=window.offset().top;
    var mouse_left=e.originalEvent.pageX;
    var mouse_top=e.originalEvent.pageY;
    console.log(obj_left+','+obj_top+','+mouse_left+','+mouse_top);
    e.originalEvent.dataTransfer.setData("text/plain",obj_left+','+obj_top+','+mouse_left+','+mouse_top+','+id);
} 

function drag_enter(e) { 
    console.log('drag enter');
    e.preventDefault();
    e.stopPropagation();
    return false; 
} 

function drag_over(e) { 
    console.log('drag over');
    e.preventDefault();
    e.stopPropagation();
    return false; 
} 

function drop(e) { 
    console.log('drop');
    e.preventDefault();
    e.stopPropagation();
    var data = e.originalEvent.dataTransfer.getData("text/plain").split(',');
    var final_left = parseInt(data[0])-parseInt(data[2])+parseInt(e.originalEvent.pageX);
    var final_top = parseInt(data[1])-parseInt(data[3])+parseInt(e.originalEvent.pageY);
    console.log(data);
    var dm = $('#'+data[4]);
    if (dm) {
        console.log('Cambiando coordenadas a: '+final_left+','+final_top);
        dm.offset({top:final_top,left:final_left});
        console.log(dm.position());
    }
    return false;
} 

function close_window() {
    $(this).parent().parent().remove();
}

function initTree(id_div) {
  $(function() {
    $("#"+id_div).jstree({
      "themes" : {
        "theme" : "komlog",
        "icons" : false
      },
      "plugins" : ["themes", "ui", "html_data"]
    }).bind("select_node.jstree", function(e, data) {
      loadItemContent(data.rslt.obj[0].id,data.rslt.obj[0].textContent);
    });
  });
}

/*
 * Funcion para cargar cada item del Tree
 */

function loadItemContent(id,item){
  if (id) {
    var itemtype=id.split("#")[0];
    var itemid=id.split("#")[1];
    item=item.replace(/^\s+/g, '');
    switch (itemtype) {
      case "AC": getAC(itemid);
            break;
      case "DC": getDC(itemid);
            break;
      case "DD": getDD(itemid,item);
            break;      
    }
  }
}


function getAC(id){ 
    url="/etc/agent/"+id;
    $.ajax({ url: url, dataType: "json", success: function(data) {
                agtable=$('<table></table>');
                agtable.append('<tr><td>Agent Name: </td><td><input type="text" id="ag_name" value="'+data['ag_name']+'"></td></tr>');
                var button = $("<input />").attr('type','button');
                button.attr('value','Update');
                button.attr('onClick','updateAgent("'+data['aid']+'")');
                $("#c_content").empty();
                $("#c_content").append(agtable);
                $("#c_content").append(button);
                var newDs = $("<div></div>");
                newDs.append('<table></table>');
                newDs.append('<tr><td>Report Name: </td><td><input type="text" id="ds_name"></td></tr>');
                newDs.append('<tr><td>Script Name: </td><td><input type="text" id="script"></td></tr>');
                newDs.append('<tr><td>Minute: </td><td><input type="text" id="minute"></td></tr>');
                newDs.append('<tr><td>Hour: </td><td><input type="text" id="hour"></td></tr>');
                newDs.append('<tr><td>Day of Week: </td><td><input type="text" id="day_of_week"></td></tr>');
                newDs.append('<tr><td>Month: </td><td><input type="text" id="month"></td></tr>');
                newDs.append('<tr><td>Day of Month: </td><td><input type="text" id="day_of_month"></td></tr>');
                var newDsBtn = $("<input />").attr('type','button');
                newDsBtn.attr('value','Add Report');
                newDsBtn.attr('onClick','newDatasource("'+data['aid']+'")');
                newDs.append(newDsBtn);
                $("#c_content").append(newDs);
                }
        });
}

function getDC(id){ 
    url="/etc/ds/"+id;
    $.ajax({ url: url, dataType: "json", success: function(data) {
                dstable=$('<table></table>');
                dstable.append('<tr><td>Report Name: </td><td><input type="text" id="ds_name" value="'+data['ds_name']+'"></td></tr>');
                dstable.append('<tr><td>Script Name: </td><td><input type="text" id="script" value="'+data['ds_params']['script_name']+'"></td></tr>');
                dstable.append('<tr><td>Minute: </td><td><input type="text" id="minute" value="'+data['ds_params']['min']+'"></td></tr>');
                dstable.append('<tr><td>Hour: </td><td><input type="text" id="hour" value="'+data['ds_params']['hour']+'"></td></tr>');
                dstable.append('<tr><td>Day of Week: </td><td><input type="text" id="day_of_week" value="'+data['ds_params']['dow']+'"></td></tr>');
                dstable.append('<tr><td>Month: </td><td><input type="text" id="month" value="'+data['ds_params']['month']+'"></td></tr>');
                dstable.append('<tr><td>Day of Month: </td><td><input type="text" id="day_of_month" value="'+data['ds_params']['dom']+'"></td></tr>');
                var button = $("<input />").attr('type','button');
                button.attr('value','Update');
                button.attr('onClick','updateDatasource("'+data['did']+'")');
                $("#c_content").empty();
                $("#c_content").append(dstable);
                $("#c_content").append(button);
                }
        });
}


function labelSubstringStartingAtOfLength(string,index,length) {
          prefix=string.substr(0, index);
          stringtochange='<div class="label label-default" id='+index+'>'+string.substr(index,length)+'</div>';
          sufix=string.substr(index+length,string.length);
          result=prefix+stringtochange+sufix;
          return result;
}

function prepareDSContent(data) {
    finalcontent=data.ds_content;
    vararray=data.ds_vars;
    for (var i = vararray.length; i>0; i--){
        finalcontent=labelSubstringStartingAtOfLength(finalcontent,vararray[i-1][0],vararray[i-1][1]);
    }
    return finalcontent
}

function getDD(id,title){
    url="/var/ds/"+id
    var obj = $('#'+id+'.c_window');
    console.log(obj.attr('id'));
    if (obj.attr('id') === undefined) {
      $.getJSON(url,function(data){
          content=prepareDSContent(data);
          var window = $("<div>").addClass("c_window");
          window.attr('id',id);
          window.appendTo("#c_content")
          var window_title = $("<h3>").html(title).attr("draggable","true");
          window_title.on('dragstart',drag_start);
          window_title.appendTo(window);
          var button_bar = $('<div>').addClass('button_bar');
          var button_close = $('<p>').addClass('button_close').text('X');
          button_close.click(close_window);
          button_close.appendTo(button_bar);
          button_bar.appendTo(window);
          $("<pre>").html(content).appendTo(window);
          $("#c_content").children("#cards").remove();
          });
    } else {
        console.log('window already exists');
    }
}

function showC(data){
    $("#c_content").value=data;
}

function creaDCForm(did){
    console.log('Hola, creaForm');
    $form = $("<form></form>");
    $form.append('<div class="row">');
    $form.append('<div class="span3 offset1">Datasource Name</div><div class="span3 offset1"><input type="text" name="ds_name" value="datasource name"></div>');
    $form.append('</div>');
    $form.append('<div class="row">');
    $form.append('<div class="span3 offset1">Script name</div><div class="span3 offset1"><input type="text" name="script_name" value="Script name"></div>');
    $form.append('</div>');
    $form.append('<div class="row">');
    $form.append('<div class="span9 offset1"><strong>Schedule:</strong></div>');
    $form.append('</div>');
    $form.append('<div class="row">');
    $form.append('<div class="span1 offset1">Minute</div><div class="span1">Hour</div><div class="span1">Day of Month</div><div class="span1">Month</div><div class="span1">Day of Week</div>');
    $form.append('</div>');
    $form.append('<div class="row">');
    $form.append('<input class="span1 offset1" type="text" name="min" value="*"><input class="span1" type="text" name="hour" value="*"><input class="span1" type="text" name="dom" value="*"><input class="span1" type="text" name="month" value="*"><input class="span1" type="text" name="dow" value="*">');
    $form.append('</div>');
    $form.append('<div class="row">');
    $form.append('<div class="span1 offset1"><input class="btn btn-primary" type="button" onClick="testResults(this.form,\''+did+'\')" value="update"></div>');
    $form.append('</div>');
    $('#c_content').replaceWith('<div class="span10" id="c_content"></div>');
    $('#c_content').append($form);
}


function updateAgent(aid){
    url='/etc/agent/'+aid
    ag_name=$('#ag_name').val();
    data={}
    if (ag_name==''){alert('Agent name can\'t be empty');}
    else{
        data['ag_name']=ag_name;
        $.ajax({
            url: url,
            type: 'PUT',
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(data) {
                    alert('Update successfull.');
                      }
        });
       }
   } 

function updateDatasource(did){
    url='/etc/ds/'+did
    ds_name=$('#ds_name').val();
    script=$('#script').val();
    minute=$('#minute').val();
    hour=$('#hour').val();
    day_of_week=$('#day_of_week').val();
    month=$('#month').val();
    day_of_month=$('#day_of_month').val();
    data={}
    if (ds_name==''){alert('Report name can\'t be empty');}
    else if (script==''){alert('Script name can\'t be empty');}
    else{
        data['ds_name']=ds_name;
        params={}
        params['script_name']=script;
        if (minute==''){params['min']='*';}else{params['min']=minute;}
        if (hour==''){params['hour']='*';}else{params['hour']=hour;}
        if (month==''){params['month']='*';}else{params['month']=month;}
        if (day_of_week==''){params['dow']='*';}else{params['dow']=day_of_week;}
        if (day_of_month==''){params['dom']='*';}else{params['dom']=day_of_month;}
        data['ds_params']=params;
        $.ajax({
            url: url,
            type: 'PUT',
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(data) {
                    alert('Update successfull.');
                      }
        });
       }
   } 

function newDatasource(aid){
    url='/etc/ds';
    ds_name=$('#ds_name').val();
    script=$('#script').val();
    minute=$('#minute').val();
    hour=$('#hour').val();
    day_of_week=$('#day_of_week').val();
    month=$('#month').val();
    day_of_month=$('#day_of_month').val();
    data={}
    data['aid']=aid;
    if (ds_name==''){alert('Report name can\'t be empty');}
    else if (script==''){alert('Script name can\'t be empty');}
    else{
        data['ds_name']=ds_name;
        data['ds_type']='script';
        params={}
        params['script_name']=script;
        if (minute==''){params['min']='*';}else{params['min']=minute;}
        if (hour==''){params['hour']='*';}else{params['hour']=hour;}
        if (month==''){params['month']='*';}else{params['month']=month;}
        if (day_of_week==''){params['dow']='*';}else{params['dow']=day_of_week;}
        if (day_of_month==''){params['dom']='*';}else{params['dom']=day_of_month;}
        data['ds_params']=params;
        $.ajax({
            url: url,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(data) {
                    alert('Report Created Successfully');
                      }
        });
       }
   } 

function main() {
    $("#c_content").on('dragover',drag_over);
    $("#c_content").on('dragenter',drag_enter);
    $("#c_content").on('drop',drop);
}

$(document).ready(main);
