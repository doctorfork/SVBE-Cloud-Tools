function PersonService($http, $log) {
  this.http_ = $http;
}

PersonService.prototype.create = function(json) {
  return this.http_.post("/api/person", json);
};

PersonService.prototype.get = function(key) {
  if (key) {
    
  } else {
    return {};
  }
};
