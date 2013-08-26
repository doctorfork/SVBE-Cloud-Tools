function EventController($scope, $log, $http, $timeout) {
  $scope.newEvent = {};
  $scope.possibleRoles = [];
  $scope.newEvent.roles = {};
  $scope.datePickerOpened = false;
  
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
  
  $scope.populateWithFakeData = function() {
    $scope.newEvent.title = "An exciting event";
    $scope.newEvent.date = new Date();
    $scope.newEvent.setupTime = new Date();
    $scope.newEvent.setupTime.setHours(10);
    $scope.newEvent.startTime = new Date();
    $scope.newEvent.startTime.setHours(12);
    $scope.newEvent.stopTime = new Date();
    $scope.newEvent.stopTime.setHours(18);
    $scope.newEvent.address = "123 Somewhere St.";
    $scope.newEvent.roles['Apprentice'] = 12;
    $scope.newEvent.roles['Mechanic'] = 3;
  };
}
