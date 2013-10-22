function ListPeopleController($scope, $http, $log) {
  $http.get('/api/person/list').success(function(data) {
    $scope.people = data;
  });
}
