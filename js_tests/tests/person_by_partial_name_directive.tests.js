function dumpElement(elt) {
  var holder = $('<div>').append(elt);
  return holder.html();
}

describe('person by partial name directive works', function() {
  var element, scope, httpBackend;

  var personObject = [
    {
      "fullName": "Stanley Q. Fakerton",
      "birthday": "2013-11-05T00:00:00.000000Z",
      "key": "ahNkZXZ-YWN0aXZlLWJpcmQtMjU2chQLEgdDb250YWN0GICAgICAgIAKDA",
      "mobileNumber": "555-1212",
      "email": "stan@fake.com",
      "address": "123 Anywhere St.",
      "roles": [
        {
          "roleInfoURL": null,
          "roleType": "Apprentice",
          "roleBriefDescription": null,
          "key": "ahNkZXZ-YWN0aXZlLWJpcmQtMjU2chQLEgRSb2xlIgpBcHByZW50aWNlDA"
        }
      ],
      "class": [
        "Contact",
        "Person",
        "OneOfUsPerson"
      ],
      "phoneNumber": "555-2323",
      "volunteerPoints": null,
      "emergencyContact": null,
      "responsibleAdult": null,
      "independent": null,
      "volunteerHours": null
    }
  ];
  
  beforeEach(module('SVBE'));
  beforeEach(module('templates'));
  
  beforeEach(inject(function($rootScope, $compile, $httpBackend) {
    element = angular.element(
      '<person-by-partial-name selected-person="exteriorPerson"/>');
    scope = $rootScope.$new();
    element = $compile(element)(scope);
    $rootScope.$digest();
    
    httpBackend = $httpBackend;
  }));
  
  afterEach(function() {
    httpBackend.verifyNoOutstandingExpectation();
    httpBackend.verifyNoOutstandingRequest();
  });
  
  it('compiles', function() {
    expect(element.find('form').length).toBe(1);
  });
  
  it('populates selected person', function() {
    httpBackend.expectGET('/api/person/by_name/foo').
        respond(201, personObject);
    
    element.find('input#person-name').val('foo').trigger('input');
    element.find('#search-btn').click();
    httpBackend.flush();
    
    var btnSelector = element.find('#candidate-people-buttons > button');
    expect(btnSelector.length).toEqual(1);
    expect(scope.exteriorPerson).not.toBeDefined();
    btnSelector.click();
    expect(scope.exteriorPerson).toBeDefined();
  });
});
