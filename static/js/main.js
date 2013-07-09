function ctrl($scope) { //, Event) {
  //$scope.foo = Event.promise;
  $scope.foo = 1;
}

function Event($http, $log) {
  this.promise = $http.get("http://jsbin.com/ojabuv/1/js").then(function(response) {
    $log.info(response.data);
    return response.data;
  });
  
}

function Person($http, $log) {
  this.create = function(json) {
    return $http.post("/person", json);
  };
}

function PersonCreate($scope, $log, Person) {
  $scope.create = function() {
    $log.info('created');
    Person.create($scope.Person).then(function() {
      $scope.Person = {};
    }, function(err) {
      $log.info(err);
    });
  };
}

angular.module("SVBE", [])
  //.service("Event", Event)
  .service("Person", Person)
  .controller("Main", ctrl);
