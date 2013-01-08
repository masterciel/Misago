def csrf(request):
    if request.user.is_crawler():
        return {}
    return {
        'csrf_id': request.csrf.csrf_id,
        'csrf_token': request.csrf.csrf_token,
    }
