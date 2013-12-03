function ListEventsController($scope, $http, $log) {
  $http.get('/api/event/list').success(function(data) {
    $scope.events = data;
  });

  $scope.getHumanReadableDateString = function(dateString) {
    return new Date(dateString).toLocaleString();
  };
}
