komlogApp = angular.module('komlogApp',["ngResource"]);

angular.module('komlogApp')
.service('contentAreaServices', function($rootScope) {
    return {
        showWidget: function (id) {
            $rootScope.$broadcast("showWidgetEvent",{id:id});
        },
        hideWidget: function (id) {
            $rootScope.$broadcast("hideWidgetEvent",{id:id});
        }
    };
})
.service('dataServices', function($rootScope) {
    return {
        loadWidgetContents: function (id) {
            $rootScope.$broadcast("loadWidgetContentsEvent",{id:id});
        },
        loadDatapointData: function (id,init,end) {
            $rootScope.$broadcast("loadDatapointDataEvent",{id:id,init:init,end:end})
        }
    };
})
.constant('baseConfigUrl','http://localhost:8000/etc/')
.constant('baseDataUrl','http://localhost:8000/var/')
.controller('mainCtrl',function($scope,$http,$resource,baseConfigUrl,baseDataUrl,contentAreaServices,dataServices) {

    var datasourcesDataResource=$resource(baseDataUrl + "ds/:id",{id: "@did"})
    var datasourcesConfigResource=$resource(baseConfigUrl + "ds/:id",{id: "@did"})
    var datapointsConfigResource=$resource(baseConfigUrl + "dp/:id",{id: "@pid"})
    var widgetsConfigResource=$resource(baseConfigUrl + "wg/:id",{id: "@wid"})
    var dashboardsConfigResource=$resource(baseConfigUrl + "db/:id",{id: "@bid"})
    var agentsConfigResource=$resource(baseConfigUrl + "ag/:id",{id: "@aid"})

    var loadDatasourcesConfig = function () {
        $scope.ds_c=datasourcesConfigResource.query()
        .$promise.then(function(result) {$scope.ds_c=result})
    }

    var loadWidgetsConfig = function () {
        $scope.wg_c=widgetsConfigResource.query()
        .$promise.then(function(result) {$scope.wg_c=result})
    }

    var loadDashboardsConfig = function () {
        $scope.db_c=dashboardsConfigResource.query()
        .$promise.then(function(result) {$scope.db_c=result})
    }

    var loadAgentsConfig = function () {
        $scope.ag_c=agentsConfigResource.query()
        .$promise.then(function(result) {$scope.ag_c=result})
    }

    var updateDatasourceData = function (data) {
        var stored=false;
        for (var i=0;i<$scope.ds_d.length;i++){
            if ($scope.ds_d[i].did == data.did){
                 $scope.ds_d[i]=data
                 stored=true;
            }
        }
        if (stored==false){
            $scope.ds_d.push(data)
        }
    }

    var updateDatapointData = function (id,sd,ed) {
        var stored = false;
        params={}
        if (ed) {
            params.ed=ed;
        }
        if (sd) {
            params.sd=sd;
        }
        for (var i=0; i<$scope.dp_d.length;i++) {
            if ($scope.dp_d[i]['pid'] == id) {
                dp_obj=$scope.dp_d[i]
                dp_obj._last_updated=new Date()
                stored=true
                $http.get(dp_obj._baseUrl,{params:params}).success(function (data) {
                    for (var j=0;j<data.length;j++) {
                        dp_obj['data'][data[j].date]=data[j].value
                    }
                })
                break;
            }
        }
        if (stored == false) {
            new_dtp={pid:id,data:{},_baseUrl:baseDataUrl + 'dp/'+id}
            $http.get(new_dtp._baseUrl,{params:params}).success(function (data) {
                new_dtp._last_updated=new Date()
                for (var j=0;j<data.length;j++) {
                    new_dtp.data[data[j].date]=data[j].value
                }
                $scope.dp_d.push(new_dtp)
            })
        }
    }

    var updateDatapointConfig = function (id) {
        datapointsConfigResource.get({id:id})
        .$promise.then(function(data) {
            var stored=false;
            for (var i=0;i<$scope.dp_c.length;i++){
                if ($scope.dp_c[i].pid == data.pid){
                     $scope.dp_c[i]=data
                     stored=true;
                }
            }
            if (stored==false){
                $scope.dp_c.push(data)
            }
        })
    }

    var loadDatasourceWidgetContents = function (did) {
        datasourcesDataResource.get({id:did}).$promise.then( function (data) {
           updateDatasourceData(data);
           if (data.ds_dtps.length>0) {
               for (var i=0;i<data.ds_dtps.length;i++){
                   updateDatapointConfig(data.ds_dtps[i].pid)
                   updateDatapointData(data.ds_dtps[i].pid)
                   }
               }
           })
        datasourcesConfigResource.get({id:did})
    }

    var loadDatapointWidgetContents = function (pid) {
           updateDatapointConfig(pid)
           updateDatapointData(pid)
    }

    $scope.$on('loadWidgetContentsEvent', function (event, args) {
            for (var i=0;i<$scope.wg_c.length;i++) {
                if ($scope.wg_c[i].wid == args.id) {
                    if ($scope.wg_c[i].type == 'ds') {
                        loadDatasourceWidgetContents($scope.wg_c[i].did)
                    }
                    if ($scope.wg_c[i].type == 'dp') {
                        loadDatapointWidgetContents($scope.wg_c[i].pid)
                    }
                }
            }
        });

    $scope.$on('loadDatapointDataEvent', function (event, args) {
        updateDatapointData(id=args.id,sd=args.init,ed=args.end);
        });

    $scope.ds_d=[]
    $scope.dp_d=[]
    $scope.dp_c=[]
    $scope.db_c=[{bid:'0',name:'Home',wids:[]}]

    $scope.showWidget = function (id) {
        contentAreaServices.showWidget(id)
        dataServices.loadWidgetContents(id);
    }

    loadDatasourcesConfig();
    loadAgentsConfig();
    loadWidgetsConfig();

});

