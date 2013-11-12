// Karma configuration
// Generated on Mon Sep 30 2013 18:23:47 GMT-0700 (PDT)

module.exports = function(config) {
  config.set({
    // base path, that will be used to resolve files and exclude
    basePath: '',

    // frameworks to use
    frameworks: ['jasmine'],
    
    preprocessors: {
      '../static/html/**/*.html': ['ng-html2js']
    },
    
    // list of files / patterns to load in the browser
    files: [
      // JQuery must appear before AngularJS
      '../static/jquery-1.10.2/jquery-1.10.2.min.js',
      '../static/angular-1.0.8/angular.js',
      '../static/angular-1.0.8/angular-bootstrap.js',
      '../static/angular-1.0.8/angular-mocks.js',
      '../static/angular-1.0.8/angular-resource.js',
      '../static/angular-1.0.8/angular-sanitize.js',
      '../static/js/**/*.js',
      '../static/html/**/*.html',
      'tests/*.tests.js'
    ],

    ngHtml2JsPreprocessor: {
      cacheIdFromPath: function(filepath) {
        // Keep only the last 3 path components
        // (/static, /html, the file name)
        var toks = filepath.split('/');
        var cacheKey = '/' + 
            toks.slice(toks.length - 3, toks.length).join('/');
        return cacheKey;
      },
      moduleName: 'templates'
    },
    
    // list of files to exclude
    exclude: [
      
    ],

    // test results reporter to use
    // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
    reporters: ['progress'],

    // web server port
    port: 9876,

    // enable / disable colors in the output (reporters and logs)
    colors: true,

    // level of logging
    logLevel: config.LOG_INFO,

    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,
    browsers: ['Chrome'],
    // If browser does not capture in given timeout [ms], kill it
    captureTimeout: 60000,
    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false
  });
};
