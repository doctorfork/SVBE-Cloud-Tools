function AddParticipantsToEventController($scope, $log, $http, $location) {
  $scope.eventKey = $location.search()['eventKey'];
  
  $http.get('/api/event_roles/get_by_event/' + $scope.eventKey).success(
    function(data) {
      $scope.eventRoles = data;
    });
}
