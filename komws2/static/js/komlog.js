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
        }
    };
})
.constant('baseConfigUrl','http://localhost:8000/etc/')
.constant('baseDataUrl','http://localhost:8000/var/')
.controller('mainCtrl',function($scope,$resource,baseConfigUrl,baseDataUrl,contentAreaServices,dataServices) {

    var datasourcesDataResource=$resource(baseDataUrl + "ds/:id",{id: "@did"})
    var datasourcesConfigResource=$resource(baseConfigUrl + "ds/:id",{id: "@did"})
    var datapointsDataResource=$resource(baseDataUrl + "dp/:id",{id: "@pid"})
    var datapointsConfigResource=$resource(baseConfigUrl + "dp/:id",{id: "@pid"})
    var widgetsConfigResource=$resource(baseConfigUrl + "wg/:id",{id: "@wid"})
    var dashboardsConfigResource=$resource(baseConfigUrl + "db/:id",{id: "@bid"})
    var agentsConfigResource=$resource(baseConfigUrl + "ag/:id",{id: "@aid"})

    var loadDatasourcesConfig = function (id) {
        if (id==null) {
            $scope.ds_c=datasourcesConfigResource.query().$promise.then(function(result) {$scope.ds_c=result})
        } else {
            datasourcesConfigResource.get({id:id}).$promise.then(function () {
                console.log($scope.ds_c)
                })
        }
    }

    var loadDatasourceData = function (id) {
        datasourcesDataResource.get({id:id}).$promise.then(function(value) {
            console.log($scope.ds_d)
            for (var i=0;i<$scope.ds_d.length;i++){
                if ($scope.ds_d[i].did == value.did){
                    $scope.ds_d[i]=value
                    return
                }
            }
            $scope.ds_d.push(value)
        })
    }

    var loadDatapointConfig = function (id) {
        datapointsConfigResource.get({id:id})
    }

    var loadDatapointData = function (id) {
        datapointsDataResource.get({id:id})
    }


    var loadWidgetsConfig = function () {
        $scope.wg_c=widgetsConfigResource.query().$promise.then(function(result) {$scope.wg_c=result})
    }

    var loadDashboardsConfig = function () {
        $scope.db_c=dashboardsConfigResource.query().$promise.then(function(result) {$scope.db_c=result})
    }

    var loadAgentsConfig = function () {
        $scope.ag_c=agentsConfigResource.query().$promise.then(function(result) {$scope.ag_c=result})
    }

    $scope.$on('loadWidgetContentsEvent', function (event, args) {
            console.log('loading widget content');
            for (var i=0;i<$scope.wg_c.length;i++) {
                if ($scope.wg_c[i].wid == args.id) {
                    if ($scope.wg_c[i].type == 'ds') {
                        loadDatasourcesConfig($scope.wg_c[i].did)
                        loadDatasourceData($scope.wg_c[i].did)
                    }
                }
            }
        });

    $scope.$on('loadDatapointEvent', function (event, args) {
            loadDatapointConfig(args.id);
            loadDatapointData(args.id);
        });

    $scope.ds_d=[]
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

})
.directive("dsContent", function () {
    function link(scope,element,attrs) {

        var ds_content=[];

        var labelSubstringStartingAtOfLength = function (string,index,length) {
            prefix=string.substr(0,index);
            stringtochange='<div class="label label-default" id='+index+'>'+string.substr(index,length)+'</div>';
            sufix=string.substr(index+length,string.length);
            result=prefix+stringtochange+sufix;
            return result;
        }

        var updateElementContent = function () {
            console.log('updating Element Content')
            console.log(ds_content)
            console.log(ds_content.ds_vars.length)
            var e_content=ds_content.ds_content
            for (var i=ds_content.ds_vars.length; i>0; i--) {
                e_content=labelSubstringStartingAtOfLength(e_content,ds_content.ds_vars[i-1][0],ds_content.ds_vars[i-1][1]);
            }
            console.log('setting html content')
            element.html(e_content);
        }

        for (var i=0; i<scope.ds_d.length;i++) {
            if (scope.ds_d[i].did == attrs["dsContent"]) {
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
.directive("dsDate", function () {
    function link(scope,element,attrs) {

        ds_date = [];
        for (var i=0; i<scope.ds_d.length;i++) {
            if (scope.ds_d[i].did == attrs["dsDate"]) {
                ds_date=scope.ds_d[i].ds_date;
                break;
            }
        }
        if (ds_date) {
            element.html(new Date(ds_date).toString());
        }
    }

    return {
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
}]);

