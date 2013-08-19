function AddParticipantsToEventController($scope, $log, $http, $location) {
  $scope.eventKey = $location.search()['eventKey'];
  $scope.personSearchName = "";
  $scope.personKey = "";
  
  $http.get('/api/event_roles/get_by_event/' + $scope.eventKey).success(
    function(data) {
      $scope.eventRoles = data;
    });
    
  $scope.getPeopleByPartialName = function() {
    $log.info('prefix: ' + $scope.personSearchName);
    $http.get('/api/person/by_name/' + $scope.personSearchName).success(
      function(data) {
        $scope.possiblePeople = data;
      });
  };
  
  $scope.registerPerson = function() {
    // Register the currently selected person for this event.
    $http.post('/api/event/register_person',
      {'eventKey': $scope.eventKey, 'personKey': $scope.personKey}).success(
        function() {
          $scope.personKey = "";
          $scope.personSearchName = ""; 
          $scope.possiblePeople = [];
        });
  };
}
