function PickEventController($scope, $log, $http) {
  $scope.events = [];
  $scope.eventKey = "";

  $http.get('/api/event/list').success(function(data) {
    $scope.events = data;
  });
  
  $scope.setActiveEvent = function($event, key) {
    $scope.activeEvent = key;
  };
  
  $scope.getHumanReadableDate = function(dateStr) {
    return new Date(dateStr).toLocaleDateString();
  };
}
