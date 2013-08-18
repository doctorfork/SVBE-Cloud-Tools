angular.module("SVBE", ['$strap.directives'])
  .service("Person", Person)
  .config(function($locationProvider) {
    $locationProvider.html5Mode(true);
  });
