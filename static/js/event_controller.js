var EventService = function($http, $q, $log, DefaultConfigsService) {
  this.defaultEvent = DefaultConfigsService.getEvent();
  this.http = $http;
  this.q = $q;
  this.log = $log;
};


EventService.prototype.get = function(key) {
  if (key) {
    var self = this;
    return this.http.get('/api/event/' + key).
      then(function(response) {
        self.log(response.data)
        return response.data;
      });
  } else {
    return this.q.when(this.defaultEvent);
  }
};


EventService.prototype.save = function(event) {
  var self = this;
  this.http.post('/api/event', event).
    then(function(response) {
      self.log.info('Saved.');
      return response.data.key;
    }, function(err) {
      self.log.error(err);
      throw 'Could not save event.';
    });
};



var EventController = function(
    $scope, $log, $http, $timeout, $location, event, EventService) {
  $scope.event = event;
  $scope.date = new Date(event.startTime);
  $scope.startTime = new Date(event.startTime);
  $scope.setupTime = new Date(event.setupTime);
  $scope.stopTime = new Date(event.stopTime);
  $scope.possibleRoles = [];
  $scope.datePickerOpened = false;
  var combineStartTimes = function() {
     var d = $scope.date;
     var t = $scope.startTime;
     d.setHours(t.getHours());
     d.setMinutes(t.getMinutes());
     event.startTime = d;
  };
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });
  
  $scope.save = function() {
    combineStartTimes();
    EventService.save($scope.event).
      then(function(key) {
        $location.path('/event/' + key);
      });
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
};
