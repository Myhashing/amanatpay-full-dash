from django.shortcuts import render, redirect
from auth.views import AuthView


class CheckTestView(AuthView):

    template_name = 'layout/layout_blank.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")

        return super().get(request)
