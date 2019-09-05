from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import format_duration
from datacenter.models import change_timezone_msc

def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    
    for visit in visits:
        passcard_visit = {}
        passcard_visit["entered_at"] = change_timezone_msc(visit.entered_at)
        passcard_visit["duration"] = format_duration(visit.get_duration())
        passcard_visit["is_strange"] = visit.is_visit_long()
        this_passcard_visits.append(passcard_visit)
    
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
