angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .service("DefaultConfigs", DefaultConfigs)
  .config(function($locationProvider) {
    $locationProvider.html5Mode(true);
  });
