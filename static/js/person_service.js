function PersonService($http, $q) {
  this.http_ = $http;
  this.q_ = $q;
}

PersonService.successHandler_ = function(response) {
  return response.data;	
};

PersonService.errorHandler_ = function(response) {
  throw response.data;	
};

PersonService.prototype.save = function(json) {
  return this.http_.post("/api/person", json).then(
    PersonService.successHandler_, 
    PersonService.errorHandler_);
};

PersonService.prototype.get = function(key) {
  if (key) {
    return this.http_.get("/api/person/" + key).then(
      PersonService.successHandler_, 
      PersonService.errorHandler_);
  } else {
    return this.q_.when({
        birthday: new Date(),
        roles: []
    });
  }
};

PersonService.prototype.remove = function(person) {
  return this.http_.delete("/api/person/" + person.key).then(
    PersonService.successHandler_, 
    PersonService.errorHandler_);
};
