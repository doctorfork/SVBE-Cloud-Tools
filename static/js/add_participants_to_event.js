function AddParticipantsToEventController($scope, $log, $http, $location) {
  $scope.eventKey = $location.search()['eventKey'];
  $scope.personSearchName = "";
  $scope.selectedPersonKey = "";
  $scope.possiblePeople = {};
  
  // Fetch the event role counts (what this event needs).
  $http.get('/api/event_roles/get_by_event/' + $scope.eventKey).success(
    function(data) {
      $scope.eventRoles = new Object();
      for (var i = 0; i < data.length; ++i) {
        $scope.eventRoles[data[i][0]["role_type"]] = data[i][1];
      }
    });
    
  // Fetch the person event role counts (what this event has).
  $http.get('/api/person_event_roles/get_by_event/' + 
            $scope.eventKey).success(function(data) {
              $scope.personEventRoles = data;
            });
    
  // Search function to find a person by their name or a fragment thereof.
  $scope.getPeopleByPartialName = function() {
    $log.info('prefix: ' + $scope.personSearchName);
    $http.get('/api/person/by_name/' + $scope.personSearchName).success(
      function(data) {
        $scope.possiblePeople = new Object();
        for (var i = 0; i < data.length; ++i) {
          $scope.possiblePeople[data[i].key] = data[i];
        }
      });
  };
  
  $scope.getSelectedPerson = function() {
    return $scope.possiblePeople[$scope.selectedPersonKey];
  };
  
  // Register the currently selected person for this event.
  $scope.registerPerson = function(role) {
    $http.post('/api/event/register_person',
      {'eventKey': $scope.eventKey, 
       'personKey': $scope.selectedPersonKey,
       'roleType': role}).success(
        function() {
          $scope.selectedPersonKey = "";
          $scope.personSearchName = ""; 
          $scope.possiblePeople = new Object();
        });
  };
}
