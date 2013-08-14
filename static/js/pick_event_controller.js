function PickEventController($scope, $log, $http) {
  $scope.events = [];
  $scope.eventKey = "";

  $http.get('/api/event').success(function(data) {
    $scope.events = data;
  });
  
  $scope.setActiveEvent = function($event, key) {
    $scope.activeEvent = key;
    //$event.target.cls = "ng-active";
  };
  
  $scope.getHumanReadableDate = function(dateStr) {
    return new Date(dateStr).toLocaleDateString();
  };
}
