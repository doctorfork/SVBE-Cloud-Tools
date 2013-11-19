angular.module("SVBE", ['ui.bootstrap'])
  .service("PersonService", PersonService)
  .service("DefaultConfigsService", DefaultConfigs)
  .service('EventService', EventService)
  .directive('personByPartialName', PersonByPartialNameDirective)
  .config(function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/event/:key/edit', {
        templateUrl: 'event.html',
        controller: EventController,
        resolve: {
          event: function($route, EventService) {
            var key = $route.current.params['key'];
            return EventService.get(key);
          }
        }
      })
      .when('/person', {
        templateUrl: 'person.html',
        controller: PersonController,
        resolve: {
          person: function($route, PersonService) {
            var key = $route.current.params['key'];
            return PersonService.get(key);
          }
        }
      })
      .when('/listPeople', {
        templateUrl: 'list_people.html',
        controller: ListPeopleController
      })
      .when('/pickEvent', {
        templateUrl: 'pick_event.html',
        controller: PickEventController
      })
      .when('/event/:key', {
        templateUrl: 'event_view.html',
        controller: EventViewController,
        resolve: {
          event: function($route, EventService) {
            var key = $route.current.params['key'];
            return EventService.get(key);
          }
        }
      })
      .when('/event/:key/registrationDetails', {
        templateUrl: 'event_registration_details.html',
        controller: EventViewController,
        resolve: {
          event: function($route, EventService) {
            var key = $route.current.params['key'];
            return EventService.get(key);
          }
        }
      })
      .otherwise({
        templateUrl: 'things_to_do.html'
      });
    //$locationProvider.html5Mode(true);
  });
