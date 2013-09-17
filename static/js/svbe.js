angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .service("DefaultConfigs", DefaultConfigs)
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
    //$locationProvider.html5Mode(true);
  });
