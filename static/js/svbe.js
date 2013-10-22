angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .service("DefaultConfigsService", DefaultConfigs)
  .service('EventService', EventService)
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
      .when('/createPerson', {
        templateUrl: 'create_one_of_us_person.html',
        controller: PersonController
      })
      .when('/pickEvent', {
        templateUrl: 'pick_event.html',
        controller: PickEventController
      })
      .when('/event/:key', {
        templateUrl: 'add_participants_to_event.html',
        controller: AddParticipantsToEventController,
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
