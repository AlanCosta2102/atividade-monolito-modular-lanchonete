from django.http import JsonResponse


def health(request):
    return JsonResponse({
        "status": "UP",
        "application": "monolito-modular-lanchonete"
    })