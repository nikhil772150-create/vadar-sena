class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin", "*")
        
        if request.method == "OPTIONS":
            from django.http import HttpResponse
            response = HttpResponse(status=200)
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-Requested-With, Accept, Origin"
            response["Access-Control-Allow-Credentials"] = "true"
            return response

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = origin
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-Requested-With, Accept, Origin"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
