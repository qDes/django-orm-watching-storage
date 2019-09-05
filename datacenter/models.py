from django.db import models
from django.utils import timezone
import pytz
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
    
    def get_duration(self) -> datetime.timedelta:
        if self.leaved_at == None:
            return timezone.now() - self.entered_at
        return self.leaved_at - self.entered_at
    
    def is_visit_long(self, minutes: int = 60) -> bool:
        duration_minutes = self.get_duration().total_seconds()/60
        if duration_minutes > minutes:
            return True
        return False


def format_duration(duration:datetime.timedelta) -> str:
    seconds = duration.total_seconds()
    hrs = int(seconds // 3600)
    minutes = int(seconds % 3600 / 60)
    formated = str(hrs) + " ч " + str(minutes) + " мин"
    return formated

def change_timezone_msc(date:datetime.datetime) -> datetime.datetime:

    if date == None:
        return None
    local_tz = pytz.timezone("Europe/Moscow")
    local_date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_date
