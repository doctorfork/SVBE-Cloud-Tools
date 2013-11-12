function PersonService($http, $log) {
  this.http_ = $http;
}

PersonService.prototype.create = function(json) {
  return this.http_.post("/api/person", json);
};

PersonService.prototype.get = function(key) {
  if (key) {
    return this.http_.get("/api/person/" + key).then(function(response) {
       console.log(response.data)
      return response.data;
    });
  } else {
    return {};
  }
};
