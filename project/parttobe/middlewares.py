from .endpoints import operation_paths
from re import search


cache_for_path = {}


def set_cache_for_paths(expressions, cache):
    for expression in expressions:
        for operationId, path in operation_paths.items():
            if not search(expression, operationId):
                continue
            cache_for_path[path.strip("/")] = cache


# keep for duration of use
set_cache_for_paths(["metric:get$"], "max-age=10800, must-revalidate")

# keep forever
set_cache_for_paths(
    ["^partto:get$", "^task:get$", "^run.*:get$"],
    "public, max-age=31536000, immutable",
)


class Headers:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/"):
            return response
        if request.method.lower() != "get":
            return response
        if request.path.strip("/") in cache_for_path:
            response["Cache-Control"] = cache_for_path[
                request.path.strip("/")
            ]
        return response
