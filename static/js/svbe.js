angular.module("SVBE", ['ui.bootstrap'])
  .service("PersonService", PersonService)
  .service("DefaultConfigsService", DefaultConfigs)
  .service('EventService', EventService)
  .directive('personbypartialname', PersonByPartialNameDirective)
  .config(function($routeProvider, $locationProvider) {
    $routeProvider.when('/event/:key/edit', {
       templateUrl: 'event.html',
       controller: EventController,
       resolve: {
          event: function($route, EventService) {
            var key = $route.current.params['key'];
            return EventService.get(key);
          }
        }
      });
    $routeProvider.when('/person', {
      templateUrl: 'person.html',
      controller: PersonController,
      resolve: {
        person: function($route, PersonService) {
          var key = $route.current.params['key'];
          return PersonService.get(key);
        }
      }
    });
    $routeProvider.when('/pickEvent', {
      templateUrl: 'pick_event.html',
      controller: PickEventController
    });
    $routeProvider.when('/event/:key', {
      templateUrl: 'add_participants_to_event.html',
      controller: AddParticipantsToEventController,
      resolve: {
        event: function($route, EventService) {
          var key = $route.current.params['key'];
          return EventService.get(key);
        }
      }
    });
    $routeProvider.otherwise({
      templateUrl: 'things_to_do.html'
    });
    //$locationProvider.html5Mode(true);
  });
