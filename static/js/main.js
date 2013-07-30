function Contact($http, $log) {
  this.create = function(json) {
    return $http.post("/api/contact/save", json);
  }
}

function Person($http, $log) {
  this.create = function(json) {
    return $http.post("/api/person/save", json);
  };
}

function PersonController($scope, $log, Person) {
  $scope.person = {};
  $scope.personType = 'contact'
  
  $scope.splitDate = function() {
    var d = new Date($scope.person.birthday);
    $scope.person.birthdayMonth = d.getMonth();
    $scope.person.birthdayDay = d.getDay();
    $scope.person.birthdayYear = d.getFullYear();
  }
  
  $scope.create = function() {
    $log.info('created');
    var handler = function() {
      $scope.person = {};
    };
    var errorHandler = function(err) {
      $log.info(err);
    };
    
    if ($scope.personType == 'contact') {
      Contact.create($scope.person).then(handler, errorHandler);
    } else if ($scope.personType == 'person') {
      Person.create($scope.person).then(handler, errorHandler);
    } else {
      $log.warning('Unknown kind of person - ' + $scope.personType);
    }
  };
  
  $scope.populateWithFakeData = function() {
    $scope.person.address = '123 Anywhere St.';
    $scope.person.phoneNumber = '555-2323';
    
    if ($scope.personType == 'person') {
      $scope.person.fullName = "Stanley Q. Fakerton"
      $scope.person.birthday = new Date();
      $scope.person.mobileNumber = "555-1212";
      $scope.person.email = "stan@fake.com";
      $scope.splitDate();
    }
  };
}

angular.module("SVBE", ['$strap.directives'])
  .service("Person", Person)
