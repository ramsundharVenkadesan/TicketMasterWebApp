from django.shortcuts import render
from .forms import *
import requests
from django.views import View
from datetime import datetime
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

API_KEY:str = "11QISoj5UVR4B1nzygy015Vg5ZhxgLyb"

class DashboardView(View):
    def get(self, request):
        form_data = Search(request.GET)
        events, error = [], str()
        if form_data.is_valid():
            genre = form_data.cleaned_data['genre']
            city = form_data.cleaned_data['city']

            url = "https://app.ticketmaster.com/discovery/v2/events.json"
            params = { "apikey": API_KEY, "keyword": genre, "city": city, "size": 20}

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()

                try:
                    for event in data['_embedded']['events']:
                        venue = event['_embedded']['venues'][0]
                        raw_time = event['dates']['start'].get('localTime')

                        if raw_time:
                            try:
                                formatted_time = datetime.strptime(raw_time, "%H:%M:%S").strftime("%I:%H %p")
                                pass
                            except ValueError:
                                formatted_time = raw_time
                        else: formatted_time = "TBA"

                        item = {
                            "event_id": event['id'], "name": event['name'], "venue": venue['name'],
                            "address": venue['address'].get("line1", ""), "city": venue['city']['name'], "state": venue.get("state", {}).get("name", ""),
                            "date": event["dates"]["start"].get("localDate", "TBA"), "time": formatted_time,
                            "image": event["images"][0]["url"], "event_url": event['url']
                        }
                        events.append(item)
                    events.sort(key=lambda x: x['date'])
                except KeyError: error = "No Events Found!"
            else: error = "TicketMaster API Failure!"
        return render(request, "ticketmaster/index.html", {"form": form_data, "events": events, "error": error})

    def post(self, request):
        form_data = Save(request.POST)
        if form_data.is_valid():
            record = form_data.cleaned_data['event_id']
            if not Event.objects.filter(event_id=record).exists():
                form_data.save()
                return HttpResponseRedirect(reverse("favorites"))
            else:
                return HttpResponseRedirect(reverse("favorites"))
        else:
            return HttpResponseRedirect(reverse("dashboard"))


class SavedEvents(ListView):
    model = Event
    context_object_name = "events"
    template_name = "ticketmaster/favorites.html"

    def get_queryset(self):
        base_query = super(SavedEvents, self).get_queryset()
        return base_query.all()


class DeleteEvent(View):
    def post(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
            event.delete()
        except Event.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse("favorites"))

