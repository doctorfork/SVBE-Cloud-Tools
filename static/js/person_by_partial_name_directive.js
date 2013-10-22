function PersonByPartialNameDirective($http, $log) {
  return {
    restrict: 'E',
    scope: {
      'selectedPerson': '='
    },
    templateUrl: 
        '/static/html/person_by_partial_name_directive_template.html',
    link: function(scope, element, attr) {
        console.log(scope.selectedPerson)
    
      // Search function to find a person by their name or a fragment thereof.
      scope.getPeopleByPartialName = function() {
        $log.info('prefix: ' + scope.personSearchName);
        $http.get('/api/person/by_name/' + scope.personSearchName).success(function(data) {
          scope.people = data;
        });
      };
      scope.select = function(person) {
        console.log(scope.selectedPerson, person)
        scope.selectedPerson = person;
      };
    }
  };
}