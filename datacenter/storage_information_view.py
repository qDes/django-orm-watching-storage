from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration

from django.shortcuts import render
from django.utils import timezone

import pytz

def storage_information_view(request):
    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
        tmp = {
                "who_entered": visit.passcard,
                "entered_at": visit.entered_at,
                "duration": format_duration(visit.get_duration()),
                "is_strange": visit.is_visit_long()
        }
        non_closed_visits.append(tmp)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
