from .endpoints import operation_paths

VOLATILE_OPERATIONS = ["parttos:get"]


class Headers:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/"):
            return response
        if request.method.lower() != "get":
            return response
        for operation in VOLATILE_OPERATIONS:
            path = operation_paths[operation]
            if request.path.strip("/") == path.strip("/"):
                return response
        response["Cache-Control"] = (
            "public, max-age=31536000, immutable"
        )
        return response
