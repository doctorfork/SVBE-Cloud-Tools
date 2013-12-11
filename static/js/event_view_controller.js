function EventViewController($scope, $http, $log, event) {
  $scope.event = event;
  $log.info('Event', $scope.event);
  
  // Fetch the event role counts (what this event needs).
  $http.get('/api/event_roles/get_by_event/' + $scope.event.key).
    success(function(data) {
      $scope.eventRoles = {};
      angular.forEach(data, function(eventRole) {
        $scope.eventRoles[eventRole[0]['role_type']] = eventRole[1];
      });
    });
  
  // Fetch the actual PersonEventRole records (what people are actually registered).
  $http.get('/api/person_event_roles/get_by_event/' + 
            $scope.event.key).success(function(data) {
              $scope.personEventRoles = data;
              console.log(data);
            });

  $scope.unregisterPerson = function(personEventRoleIndex, roleKey) {
    $log.info('unregistering for ', roleKey);
    $http.post('/api/person_event_roles/remove/' + roleKey).success(function() {
      $scope.personEventRoles.splice(personEventRoleIndex, 1);
    });
  };
}
