/**
 * Creates default configurations for models.
 */
var DefaultConfigs = function() {};


DefaultConfigs.prototype.getEvent = function(){
  var evt = {
    'eventTitle': 'Fixit Workday',
    'setupTime': new Date(),
    'startTime': new Date(),
    'stopTime': new Date(),
    'roles': {
      'Apprentice': 12,
      'Mechanic': 3
    }
  };
  evt.setupTime.setHours(9);
  evt.setupTime.setMinutes(30);
  evt.startTime.setHours(10);
  evt.startTime.setMinutes(0);
  evt.stopTime.setHours(15);
  evt.stopTime.setMinutes(0);
  evt.address = '2566 Leghorn Street, Mountain View, CA 94043';
  return evt; 
};
