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

    app.directive('pagination', page);
    function page() {
        var directive = {
            restrict: 'E',
            templateUrl: '/static/views/page.html',
            replace: true,
        };
        return directive;
    }

    app.factory('web.api.service', apiService);
    apiService.$inject = ['$http'];
    function apiService($http) {
        return {
            getIndex: getIndex,
            getPost: getPost,
            removePost: removePost
        };

        function getIndex(params) {
            return $http.get("/api/posts/", {params: params});
        }

        function getPost(params) {
            const _id = params.id;
            return $http.get("/api/posts/" + _id);
        }

        function removePost(id) {
            return $http.delete("/api/posts/" + id);
        }
    }

    app.factory('query.arguments.service', getParameter);

    function getParameter() {
        return {
            getParameterByName: getParameterByName
        };

        function getParameterByName(name, url) {
            if (!url) url = window.location.href;
            name = name.replace(/[\[\]]/g, "\\$&");
            var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, " "));
        }
    }

    app.controller('IndexController', IndexController);
    IndexController.$inject = ['web.api.service', 'query.arguments.service'];

    function IndexController(apiService, getParameter) {
        const ctrl = this;
        let pageId = getParameter.getParameterByName('p') || 1;
        let query = getParameter.getParameterByName('q') || null;
        ctrl.query = query;

        apiService.getIndex({ p: pageId, q: query })
            .success(function (data) {
                ctrl.posts = data['posts'];
                ctrl.totalPageInView = data['total_pages_inview'];
                ctrl.lastPage = data['last_page'];
                ctrl.pages = [];
                const currentPage = parseInt(pageId, 10);
                ctrl.currentPage = currentPage;
                let totalPrev = 0;

                if (currentPage === ctrl.lastPage) {
                    for (let i = ctrl.lastPage; i > ctrl.lastPage - ctrl.totalPageInView; i--)
                    ctrl.pages.push(i);
                    totalPrev++;
                }
                else {
                    for (let i = currentPage; i >= currentPage - Math.floor(ctrl.totalPageInView / 2) && i >= 1; i--) {
                        ctrl.pages.push(i);
                        totalPrev++;
                    }
                }
                ctrl.pages.reverse();

                for (let i = currentPage + 1; i <= currentPage + ctrl.totalPageInView - totalPrev && i <= ctrl.lastPage; i++) {
                    ctrl.pages.push(i);
                }
            });
        ctrl.posts = [{
            id: "123",
            title: "我是小王子"
        }]
    }

    app.controller('PostController', PostController);
    PostController.$inject = ['web.api.service', '$routeParams', '$location', '$timeout'];

    function PostController(apiService, $routeParams, $location, $timeout) {
        const ctrl = this;

        ctrl.removePost = function (id) {
            apiService.removePost(id)
                .success(function () {
                    $(".modal.confirm").modal('hide');
                    toastr.success('删除成功，即将跳转到首页');
                    $timeout(function () {
                        location.href = "/";
                    }, 1000);
                })
                .error(function () {
                    toastr.error('删除失败');
                });
        }

        apiService.getPost({id: $routeParams.id})
            .success(function (data) {
                ctrl.post = data;
            })
            .error(function (data, status, headers, config) {
                if (status === 404) {
                    $location.url("/");
                }
            });
    }
}());
