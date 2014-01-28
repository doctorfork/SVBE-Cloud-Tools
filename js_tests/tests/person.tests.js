'use strict';

describe('PersonService', function() {
  var personService;
  var $httpBackend;
  var rootScope;
  
  beforeEach(angular.mock.module('SVBE'));
  beforeEach(angular.mock.inject(function(PersonService, _$httpBackend_, $rootScope) {
    personService = PersonService;
    $httpBackend = _$httpBackend_;
    rootScope = $rootScope;
  }));
     
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });
     
  it('saves correctly', function() {
    $httpBackend.expectPOST('/api/person', '{"foo":"bar"}').respond(201, '');
    personService.save({'foo': 'bar'});
    $httpBackend.flush();
  });
  
  it('save fails', function() {
    var expected = 'Bad person.';
    $httpBackend.expectPOST('/api/person', '{"foo":"bar"}').respond(400, expected);
    personService.save({'foo': 'bar'});
    try {
      $httpBackend.flush();
      fail();
    } catch (actual) {
      expect(actual).toBe(expected);
    }
  });
  
  it('gets correctly', function() {
    $httpBackend.expectGET('/api/person/123').respond(200, '{"id": 123}');
    personService.get(123);
    $httpBackend.flush();
  });
  
  it('get fails', function() {
    var expected = 'Bad person.';
    $httpBackend.expectGET('/api/person/123').respond(400, expected);
    personService.get(123);
    try {
      $httpBackend.flush();
      fail();
    } catch (actual) {
      expect(actual).toBe(expected);
    }
  });
  
  it('gets default', function() {
    personService.get().then(function(actual) {
      expect(actual.birthday).toBeDefined();
      expect(actual.roles.length).toEqual(0);
    });
    rootScope.$digest();
  });
  
  it('removes correctly', function() {
    $httpBackend.expectDELETE('/api/person/123').respond(200);
    personService.remove({key: 123});
    $httpBackend.flush();
  });
  
  it('remove fails', function() {
    var expected = 'Bad person.';
    $httpBackend.expectDELETE('/api/person/123').respond(400, expected);
    personService.remove({key: 123});
    try {
      $httpBackend.flush();
      fail();
    } catch (actual) {
      expect(actual).toBe(expected);
    }
  });
  
});


describe('PersonController', function() {
  var personService;
  var personController;
  var scope;
  var http;
  var location;
  var dfr;
  var rootScope;
  
  beforeEach(angular.mock.inject(function($q, $rootScope) {
    personService = jasmine.createSpyObj('person', ['save']);
    http = jasmine.createSpyObj('http', ['get']);
    http.get.andReturn(jasmine.createSpyObj('promise', ['success']));
    location = jasmine.createSpyObj('location', ['path']);
    dfr = $q.defer();
    rootScope = $rootScope;
    personService.save.andReturn(dfr.promise);
    scope = {};
    
    personController = new PersonController(scope, {}, http, {}, personService, {key: 1}, location);
  }));

  it('creates correctly', function() {
    scope.save();
    
    var savedPerson = {key: 2};
    
    expect(personService.save).toHaveBeenCalledWith(scope.person);
    
    dfr.resolve(savedPerson);
    rootScope.$digest();
    
    expect(scope.person).toBe(savedPerson);
    expect(location.path).toHaveBeenCalledWith('/listPeople');
    expect(scope.errorMessage).toBe('');
  });
  
  it('creates fails', function() {
    scope.save();
    
    expect(personService.save).toHaveBeenCalledWith(scope.person);
    
    dfr.reject('could not save');
    rootScope.$digest();
    
    expect(scope.person).toEqual({key: 1});
    expect(location.path).not.toHaveBeenCalled();
    expect(scope.errorMessage).toBe('could not save');
  });
  
})
