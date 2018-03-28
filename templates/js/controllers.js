angular.module('seil_solar')

.controller('HomeCtrl', function($scope,$http, $window, $location) {
	$scope.devices=[];
	$scope.in_progress=true;
	var d = new Date
	$scope.timestamp = ('0' + d.getDate()).slice(-2) + 
			   ('0' + d.getHours()).slice(-2) + 
			   ('0' + d.getMinutes()).slice(-2);
    $http.get("/client").then(function successCallback(response){
    	$scope.devices = response.data
    	$scope.in_progress = false;
    }, function errorCallback(response){
    	console.log(response)
    })

    $scope.sendDebug = function(device){
    	console.log(device.debug)
    	$http.get("http://"+device.ip+"/debug?"+device.debug).then(function successCallback(reponse){
    		alert("Debug message sent successfully");
    	},function errorCallback(reponse){
    		alert("Debug message could not be sent");
    	})
    }
})