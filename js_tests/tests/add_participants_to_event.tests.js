describe('add participants to event partial', function() {
  var controller, scope, httpBackend, timeout;
  beforeEach(module('SVBE'));
  
  beforeEach(inject(function($rootScope, $controller, $httpBackend, 
                             $timeout) {
    scope = $rootScope.$new();
    scope.event = {
      key: '1234',
      roles: {'Apprentice': 12, 'Czar': 1}
    };
    httpBackend = $httpBackend;
    httpBackend.expectGET('/api/person_event_roles/get_by_event/1234').
        respond(201, {'Apprentice': 1});
    
    controller = $controller('AddParticipantsToEventController', 
        {$scope: scope});
    httpBackend.flush();
    
    timeout = $timeout;
  }));
  
  afterEach(function() {
    httpBackend.verifyNoOutstandingExpectation();
    httpBackend.verifyNoOutstandingRequest();
  });
  
  it('doesnt break when person is null', function() {
    expect(scope.getPossibleRolesForSelectedPerson().length).toBe(0);
  });
  
  it('correctly gets roles for the selected person', function() {
    // We expect the valid roles for the selected person to be
    // (roles the event needs) intersected with (roles the person can fill).
    scope.selectedPerson = {
      roles: [
        {roleType: 'Apprentice'},
        {roleType: 'Mechanic'}
      ]
    };
    
    expect(scope.getPossibleRolesForSelectedPerson()).toEqual(
        [{roleType:'Apprentice'}]);
  });
  
  it('can register people for roles', function() {
    scope.selectedPerson = {key: '5678'};
    httpBackend.expectPOST('/api/event/register_person', {
      eventKey: '1234',
      personKey: '5678',
      roleKey: 'aabb'
    }).respond(201);
    scope.registerPerson('aabb');
    httpBackend.flush();
    
    // The controller will wait for a bit, then re-fetch the personEventRoles
    // to see the newly added person.
    httpBackend.expectGET('/api/person_event_roles/get_by_event/1234').
        respond(201, {'Apprentice': 1, 'Czar': 1});
    timeout.flush();
    httpBackend.flush();
  });
});
