from django.contrib import admin

from airport.models import (
    Airport,
    Order,
    Ticket,
    Airplane,
    AirplaneType,
    Route,
    Crew,
    Flight,
)

admin.site.register(Airport)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Route)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Ticket)
