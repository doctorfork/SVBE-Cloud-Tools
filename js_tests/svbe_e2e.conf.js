// Configuration for end to end (e2e) tests.
module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['ng-scenario'],

    files: [
      'e2e_tests/*.tests.js'
    ],
    exclude: [],
    reporters: ['progress'],
    port: 9877,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    browsers: ['Chrome'],
    captureTimeout: 60000,
    singleRun: true,
    proxies: {
      // The following address should be the address of the running server 
      // that will be used in the test.
      '/': 'http://localhost:9080'
    }
  });
};
