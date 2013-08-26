angular.module("SVBE", ['ui.bootstrap'])
  .service("Person", Person)
  .config(function($locationProvider) {
    $locationProvider.html5Mode(true);
  });
