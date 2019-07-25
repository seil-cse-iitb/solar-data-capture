angular.module('seil_solar')

	.controller('HomeCtrl', function ($scope, $http, $window, $location) {
		$scope.devices = [];
		$scope.in_progress = true;
		var d = new Date
		$scope.timestamp = d.toDateString() +
			('0' + d.getHours()).slice(-2) +
			('0' + d.getMinutes()).slice(-2);
		$http.get("/client").then(function successCallback(response) {
			$scope.devices = response.data
			$scope.in_progress = false;
		}, function errorCallback(response) {
			console.log(response)
		})
		$scope.startLiveData = function (device) {
			// console.log(device)
			$http.get("/start_live_data/" + device.ip + "/" + $scope.timestamp).then(function successCallback(response) {
				alert("Started live data streaming. Downloaded data is being saved on RPi. Click on Stop Live Data to stop and download here");
				device.streaming = true;
				device.thread_name = response.data;
			}, function errorCallback(response) {
				alert("Error receiving logging data");
			})
		}
		$scope.sendDebug = function (device) {
			console.log(device.debug)
			$http.get("/debug/" + device.ip + "/" + device.debug).then(function successCallback(reponse) {
				alert("Debug message sent successfully");
			}, function errorCallback(reponse) {
				alert("Debug message could not be sent");
			})
		}
	})
