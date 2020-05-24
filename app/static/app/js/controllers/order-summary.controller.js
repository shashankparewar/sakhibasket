(function () {
    'use strict';
    var app = angular
        .module('sakhiBasket')
        .controller('OrderSummaryController', function($scope, $http, $routeParams) {
            $scope.rows = []
            $scope.order = {}

            $scope.init = function(){
                $http.get("/app/api/v1/order/" + $routeParams.order_id).then(function (data) {
                    $scope.rows = data.data.items
                    delete data.data.items
                    $scope.order = data.data
                    var total_price = 0
                    $scope.rows.map(function (item, index) {
                        total_price += (item.item.price * item.quantity) || 0
                    })
                    $scope.total_price = total_price
                }, function (error) {

                })

                $scope.status = {
                    isFirstOpen: true,
                    isSecOpen: true
                };
            }
        })
})()