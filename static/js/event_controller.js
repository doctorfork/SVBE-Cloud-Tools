function EventController($scope, $log, $http) {
  $scope.newEvent = {};
  $scope.possibleRoles = [];
  $scope.newEvent.roles = {};
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });
  
  $scope.create = function() {
    $log.info('created');
    var handler = function() {
      $scope.newEvent = {};
      $scope.newEvent.roles = {};
    };
    var errorHandler = function(err) {
      $log.info(err);
    };

    $http.post("/api/event", $scope.newEvent)
      .then(handler, errorHandler);
  };
  
  $scope.getRoleSelected = function(role) {
    $log.info(role);
    return role in $scope.newEvent.roles;
  };
  
  $scope.getRoleClass = function(role) {
    if (role in $scope.newEvent.roles) {
      return 'btn btn-success';
    } else {
      return 'btn btn-primary';
    }
  };
  
  $scope.toggleRole = function(role) {
    if (role in $scope.newEvent.roles) {
      delete $scope.newEvent.roles[role];
    } else {
      $scope.newEvent.roles[role] = 1;
    }
  };
  
  $scope.populateWithFakeData = function() {
    $scope.newEvent.title = "An exciting event";
    $scope.newEvent.date = new Date();
    $scope.newEvent.setupTime = "01:00 PM";
    $scope.newEvent.startTime = "02:00 PM";
    $scope.newEvent.stopTime = "06:00 PM";
    $scope.newEvent.address = "123 Somewhere St.";
    $scope.newEvent.roles['Assistant'] = 12;
  };
}
