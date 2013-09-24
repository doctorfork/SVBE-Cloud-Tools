angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .service("DefaultConfigsService", DefaultConfigs)
  .service('EventService', EventService)
  .config(function($routeProvider, $locationProvider) {
    $routeProvider.when('/event/:key', {
       templateUrl: 'event.html',
       controller: EventController,
       resolve: {
          event: function($route, EventService) {
            var key = $route.current.params['key'];
            return EventService.get(key);
          }
        }
      });
    $routeProvider.when('/createPerson', {
      templateUrl: 'create_one_of_us_person.html',
      controller: PersonController
    });
    $routeProvider.otherwise({
      templateUrl: 'things_to_do.html'
    });
    //$locationProvider.html5Mode(true);
  });
