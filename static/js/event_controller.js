function EventController($scope, $log, $http, $timeout, DefaultConfigs) {
  $scope.newEvent = DefaultConfigs.getEvent();
  $scope.possibleRoles = [];
  $scope.datePickerOpened = false;
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });
  
  $scope.create = function() {
    $log.info('created');
    var handler = function() {
      $scope.newEvent = DefaultConfigs.getEvent();
    };
    var errorHandler = function(err) {
      $log.info(err);
    };

    $http.post("/api/event", $scope.newEvent)
      .then(handler, errorHandler);
  };
  
  $scope.openDatePicker = function() {
    $timeout(function() {
      $scope.datePickerOpened = true;
    });
  };
  
  $scope.getRoleSelected = function(role) {
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
}
