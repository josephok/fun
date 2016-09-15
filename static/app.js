(function () {
    const app = angular.module('web', ['ngRoute']);
    app
        .config(['$routeProvider', function ($routeProvider) {
            $routeProvider.when('/', {
                controller: 'IndexController',
                controllerAs: 'index',
                templateUrl: '/static/views/index.html'
            })
            .when('/post/:id', {
                controller: 'PostController',
                controllerAs: 'post',
                templateUrl: '/static/views/post.html'
            })
            .otherwise({redirectTo: '/'});
        }])
        .config(function ($sceProvider) {
            $sceProvider.enabled(false);
        });

    app.factory('web.api.service', apiService);
    apiService.$inject = ['$http'];
    function apiService($http) {
        return {
            getIndex: getIndex,
            getPost: getPost
        };

        function getIndex(params) {
            return $http.get("/api/posts/", {params: params});
        }

        function getPost(params) {
            const _id = params.id;
            return $http.get("/api/posts/" + _id);
        }
    }

    app.controller('IndexController', IndexController);
    IndexController.$inject = ['web.api.service'];

    function IndexController(apiService) {
        const ctrl = this;
        let pageId = location.search.split("=")[1] || 1;

        apiService.getIndex({p: pageId})
            .success(function (data) {
                ctrl.posts = data['posts'];
                ctrl.totalPageInView = data['total_pages_inview'];
                ctrl.lastPage = data['last_page'];
                ctrl.pages = [];
                const currentPage = parseInt(pageId, 10);
                ctrl.currentPage = currentPage;
                let totalPrev = 0;
                for (let i = currentPage; i >= currentPage - Math.floor(ctrl.totalPageInView / 2) && i >= 1; i--) {
                    ctrl.pages.push(i);
                    totalPrev++;
                }
                ctrl.pages.reverse();

                for (let i = currentPage + 1; i <= currentPage + ctrl.totalPageInView - totalPrev; i++) {
                    ctrl.pages.push(i);
                }
            });
        ctrl.posts = [{
            id: "123",
            title: "我是小王子"
        }]
    }

    app.controller('PostController', PostController);
    PostController.$inject = ['web.api.service', '$routeParams'];

    function PostController(apiService, $routeParams) {
        const ctrl = this;

        apiService.getPost({id: $routeParams.id})
            .success(function (data) {
                ctrl.post = data;
            });
    }
}());
