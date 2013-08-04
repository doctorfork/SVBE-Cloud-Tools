function EventController($scope, $log, $http, Person) {
  $scope.newEvent = {};
  
  $scope.create = function() {
    $log.info('created');
    var handler = function() {
      $scope.newEvent = {};
    };
    var errorHandler = function(err) {
      $log.info(err);
    };

    $http.post("/api/event/save", $scope.newEvent)
      .then(handler, errorHandler);
  };
  
  $scope.populateWithFakeData = function() {
    
  };
}
