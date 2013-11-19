function PersonService($http, $log) {
  this.http_ = $http;
}

PersonService.prototype.create = function(json) {
  return this.http_.post("/api/person", json).then(function(response) {
    return response.data;	
  });
};

PersonService.prototype.get = function(key) {
  if (key) {
    return this.http_.get("/api/person/" + key).then(function(response) {
      return response.data;
    });
  } else {
    return {
        birthday: new Date(),
        roles: []
    };
  }
};

PersonService.prototype.remove = function(person) {
  return this.http_.delete("/api/person/" + person.key).then(function(response) {
    return response.data;
  });
};
