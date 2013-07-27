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
    return $http.post("http://localhost:9080/api/person/save", json);
  };
}

function PersonController($scope, $log, Person) {
  $scope.person = {};
  
  $scope.splitDate = function() {
    var d = new Date($scope.person.birthday);
    $scope.person.birthdayMonth = d.getMonth();
    $scope.person.birthdayDay = d.getDay();
    $scope.person.birthdayYear = d.getFullYear();
  }
  
  $scope.create = function() {
    $log.info('created');
    Person.create($scope.person).then(function() {
      $scope.person = {};
    }, function(err) {
      $log.info(err);
    });
  };
  
  $scope.populateWithFakeData = function() {
    $scope.person.fullName = "Stanley Q. Fakerton"
    $scope.person.birthday = new Date();
    $scope.person.mobileNumber = "555-1212";
    $scope.person.email = "stan@fake.com";
    $scope.splitDate();
  };
}

angular.module("SVBE", ['$strap.directives'])
  .service("Person", Person)
