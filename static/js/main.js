function Person($http, $log) {
  this.create = function(json) {
    return $http.post("/person", json);
  };
}

function PersonCreate($scope, $log, Person) {
	$scope.current_year = new Date().getFullYear();
  $scope.create = function() {
    $log.info('created');
    Person.create($scope.person).then(function() {
      $scope.person = {};
    }, function(err) {
      $log.info(err);
    });
  };
}

angular.module("SVBE", [])
  .service("Person", Person)
