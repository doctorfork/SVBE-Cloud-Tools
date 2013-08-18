function Person($http, $log) {
  this.create = function(json) {
    return $http.post("/api/person", json);
  };
}
