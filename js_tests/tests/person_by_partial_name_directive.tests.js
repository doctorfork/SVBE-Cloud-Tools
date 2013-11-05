function dumpElement(elt) {
  var holder = $('<div>').append(elt);
  return holder.html();
}

describe('person by partial name directive works', function() {
  var element, scope;
  
  beforeEach(module('SVBE'));
  beforeEach(module('templates'));
  
  beforeEach(inject(function($rootScope, $compile, $templateCache) {
    element = angular.element(
      '<person-by-partial-name selected-person="person"/>');
    scope = $rootScope.$new();
    element = $compile(element)(scope);
    scope.$digest();
    console.log(dumpElement(element));
  }));
  
  it('compiles', function() {
    expect(element.find('form').length).toBe(1);
  });
});
