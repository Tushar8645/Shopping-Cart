from django.conf.urls import url
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # print(request.path.split('/')[1])
        next = request.path.split('/')[1]

        if not request.session.get('customer'):
            # return redirect('store:login')
            return HttpResponseRedirect('store:login')
            # return HttpResponseRedirect('login?next={}'.format(next))
        else:
            response = get_response(request)

            return response

    return middleware
