function Contact($http, $log) {
  this.create = function(json) {
    return $http.post("/api/contact/save", json);
  }
}

function PersonController($scope, $log, $http, $timeout, PersonService, 
                          person, $location) {
  $scope.person = person;
  $scope.personType = 'person'
  $scope.possibleRoles = [];
  $scope.datePickerOpened = false;
  $scope.maxBirthday = new Date();
  
  // Fetch the list of possible roles.
  $http.get('/api/roles/get').success(function(data) {
    $scope.possibleRoles = data;
  });

  $scope.openDatePicker = function() {
    $timeout(function() {
      $scope.datePickerOpened = true;
    });
  };
  
  $scope.dateOptions = {
    'year-format': "'yy'",
    'starting-day': 1
  };
  
  $scope.getRoleClass = function(roleType) {
     for (var i = 0, ii = $scope.person.roles.length; i < ii; i++) {
        var role = $scope.person.roles[i];
        if (role.roleType == roleType) {
            return 'btn-success';
        }
      }
      return 'btn-primary';
  };
  
  $scope.toggleRole = function(roleType) {
    var deleted;
    for (var i = 0, ii = $scope.person.roles.length; i < ii; i++) {
      var role = $scope.person.roles[i];
      if (role.roleType == roleType) {
          $scope.person.roles.splice(i, 1);
          deleted = true;
          break;
      }
    }
    if (!deleted) {
       $scope.person.roles.push({roleType: roleType}); 
    }
  };
  
  $scope.remove = function() {
    PersonService.remove($scope.person).then(function(person) {
        $scope.person = person;
    });  
  };
  
  $scope.save = function() {
    $log.info('created');
    var handler = function(person) {
	  $scope.person = person;
	  $location.path('/person/' + person.key + '/edit')
      $scope.errorMessage = '';
    };
    var errorHandler = function(err) {
      $log.info(err);
      $scope.errorMessage = err['data'];
    };
    
    PersonService.create($scope.person).then(handler, errorHandler);
  };
  
  $scope.populateWithFakeData = function() {
    $scope.person.address = '123 Anywhere St.';
    $scope.person.phoneNumber = '345-555-2323';
    $scope.person.roles = [{roleType: "Apprentice"}];
    $scope.person.fullName = "Stanley Q. Fakerton"
    $scope.person.birthday = new Date();
    $scope.person.mobileNumber = "123-555-1212";
    $scope.person.email = "stan@fake.com";
  };
}

