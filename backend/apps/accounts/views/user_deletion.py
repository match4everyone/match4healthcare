from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# TODO: make these class based # noqa T003


@login_required
def delete_me(request):
    user = request.user
    logout(request)
    user.delete()
    return render(request, "deleted_user.html")


@login_required
def delete_me_ask(request):
    return render(request, "deleted_user_ask.html")
