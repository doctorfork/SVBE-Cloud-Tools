function PersonByPartialNameDirective($http, $log) {
  return {
    restrict: 'E',
    scope: {
      'selectedPerson': '='
    },
    templateUrl: 
        '/static/html/person_by_partial_name_directive_template.html',
    link: function(scope, element, attr) {
    
      // Search function to find a person by their name or a fragment thereof.
      scope.getPeopleByPartialName = function() {
        $log.info('prefix: ' + scope.personSearchName);
        $http.get('/api/person/by_name/' + scope.personSearchName).success(
          function(data) {
            scope.possiblePeople = new Object();
            for (var i = 0; i < data.length; ++i) {
              scope.possiblePeople[data[i].key] = data[i];
            }
          });
      };
      
      scope.$watch('selectedPersonKey', function() {
        scope.selectedPerson = scope.possiblePeople[scope.selectedPersonKey];
      });
    }
  };
}