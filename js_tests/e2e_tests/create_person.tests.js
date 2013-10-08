'use strict';

describe('PersonController', function() {
  var $httpBackend;
  var scope;
  var createController;
     
  it('creates correctly', function() {
    browser().navigateTo(
      '/static/html/index.html#/createPerson');
    input('person.fullName').enter('Jack Drebin');

    // Look up the person somehow, and verify that it got created.
  });
});
