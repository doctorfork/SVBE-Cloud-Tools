function Contact($http, $log) {
  this.create = function(json) {
    return $http.post("/api/contact/save", json);
  }
}

function PersonController($scope, $log, $http, $timeout, Person) {
  $scope.person = {};
  $scope.person.birthday = new Date();
  $scope.person.roles = {};
  $scope.personType = 'person'
  $scope.possibleRoles = [];
  $scope.datePickerOpened = false;
  $scope.maxBirthday = new Date();
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });
  
  $scope.splitDate = function() {
    var d = new Date($scope.person.birthday);
    $scope.person.birthdayMonth = d.getMonth();
    $scope.person.birthdayDay = d.getDate();
    $scope.person.birthdayYear = d.getFullYear();
  }
  
  $scope.openDatePicker = function() {
    $timeout(function() {
      $scope.datePickerOpened = true;
    });
  };
  
  $scope.dateOptions = {
    'year-format': "'yy'",
    'starting-day': 1
  };
  
  $scope.getRoleClass = function(role) {
    if (role in $scope.person.roles) {
      return 'btn btn-success';
    } else {
      return 'btn btn-primary';
    }
  };
  
  $scope.toggleRole = function(role) {
    if (role in $scope.person.roles) {
      delete $scope.person.roles[role];
    } else {
      $scope.person.roles[role] = 1;
    }
  };
  
  $scope.create = function() {
    $log.info('created');
    var handler = function() {
      $scope.person = {};
      $scope.person.roles = {};
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
    $scope.person.roles = {"Apprentice": 1};
    $scope.person.fullName = "Stanley Q. Fakerton"
    $scope.person.birthday = new Date();
    $scope.person.mobileNumber = "555-1212";
    $scope.person.email = "stan@fake.com";
    $scope.splitDate();
  };
}

