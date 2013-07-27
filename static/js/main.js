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
    return $http.post("http://localhost:9080/person", json);
  };
}

function PersonController($scope, $log, Person) {
  $scope.datepicker = {date: new Date()};
  $scope.person = {};
  $scope.create = function() {
    $log.info('created');
    Person.create($scope.person).then(function() {
      $scope.person = {};
    }, function(err) {
      $log.info(err);
    });
  };
}

angular.module("SVBE", ['$strap.directives'])
  .service("Person", Person)
