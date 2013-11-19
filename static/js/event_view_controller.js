function EventViewController($scope, $http, event) {
  $scope.event = event;
  console.log('Event');
  console.log($scope.event);
  
  // Fetch the event role counts (what this event needs).
  $http.get('/api/event_roles/get_by_event/' + $scope.event.key).success(
    function(data) {
      $scope.eventRoles = {};
      for (var i = 0; i < data.length; ++i) {
        $scope.eventRoles[data[i][0]["role_type"]] = data[i][1];
      }
    });

  // Fetch the actual PersonEventRole records (what people are actually registered).
  $http.get('/api/person_event_roles/get_by_event/' + 
            $scope.event.key).success(function(data) {
              $scope.personEventRoles = data;
            });
}
