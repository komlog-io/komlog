$('.pop').each(function () {
    var $elem = $(this);
    $elem.popover({
        container: $elem
    });
});

function multivariableBtnClick (e) {
        console.log('onclick del boton')
        e.preventDefault();
        var chartName= $(e.target).parent().parent().find('input').val()
        var thePopover = $(event.target).parent().parent().parent()
        $(event.target).parent().parent().css("display","none");
        //thePopover.popover('disable').popover('hide')
        //thePopover.remove();
        console.log('El valor del form es ',chartName,thePopover)
        //PubSub.publish('monitorDatapoint',data)
        PubSub.publish('newSlide',{type:'mp',widgetname:chartName})
}

$('#newMultivarBtn').on('click', function (e) {
        console.log('onclick del boton')
        e.preventDefault();
        var chartName= $(e.target).parent().find('input').val()
        console.log('El valor del form es ',chartName)
        //PubSub.publish('monitorDatapoint',data)
})

