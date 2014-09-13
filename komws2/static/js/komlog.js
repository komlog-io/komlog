komlogApp = angular.module('komlogApp',[]);

angular.module('komlogApp')
.service('contentAreaServices', function($rootScope) {
    return {
        showContent: function (id) {
            $rootScope.$broadcast("showContentEvent",{id:id});
        },
        hideContent: function (id) {
            $rootScope.$broadcast("hideContentEvent",{id:id});
        }
    };
})
.controller('mainCtrl',function($scope,contentAreaServices) {

    $scope.ds_d=[{did:'1',ds_content:'Datasource 1 oeo',ds_vars:[[11,1]],ds_date:'2014-02-13T20:25:01.048000'},
                  {did:'2',ds_content:'Datasource 2 oeo',ds_vars:[[11,1]]},
                  {did:'3',ds_content:'Datasource 3 oeo',ds_vars:[[11,1]]},
                  {did:'4',ds_content:'Datasource 4 oeo',ds_vars:[[11,1]]},
                  {did:'5',ds_content:'Datasource 5 oeo',ds_vars:[[11,1]]},
                  {did:'6',ds_content:'Datasource 6 oeo',ds_vars:[[11,1]]},
                  {did:'7',ds_content:'Datasource 7 oeo',ds_vars:[[11,1]]},
                  {did:'8',ds_content:'Datasource 8 oeo',ds_vars:[[11,1]]},
                  {did:'9',ds_content:'Datasource 9 oeo',ds_vars:[[11,1]]},
                  {did:'10',ds_content:'Datasource 10 oeo',ds_vars:[[11,2]]},
                  {did:'11',ds_content:'Datasource 11 oeo',ds_vars:[[11,2]]},
                  {did:'12',ds_content:'Datasource 12 oeo',ds_vars:[[11,2]]},
                  {did:'13',ds_content:'Datasource 13 oeo',ds_vars:[[11,2]]}];

    $scope.ds_c=[{did:'1',aid:'1',name:'Datasource 1'},
                {did:'2',aid:'1',name:'Datasource 2'},
                {did:'3',aid:'1',name:'Datasource 3'},
                {did:'4',aid:'1',name:'Datasource 4'},
                {did:'5',aid:'2',name:'Datasource 5'},
                {did:'6',aid:'2',name:'Datasource 6'},
                {did:'8',aid:'1',name:'Datasource 8'},
                {did:'9',aid:'2',name:'Datasource 9'},
                {did:'7',aid:'1',name:'Datasource 7'},
                {did:'10',aid:'3',name:'Datasource 10'},
                {did:'12',aid:'3',name:'Datasource 12'},
                {did:'13',aid:'3',name:'Datasource 13'}];

    $scope.agents=[{aid:'1',name:'Agent #1'},
                   {aid:'2',name:'Agent #2'},
                   {aid:'3',name:'Agent #3'}];

    $scope.widgets=[{wid:'1',type:'ds',did:'1'},
                    {wid:'2',type:'ds',did:'2'},
                    {wid:'3',type:'ds',did:'3'},
                    {wid:'4',type:'ds',did:'4'},
                    {wid:'5',type:'ds',did:'5'},
                    {wid:'6',type:'ds',did:'6'},
                    {wid:'7',type:'ds',did:'7'},
                    {wid:'8',type:'ds',did:'8'},
                    {wid:'9',type:'ds',did:'9'},
                    {wid:'10',type:'ds',did:'10'},
                    {wid:'11',type:'ds',did:'11'},
                    {wid:'12',type:'ds',did:'12'},
                    {wid:'13',type:'ds',did:'13'}];
    
    $scope.dashboards=[{bid:'0',name:'Home',wid_list:[]},
                       {bid:'1',name:'Dashboard 1',wid_list:['1','2','3','4','5','6']},
                       {bid:'2',name:'Dashboard 2',wid_list:['2','5','8','10','12','3']}, 
                       {bid:'3',name:'Dashboard 3',wid_list:['2','5','8','10','12','3']}, 
                       {bid:'4',name:'Dashboard 4',wid_list:['2','5','8','10','12','3']}] 

    $scope.loadWidget = function (id) {
        contentAreaServices.showContent(id);
    }

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
.controller('contentAreaCtrl', function ($scope, contentAreaServices) {

    $scope.currentDashboard ='0';

    $scope.$on('showContentEvent', function (event, args) {
        for (var i=0; i<$scope.dashboards.length;i++) {
            if ($scope.dashboards[i].bid == $scope.currentDashboard) {
                for (var j=0; j<$scope.dashboards[i].wid_list.length;j++) {
                    if ($scope.dashboards[i].wid_list[j] == args.id) {
                        return;
                    }
                }
                $scope.dashboards[i].wid_list.push(args.id);
                return;
            }
        }
    });

    $scope.$on('hideContentEvent', function (event, args) {
        for (var i=0;i<$scope.dashboards.length;i++) {
            if ($scope.dashboards[i].bid == $scope.currentDashboard) {
                for (var j=0; j<$scope.dashboards[i].wid_list.length; j++) {
                    if ($scope.dashboards[i].wid_list[j] == args.id) {
                        $scope.dashboards[i].wid_list.splice(j,1);
                    }
                }
            }
        };
    });
    
    $scope.closeWidget = function (id) {
        contentAreaServices.hideContent(id);
    }

})
.directive("dsContent", function () {
    function link(scope,element,attrs) {

        var labelSubstringStartingAtOfLength = function (string,index,length) {
            prefix=string.substr(0,index);
            stringtochange='<div class="label label-default" id='+index+'>'+string.substr(index,length)+'</div>';
            sufix=string.substr(index+length,string.length);
            result=prefix+stringtochange+sufix;
            return result;
        }
        var ds_content, ds_vars = [];

        for (var i=0; i<scope.ds_d.length;i++) {
            if (scope.ds_d[i].did == attrs["dsContent"]) {
                ds_content=scope.ds_d[i].ds_content;
                ds_vars=scope.ds_d[i].ds_vars;
                break;
            }
        }
        for (var i=ds_vars.length; i>0; i--) {
            ds_content=labelSubstringStartingAtOfLength(ds_content,ds_vars[i-1][0],ds_vars[i-1][1]);
        }
        element.html(ds_content);
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

