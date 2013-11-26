'use strict';

describe('PersonService', function() {
  var personService;
  var $httpBackend;
  
  beforeEach(angular.mock.module('SVBE'));
  beforeEach(angular.mock.inject(function(PersonService, _$httpBackend_) {
    personService = PersonService;
    $httpBackend = _$httpBackend_;
  }));
     
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });
     
  it('creates correctly', function() {
    $httpBackend.expectPOST('/api/person', '{"foo":"bar"}').respond(201, '');
    personService.save({'foo': 'bar'});
    $httpBackend.flush();
  });
});