angular.module('komlogApp')
.constant('leftMenuHiddenClass','left-menu-hidden')
.constant('leftMenuShowClass','left-menu-show')
.controller('leftMenuCtrl', function($scope,leftMenuHiddenClass,leftMenuShowClass) {

    var leftMenuHidden = false;

    $scope.toggleHidden = function () {
        leftMenuHidden = !leftMenuHidden;
    };

    $scope.getMenuClass = function () {
        return leftMenuHidden ? leftMenuHiddenClass : leftMenuShowClass
    };

});

angular.module('komlogApp')
.controller('contentAreaCtrl', function ($scope, contentAreaServices,dataServices) {

    $scope.currentDashboard ='0';
    $scope.wg_lc=[];

    $scope.$on('showWidgetEvent', function (event, args) {
        for (var i=0; i<$scope.db_c.length;i++) {
            if ($scope.db_c[i].bid == $scope.currentDashboard) {
                for (var j=0; j<$scope.db_c[i].wids.length;j++) {
                    if ($scope.db_c[i].wids[j] == args.id) {
                        return;
                    }
                }
                $scope.db_c[i].wids.push(args.id);
                return;
            }
        }
    });

    $scope.$on('hideWidgetEvent', function (event, args) {
        for (var i=0;i<$scope.db_c.length;i++) {
            if ($scope.db_c[i].bid == $scope.currentDashboard) {
                for (var j=0; j<$scope.db_c[i].wids.length; j++) {
                    if ($scope.db_c[i].wids[j] == args.id) {
                        $scope.db_c[i].wids.splice(j,1);
                    }
                }
            }
        };
    });
    
    $scope.hideWidget = function (id) {
        contentAreaServices.hideWidget(id);
    }

    $scope.requestWidgetData = function (wid) {
        for (var i=0;i<$scope.wg_lc.length;i++) {
            if ($scope.wg_lc[i].wid==wid && $scope.wg_lc[i].bid==$scope.currentDashboard) {
                init=$scope.wg_lc[i].interval_init
                end=$scope.wg_lc[i].interval_end
                for (var j=0;j<$scope.wg_lc[i].vars.length;j++) {
                    pid=$scope.wg_lc[i].vars[j];
                    dataServices.loadDatapointData(pid,init,end);
                }
            }
        }
    }

})
.directive("wdsContent", function ($compile) {
    function link(scope,element,attrs) {

        var ds_content=[];
        var formatNumber = d3.format(",");

        var labelSubstringStartingAtOfLength = function (string,index,length) {
            prefix=string.substr(0,index);
            stringtochange='<div id='+index+'>'+formatNumber(string.substr(index,length))+'</div>';
            sufix=string.substr(index+length,string.length);
            result=prefix+stringtochange+sufix;
            return result;
        }

        var updateElementContent = function () {
            var e_content=ds_content.ds_content
            var dtps=ds_content.ds_dtps
            for (var i=ds_content.ds_vars.length; i>0; i--) {
                e_content=labelSubstringStartingAtOfLength(e_content,ds_content.ds_vars[i-1][0],ds_content.ds_vars[i-1][1]);
            }
            element.html(e_content);
            vars=element.children();
            for (var i=0;i<vars.length;i++) {
                vars.eq(i).css("font-weight", "bold");
                id=vars.eq(i).prop('id')
                if (id!=null){
                    monitored_var=null
                    for (var j=0;j<dtps.length;j++) {
                        if (dtps[j].id==id) {
                            monitored_var=angular.element('<div>')
                                    .addClass('monitored-var')
                                    .attr('pid',dtps[j].pid)
                                    .attr('id',id).text(vars.eq(i).text());
                            vars.eq(i).replaceWith($compile(monitored_var)(scope))
                            dtps.splice(j,1);
                        }
                    }
                    if (monitored_var==null){
                        detected_var=angular.element('<div>')
                                    .addClass('detected-var')
                                    .text(vars.eq(i).text())
                                    .attr('id',id)
                                    .attr('date',ds_content.ds_date)
                        vars.eq(i).replaceWith($compile(detected_var)(scope))
                    }
                }
            }
        }

        for (var i=0; i<scope.ds_d.length;i++) {
            if (scope.ds_d[i].did == attrs["wdsContent"]) {
                ds_content=scope.ds_d[i];
                scope.$watch(scope.ds_d[i],function (newValue,oldValue) {
                    updateElementContent()
                });
                break;
            }
        }
    } 

    return {
        link: link
    };
})
.directive("detectedVar", function () {
    function link(scope,element,attrs) {
        element.bind('click',function() {
            });
    }
    return {
        restrict: 'C',
        link: link
    };
})
.directive("monitoredVar", function () {
    function link(scope,element,attrs) {
        for (var i=0; i<scope.wg_c.length;i++) {
            if (scope.wg_c[i].type=='dp') {
                if (scope.wg_c[i].pid==element.attr('pid')) {
                    wid=scope.wg_c[i].wid;
                    element.bind('click',function() {
                        scope.showWidget(wid)
                    });
                }
            }
        }
    }
    return {
        restrict: 'C',
        link: link
    };
})
.directive('draggable', ['$document', function($document) {
    return function(scope, element, attr) {
      var startX = 0, startY = 0, x = 0, y = 0;

      angular.element(element.children()[0]).on('mousedown', function(event) {
        event.preventDefault();
        startX = event.pageX;
        startY = event.pageY;
        elementY = parseInt(element.css('top'))|null;
        elementX = parseInt(element.css('left'))|null;
        element.css({
            position: 'absolute',
            top: elementY+'px',
            left: elementX+'px'
        })
        $document.on('mousemove', mousemove);
        $document.on('mouseup', mouseup);
      });

      function mousemove(event) {
        endY = event.pageY;
        endX = event.pageX;
        element.css({
          top: elementY+(endY-startY) + 'px',
          left:  elementX+(endX-startX) + 'px'
        });
      }

      function mouseup() {
        $document.off('mousemove', mousemove);
        $document.off('mouseup', mouseup);
      }
    };
}])
.directive("wdpContent", function ($compile) {
    function link(scope,element,attrs) {

        var wid=attrs['wid']
        var my_wg_lc=null;
        var my_dp_d=[];
        var formatNumber = d3.format(",.1f");
        var max_value = null;
        var min_value = null;
        var avg_value = 0;


        var initializeWdpContent = function () {
            
            for (var i=0;i<scope.wg_lc.length;i++) {
                if (scope.wg_lc[i].wid==wid && scope.wg_lc[i].bid==scope.currentDashboard) {
                    my_wg_lc=scope.wg_lc[i]
                }
            }

            if (my_wg_lc === null) {

                scope.wg_lc.push({wid:wid,bid:scope.currentDashboard,interval_init:null,interval_end:null,vars:[]})

                for (var i=0;i<scope.wg_lc.length;i++) {
                    if (scope.wg_lc[i].wid==wid && scope.wg_lc[i].bid==scope.currentDashboard) {
                        my_wg_lc=scope.wg_lc[i]
                    }
                }

                for (var i=0;i<scope.wg_c.length;i++) {
                    if (scope.wg_c[i].wid == wid) {
                        my_wg_lc.vars.push(scope.wg_c[i].pid)
                    }
                }

                for (var i=0;i<scope.dp_d.length;i++){
                    if (scope.dp_d[i].pid==my_wg_lc.vars[0]) {
                        for (var j in scope.dp_d[i].data) {
                            my_dp_d.push({date:new Date(j),value:scope.dp_d[i].data[j]})
                        }
                    }
                }

                my_wg_lc.interval_init=d3.min(my_dp_d, function(d) {return d.date.toISOString()}) 
                my_wg_lc.interval_end=d3.max(my_dp_d, function(d) {return d.date.toISOString()}) 
            }
        }

        var updateWdpContent = function () {
            my_dp_d = [];
            max_value = null;
            min_value = null;
            avg_value = 0;

            for (var i=0;i<scope.dp_d.length;i++){
                if (scope.dp_d[i].pid==my_wg_lc.vars[0]) {
                    for (var j in scope.dp_d[i].data) {
                        d_date=new Date(j)
                        if ((d_date>=new Date(my_wg_lc.interval_init)) && (d_date<=new Date(my_wg_lc.interval_end))) {
                            my_dp_d.push({date:d_date,value:scope.dp_d[i].data[j]})
                        }
                    }
                }
            }
                
            my_dp_d.forEach( function (d) {
                    tmp_value=parseFloat(d.value);
                    if ((min_value==null) && (max_value==null)) {
                        min_value=tmp_value;
                        max_value=tmp_value;
                    }
                    if (tmp_value>max_value) {
                        max_value=tmp_value;
                    }
                    else if (tmp_value<min_value) {
                        min_value=tmp_value;
                    }
                    avg_value=avg_value+tmp_value;
            })
            avg_value=avg_value/my_dp_d.length;
        }

        var showWdpContent = function () {
            
            table_html='<table><tr><td><strong>From:</strong></td><td>'+new Date(my_wg_lc.interval_init).toString()+'</td>'+
                  '<th>Max value</th><th>Min value</th><th>Avg value</th><th>Num values</th></tr>'+
                  '<tr><td><strong>To:</strong></td><td>'+new Date(my_wg_lc.interval_end).toString()+'</td>'+
                  '<td>'+formatNumber(max_value)+'</td><td>'+formatNumber(min_value)+'</td><td>'+formatNumber(avg_value)+'</td><td>'+formatNumber(my_dp_d.length)+'</td></tr></table>'

            var table = angular.element(table_html)
            var histogram = angular.element('<histogram>')
                             .attr('wid',wid)
            var timeline = angular.element('<timeline>')
                             .attr('wid',wid)
            
            items = element.children()
            if (items.length>0) {
                for (var i=0;i<items.length;i++) {
                    if (i==0) {
                        old_table=items.eq(i).children().eq(0)
                        old_table.replaceWith(table)
                    }
                    else if (i==1) {
                        items.eq(i).replaceWith($compile(histogram)(scope))
                    }
                    else if (i==2) {
                        items.eq(i).replaceWith($compile(timeline)(scope))
                    }
                }
            }
            else {
                var dateslider = angular.element('<date-slider>')
                                 .attr('wid',wid)
                new_div=angular.element('<div>');
                new_div.append(table);
                new_div.append($compile(dateslider)(scope))
                element.append(new_div)
                element.append($compile(histogram)(scope))
                element.append($compile(timeline)(scope))
            }

        }

        initializeWdpContent();

        scope.$watchGroup([function () {
            return my_wg_lc.interval_init
        }, function () {
            return my_wg_lc.interval_end
        }], function(newValue,oldValue) {
            updateWdpContent()
            showWdpContent()
        });

    }

    return {
        link: link
    };
})
.directive("histogram", function ($compile) {
    function link(scope,element,attrs) {

        var wid=attrs['wid'];
        var pid=null;
        var hg_data=[];

        for (var i=0;i<scope.wg_lc.length;i++) {
            if (scope.wg_lc[i].wid == wid) {
                my_wg_lc=scope.wg_lc[i]
            }
        }
        if (my_wg_lc!=null) {
            if (my_wg_lc.vars.length==1) {
                pid=my_wg_lc.vars[0]
            }
            else {
                return;
            }
        } 
        else {
            return;
        }

        for (var i=0;i<scope.dp_d.length;i++) {
            if (scope.dp_d[i].pid == pid) {
                for (var s_date in scope.dp_d[i].data) {
                    date=new Date(s_date)
                    if ((date >= new Date(my_wg_lc.interval_init)) &&
                        (date <= new Date(my_wg_lc.interval_end))) {
                        hg_data.push(scope.dp_d[i].data[s_date])
                    }
                }
            }
        }

        var formatCount = d3.format(",.0f");
        var formatPercent = d3.format(",.1f");
        var margin = {top: 20, right: 30, bottom: 40, left: 30},
            width = 610 - margin.left - margin.right,
            height = 230 - margin.top - margin.bottom;

        var x = d3.scale.linear()
            .range([0, width])
            .domain(d3.extent(hg_data))

        var data = d3.layout.histogram()
            .bins(x.ticks(10))
            (hg_data);

        var y = d3.scale.linear()
            .domain([0, d3.max(data, function(d) { return d.y; })])
            .range([height, 0]);


        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var svg = d3.select(element[0]).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var bar = svg.selectAll(".bar")
            .data(data)
            .enter().append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

        bar.append("rect")
            .attr("x", 1)
            .attr("width", width/(data.length+1)-1)
            .attr("height", function(d) { return height - y(d.y); });

        bar.append("text")
            .attr("dy", ".75em")
            .attr("y", 5)
            .attr("x", width/(data.length*2))
            .attr("text-anchor", "middle")
            .text(function(d) { return formatCount(d.y)});

        bar.append("text")
            .attr("dy", ".75em")
            .attr("y", -10)
            .attr("x", width/(data.length*2))
            .attr("text-anchor", "middle")
            .text(function(d) { return formatPercent(d.y/hg_data.length*100)+'%'});

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                 return "rotate(-25)" 
            });
   
    }

    return {
        restrict: 'E',
        link: link
    };
})
.directive("timeline", function () {
    function link(scope,element,attrs) {

        var wid=attrs['wid'];
        var pids=[];
        var tl_data=[];
        var my_wg_lc=null;

        for (var i=0;i<scope.wg_lc.length;i++) {
            if (scope.wg_lc[i].wid == wid) {
                my_wg_lc=scope.wg_lc[i]
            }
        }
        if (my_wg_lc!=null) {
             my_wg_lc.vars.forEach (function(d) {
                pids.push(d)
            })
        }
        else {
            return;
        }

        for (var i=0;i<scope.dp_d.length;i++) {
            for (var j=0;j<pids.length;j++) {
                if (scope.dp_d[i].pid == pids[j]) {
                    data=[]
                    for (var k in scope.dp_d[i].data) {
                        date=new Date(k)
                        if (new Date(my_wg_lc.interval_init)<=date && new Date(my_wg_lc.interval_end)>=date) {
                            data.push({date:date,value:scope.dp_d[i].data[k]})
                        }
                    }
                    tl_data.push({pid:pids[j],data:data})
                }
            }
        }

        if (tl_data) {
            y_values_array=[]
            for (var i=0; i<tl_data.length;i++) {
                y_values_array.push(d3.min(tl_data[i].data, function(d) { return d.value; }))
                y_values_array.push(d3.max(tl_data[i].data, function(d) { return d.value; }))
            }


            var formatCount = d3.format(",.0f");
            var formatPercent = d3.format(",.1f");
            var customTimeFormat = d3.time.format.multi([
              [".%L", function(d) { return d.getMilliseconds(); }],
              [":%S", function(d) { return d.getSeconds(); }],
              ["%I:%M", function(d) { return d.getMinutes(); }],
              ["%I %p", function(d) { return d.getHours(); }],
              ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
              ["%b %d", function(d) { return d.getDate() != 1; }],
              ["%B", function(d) { return d.getMonth(); }],
              ["%Y", function() { return true; }]
              ]);

            var margin = {top: 20, right: 30, bottom: 40, left: 70},
                width = 610 - margin.left - margin.right,
                height = 230 - margin.top - margin.bottom;

            var x = d3.time.scale()
                .range([0, width])
                .domain([new Date(my_wg_lc.interval_init),new Date(my_wg_lc.interval_end)])

            var y = d3.scale.linear()
                .domain(d3.extent(y_values_array))
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .ticks(7)
                .tickFormat(customTimeFormat);

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left").ticks(8);


            var svg = d3.select(element[0]).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var line = d3.svg.line()
                       .x(function (d) {return x(d.date)})
                       .y(function (d) {return y(d.value)});
            
            for (var i=0; i<tl_data.length; i++) {
                svg.append('path')
                .attr('class','line')
                .attr('d',line(tl_data[i].data));
            }

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);
        
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);
        }
    }

    return {
        restrict: 'E',
        link: link
    };
})
.directive('dateSlider', function () {
    function link(scope,element,attrs) {
        var wid=attrs['wid']
        var my_wg_lc=null;
        var my_dp_c=[];
        var slider_date_init=null;
        var slider_date_end=null;
        var slider_date_min=null;
        var slider_date_max=null;
        var margin = {top: 15, right: 50, bottom: 25, left: 50},
            width = 610 - margin.left - margin.right,
            height = 50 - margin.top - margin.bottom;
        var customTimeFormat = d3.time.format.multi([
          [".%L", function(d) { return d.getMilliseconds(); }],
          [":%S", function(d) { return d.getSeconds(); }],
          ["%I:%M", function(d) { return d.getMinutes(); }],
          ["%I %p", function(d) { return d.getHours(); }],
          ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
          ["%b %d", function(d) { return d.getDate() != 1; }],
          ["%B", function(d) { return d.getMonth(); }],
          ["%Y", function() { return true; }]
          ]);

        var brushstart = function () {
          svg.classed("selecting", true);
        }

        var brushmove = function () {
          my_wg_lc.interval_init=brush.extent()[0].toISOString()
          my_wg_lc.interval_end=brush.extent()[1].toISOString()
          scope.$apply()
        }


        var brushend = function () {
          svg.classed("selecting", !d3.event.target.empty());
          my_wg_lc.interval_init=brush.extent()[0].toISOString()
          my_wg_lc.interval_end=brush.extent()[1].toISOString()
          scope.requestWidgetData(wid);
        }

        for (var i=0;i<scope.wg_lc.length;i++) {
            if (scope.wg_lc[i].wid==wid && scope.wg_lc[i].bid==scope.currentDashboard) {
                my_wg_lc=scope.wg_lc[i]
            }
        }

        if (my_wg_lc!=null) {
            for (var i=0;i<my_wg_lc.vars.length;i++) {
                for (var j=0;j<scope.dp_c.length;j++) {
                    if (scope.dp_c[j].pid == my_wg_lc.vars[i]) {
                        my_dp_c.push(scope.dp_c[j].pid)
                    }
                }
            }
            if (my_dp_c.length>0) {
                for (var i=0;i<my_dp_c.length;i++) {
                    if (slider_date_min==null) {
                        if (my_dp_c[i].hasOwnProperty('oldest_detected')) {
                            slider_date_min=new Date(my_dp_c[i].oldest_detected)
                        } else {
                            slider_date_min=new Date(my_wg_lc.interval_init)
                            slider_date_min.setDate(slider_date_min.getDate()-5)
                        }
                        if (my_dp_c[i].hasOwnProperty('newest_detected')) {
                            slider_date_max=new Date(my_dp_c[i].newest_detected)
                        } else {
                            slider_date_max=new Date()
                        }
                    }
                    else {
                        if (my_dp_c[i].hasOwnProperty('oldest_detected')) {
                            dp_date_min=new Date(my_dp_c[i].oldest_detected)
                        } else {
                            dp_date_min=new Date(my_wg_lc.interval_init)
                            dp_date_min.setDate(slider_date_min.getDate()-5)
                        }
                        slider_date_min=(dp_date_min < slider_date_min) ? dp_date_min:slider_date_min
                        if (my_dp_c[i].hasOwnProperty('newest_detected')) {
                            dp_date_max=new Date(my_dp_c[i].newest_detected)
                        } else {
                            dp_date_max=new Date()
                        }
                        slider_date_max=(dp_date_max > slider_date_max) ? dp_date_max:slider_date_max
                    }
                }
            }
        }
        else {
            return;
        }

        interval_ms_duration=Math.abs(new Date(my_wg_lc.interval_end).getTime() - new Date(my_wg_lc.interval_init).getTime())
        slider_date_init=new Date().setTime(new Date(my_wg_lc.interval_init).getTime()-3*interval_ms_duration)
        slider_date_end=new Date().setTime(new Date(my_wg_lc.interval_end).getTime()+3*interval_ms_duration)
        slider_date_init=(slider_date_init<slider_date_min)?slider_date_min:slider_date_init;
        slider_date_end=(slider_date_end>slider_date_max)?slider_date_max:slider_date_end;
        
        var x = d3.time.scale()
            .range([0, width])
            .domain([slider_date_init,slider_date_end])

        var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .tickFormat(customTimeFormat)
                    .ticks(8);

        var y = d3.random.normal(height / 2, height / 8);

        var brush = d3.svg.brush()
            .x(x)
            .extent([new Date(my_wg_lc.interval_init),new Date(my_wg_lc.interval_end)])
            .on("brushstart", brushstart)
            .on("brush", brushmove)
            .on("brushend", brushend);

        var arc = d3.svg.arc()
            .outerRadius(height / 2)
            .startAngle(0)
            .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });

        var svg = d3.select(element[0]).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        var brushg = svg.append("g")
            .attr("class", "brush")
            .call(brush);

        brushg.selectAll(".resize").append("path")
            .attr("transform", "translate(0," +  height / 2 + ")")
            .attr("d", arc);

        brushg.selectAll("rect")
            .attr("height", height);

        brushstart();

        
    }

    return {
        restrict: 'E',
        link: link
    }
});
