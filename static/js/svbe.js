angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .service("DefaultConfigs", DefaultConfigs)
  .config(function($routeProvider, $locationProvider) {
    $routeProvider.when('/event/:key', {
       templateUrl: 'event.html',
       controller: EventController,
       resolve: {
          // I will cause a 1 second delay
          delay: function($q, $timeout) {
            var delay = $q.defer();
            $timeout(delay.resolve, 1000);
            return delay.promise;
          }
        }
      });
    //$locationProvider.html5Mode(true);
  });
