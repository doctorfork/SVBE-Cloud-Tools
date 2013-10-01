'use strict';

describe('Person', function() {
  var personService;
  var $httpBackend;
  
  beforeEach(angular.mock.module('SVBE'));
  beforeEach(angular.mock.inject(function(Person, _$httpBackend_) {
    personService = Person;
    $httpBackend = _$httpBackend_;
  }));
     
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });
     
  it('creates correctly', function() {
    $httpBackend.expectPOST('/api/person', '{"foo":"bar"}').respond(201, '');
    personService.create({'foo': 'bar'});
    $httpBackend.flush();
  });
});
