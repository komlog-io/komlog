
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
    var finalcontent=data.ds_content;
    var vararray=data.ds_vars;
    for (var i = vararray.length; i>0; i--){
        finalcontent=labelSubstringStartingAtOfLength(finalcontent,vararray[i-1][0],vararray[i-1][1]);
    }
    data.ds_content=finalcontent;
    return data;
}

function createGraph(id,data) {
    var wid = 'a'+id;
    var width = 750, height = 300;
    var domainX = d3.extent(data, function(datum) {
        return datum.timestamp;
         });
    var domainY = d3.extent(data, function(datum) {
        return datum.value;
        });
    var rangeX = [50, width], rangeY = [height-50, 0]; //los 30 son los margenes que vamos a dejar para colocar ejes, etc
    var scaleX = d3.time.scale().domain(domainX).range(rangeX);
    var scaleY = d3.scale.linear().domain(domainY).range(rangeY);
    var axisX =  d3.svg.axis().scale(scaleX);
    var axisY =  d3.svg.axis().scale(scaleY).orient('left');
    var line = d3.svg.line().x(function(datum) {
        return scaleX(datum.timestamp);
        }).y(function(datum) {
            return scaleY(datum.value);
        });
    console.log('Vamos a seleccionar la ventana del grafico');
    var svg = d3.select('#'+wid).append('svg').attr('width', width).attr('height', height);
    svg.append('g').attr('class','x axis').attr('transform','translate(0,'+(height-50)+')').call(axisX);
    svg.append('g').attr('class','y axis').attr('transform','translate(50,0)').call(axisY);
    console.log('svg creado');
    var path = svg.append('path').datum(data).attr('class', 'line').attr('d', line).style('fill', 'none').style('stroke', '#FB5050').style('stroke-width', '2px');
    console.log('Esto ha terminado');
}

function getGR(id,title) {
    console.log('Empieza getGR');
    url="/etc/graph/"+id
    var wid = 'a'+id;
    var obj = $(wid+'.c_window');
    console.log(obj.attr('id'));
    if (obj.attr('id') === undefined) {
      $.getJSON(url,function(data){
          console.log(data.datapoints);
          console.log('creamos ventana');
          var window = $("<div>").addClass("c_window");
          window.attr('id',wid);
          window.appendTo("#c_content");
          var window_title = $("<h3>").html(title).attr("draggable","true");
          window_title.on('dragstart',drag_start);
          window_title.appendTo(window);
          var button_bar = $('<div>').addClass('button_bar');
          var button_close = $('<p>').addClass('button_close').text('X');
          button_close.click(close_window);
          button_close.appendTo(button_bar);
          button_bar.appendTo(window);
          for (var key in data.datapoints) {
            var dtp_url='/var/dp/'+key;
            $.getJSON(dtp_url, function(data2) {
                var dtp_data=[];
                for (var i=0;i<data2.length;i++) {
                    dtp_data.push({
                        timestamp: new Date(data2[i][0]),
                        value: data2[i][1]
                    });
                }
                createGraph(id,dtp_data);
            });
          }
          $("#c_content").children("#cards").remove();
          });
    } else {
        console.log('window already exists');
    }
}

function getDD(id,title){
    url="/var/ds/"+id
    var wid = 'a'+id;
    var obj = $('#'+wid+'.c_window');
    console.log(obj.attr('id'));
    if (obj.attr('id') === undefined) {
      $.getJSON(url,function(data){
          content=prepareDSContent(data);
          var window = $("<div>").addClass("c_window");
          window.attr('id',wid);
          window.appendTo("#c_content")
          var window_title = $("<h3>").html(title).attr("draggable","true");
          window_title.on('dragstart',drag_start);
          window_title.appendTo(window);
          var button_bar = $('<div>').addClass('button_bar');
          var button_close = $('<p>').addClass('button_close').text('X');
          button_close.click(close_window);
          button_close.appendTo(button_bar);
          button_bar.appendTo(window);
          $("<pre>").html(content.ds_content).appendTo(window);
          if (content.ds_graphs) {
              var graphs = $('<div>').addClass('c_graphs');
              $('<h4>').text('Related Graphs').appendTo(graphs);
              graph_list = $('<ul>');
              $.each(content.ds_graphs, function (index,value) {
                  $('<a>').text(value[1]).attr('href','#').click(function() {
                      getGR(value[0],value[1]);
                  }).appendTo($('<li>').appendTo(graph_list));
              });
              graph_list.appendTo(graphs);
              graphs.appendTo(window);
          }
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
