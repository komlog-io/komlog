/* Funciones para controlar la web de komlog */

function getAC(id){ 
    url="/etc/agent/"+id;
    /*request=$.ajax({url:url,dataType: "json"}).done(function (data) { $("#ContentBox").html(data); });*/
    $("#ContentBox").load(url)
}

function getDC(id){ 
    url="/etc/ds/"+id;
    //request=$.ajax({url:url,dataType: "json"}).done(function (data) { $("#ContentBox").html(data); });
    $("#ContentBox").load(url)
}

function getDD(id){
    url="/var/ds/"+id
    $("#ContentBox").load(url)
}

function showC(data){
    $("#ContentBox").html(data);
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
    $('#ContentBox').replaceWith('<div class="span10" id="ContentBox"></div>');
    $('#ContentBox').append($form);
}

