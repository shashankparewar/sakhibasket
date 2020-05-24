(function () {
    'use strict';
    var app = angular
        .module('sakhiBasket')
        .controller('OrderController', function($scope, $http, $location) {
            $scope.name = "Shashank"
            $scope.rows = [{
                "index": 1,
                "category": "",
                "product": {},
                "quantity": 0
            }]
            $scope.popup = {
                opened: false
            };
            $scope.options = {
                formatYear: 'yy',
                maxDate: new Date(2020, 5, 28),
                minDate: new Date(),
                startingDay: 1
            };
            $scope.init = function(){
                $http.get("/app/api/v1/category/").then(function (data) {
                    $scope.categories = data.data
                }, function (error) {

                })
                $scope.total_price = 0

                $scope.status = {
                    isFirstOpen: true
                };
                $scope.order = {
                    address: {
                        "city": "Ranchi",
                        "state": "Jharkhand"
                    }
                }
            }
            $scope.load_products = function (index, id) {
                var data = {category: id}
                if (index == $scope.rows.length - 1){
                    $scope.rows.push({
                        "index": index + 2,
                        "category": "",
                        "product": {},
                        "quantity": 0
                    })
                }
                $http.post("/app/api/v1/item/filter/", data).then(function (data) {
                    $scope.rows[index]["products"] = data.data
                }, function (error) {

                })
            }
            $scope.openPersonal = function(){
                $scope.status.isFirstOpen = false
            }
            $scope.calculatePrice = function () {
                var total_price = 0
                $scope.rows.map(function (item, index) {
                    total_price += (item.product.price * item.quantity) || 0
                })
                $scope.total_price = total_price
            }
            $scope.openCalendar = function() {
                $scope.popup.opened = true;
            };
            $scope.placeOrder = function () {
                $scope.order["items"] = $scope.rows.filter(function (item, index) {
                        return item.product && item.quantity
                    }).map(function (item, index) {
                        return {
                            ordered : true,
                            item_id : item.product.id,
                            quantity: item.quantity
                        }
                    })
                $scope.order.address.name = $scope.order.name
                $scope.order.address.email = $scope.order.email
                $http.post("/app/api/v1/order/", $scope.order).then(function (data) {
                    $location.path("/order/"+data.data.readable_id);
                }, function (error) {

                })
            }
        })
})()