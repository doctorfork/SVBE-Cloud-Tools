function EventRegistrationController($scope, $http, $log, $timeout) {
  $scope.personSearchName = '';
  $scope.selectedPerson = null;
  $scope.possiblePeople = {};
  $scope.registrationError = '';  // Error message from registration attempt.
  
  $scope.eventRoles = {}; // Maps role-types to counts (what event needs)
  $scope.personEventRoles = {}; // Maps role-types to counts (what event has)

  // Fetch the person event role counts (what this event has).
  $scope.fetchPersonEventRoles = function() {
    $http.get('/api/person_event_roles/get_summary_by_event/' + $scope.event.key).
      success(function(data) {
        $scope.personEventRoles = data;
      });  
  };
  // TODO(wesalvaro): Fetch this in a resolve.
  $scope.fetchPersonEventRoles();
  
  $scope.getPossibleRolesForSelectedPerson = function() {
    if (!$scope.selectedPerson) return [];
    
    var personRoles = $scope.selectedPerson.roles;
    var neededRoles = [];
    $log.info('Person roles:', personRoles);
    for (var i = 0; i < personRoles.length; ++i) {
      if ($scope.event.roles[personRoles[i]['roleType']] > 0) {
        // Then we need at least one more of these.
        neededRoles.push(personRoles[i]);
      }
    }
    return neededRoles;
  } 
  
  // Register the currently selected person for this event.
  $scope.registerPerson = function(role) {
    $http.post('/api/event/register_person', {
        'eventKey': $scope.event.key, 
        'personKey': $scope.selectedPerson.key,
        'roleKey': role
      }).then(function() {
        $scope.selectedPerson = null;
        $scope.personSearchName = ''; 
        $scope.possiblePeople = new Object();
        // Re-fetch this event's registration so we see the new registrant.
        $log.info('About to fetch more person event roles.');
        $timeout(function() { $scope.fetchPersonEventRoles(); }, 500);
      }, function(data) {
        $scope.registrationError = data;
      });
  };
}
