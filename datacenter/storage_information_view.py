from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from datacenter.models import change_timezone_msc

from django.shortcuts import render
from django.utils import timezone

import pytz



def storage_information_view(request):
    # Программируем здесь
    now = change_timezone_msc(timezone.now())
    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
        tmp = {}
        tmp["who_entered"] = visit.passcard
        tmp["entered_at"] = change_timezone_msc(visit.entered_at)
        tmp["duration"] = format_duration(visit.get_duration())
        tmp["is_strange"] = visit.is_visit_long()
        non_closed_visits.append(tmp)


    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
