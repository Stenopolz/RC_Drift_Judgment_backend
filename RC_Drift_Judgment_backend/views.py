from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Pilot, RaceMark, MARK_CHOICES
from .serializers import PilotSerializer


def home(request):
    raise Http404()


def pageResults(request):
    return render_to_response(
        "results.html",
        {},
        RequestContext(request, {}),
    )


@login_required
def pageJudge(request):

    return render_to_response(
        "judge.html",
        {'marks': MARK_CHOICES},
        RequestContext(request, {}),
    )
