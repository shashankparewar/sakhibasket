'use strict';

angular.module('sakhiBasket').config(['$routeProvider',
    function config($routeProvider) {
        $routeProvider.when('/order', {
            templateUrl: '/app/order',
            controller: 'OrderController'
        }).when('/order/:order_id', {
            templateUrl: '/app/order_summary',
            controller: 'OrderSummaryController'
        }).otherwise('/order');
    }
]);


/* Init global settings and run the app */
angular.module('sakhiBasket').config(["$httpProvider", function ($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
}]);