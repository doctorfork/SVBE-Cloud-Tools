function EventService($http, $q, DefaultConfigsService) {
  this.defaultEvent = DefaultConfigsService.getEvent();
  this.http = $http;
  this.q = $q;
}

EventService.prototype.get = function(key) {
  if (key) {
    return this.http.get('/api/event/' + key).then(function(data) {
       console.log(data.data)
      return data.data;
    });
  } else {
    return this.q.when(this.defaultEvent);
  }
}

function EventController($scope, $log, $http, $timeout, $location, event, 
                         DefaultConfigsService) {
  $scope.event = event;
  $scope.date = new Date(event.startTime);
  $scope.startTime = new Date(event.startTime);
  $scope.setupTime = new Date(event.setupTime);
  $scope.stopTime = new Date(event.stopTime);
  console.log(JSON.stringify(event))
  $scope.possibleRoles = [];
  $scope.datePickerOpened = false;
  var combineStartTimes = function() {
     var d = $scope.date;
     var t = $scope.startTime;
     d.setHours(t.getHours());
     d.setMinutes(t.getMinutes());
     event.startTime = d;
     console.log('Start time')
  };
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });
  
  $scope.save = function() {
    combineStartTimes();
    $log.info('created');
    var handler = function(response) {
      $location.path('/event/' + response.data.key);
      //$scope.event = DefaultConfigsService.getEvent();
    };
    var errorHandler = function(err) {
      $log.info(err);
    };

    $http.post("/api/event", $scope.event)
      .then(handler, errorHandler);
  };
  
  $scope.openDatePicker = function() {
    $timeout(function() {
      $scope.datePickerOpened = true;
    });
  };
  
  $scope.getRoleSelected = function(role) {
    return role in $scope.event.roles;
  };
  
  $scope.getRoleClass = function(role) {
    if (role in $scope.event.roles) {
      return 'btn btn-success';
    } else {
      return 'btn btn-primary';
    }
  };
  
  $scope.toggleRole = function(role) {
    if (role in $scope.event.roles) {
      delete $scope.event.roles[role];
    } else {
      $scope.event.roles[role] = 1;
    }
  };
}
