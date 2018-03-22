angular.module('seil_solar', ['ngMaterial','ngResource'])

.config(function($mdThemingProvider, $interpolateProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('yellow')
    .accentPalette('blue')
    // .dark();

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
