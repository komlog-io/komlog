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
    //$("#ContentBox").load(url)
    $.getJSON(url,function(data){
        content=prepareDSContent(data)
        doc=$("<h3/>").html(title)
        $("#ContentBox").empty()
        $("<pre/>").html(content).appendTo(doc)
        $("<div/>").html(doc).appendTo("#ContentBox")}
        )
}

function showC(data){
    $("#ContentBox").value=data;
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

