from django.contrib import admin
from .models import TransportType, Route, Client, Ticket

admin.site.register(TransportType)
admin.site.register(Route)
admin.site.register(Client)
admin.site.register(Ticket)