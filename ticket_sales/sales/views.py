from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, Ticket, Client
from .forms import TicketPurchaseForm
from django.db.models import Count


def route_list(request):
    routes = Route.objects.all()
    return render(request, 'sales/route_list.html', {'routes': routes})

def purchase_ticket(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            client = Client.objects.create(
                full_name=form.cleaned_data['full_name'],
                passport_series=form.cleaned_data['passport_series'],
                passport_number=form.cleaned_data['passport_number']
            )
            Ticket.objects.create(route=route, client=client)
            route.available_seats -= 1
            route.save()
            return redirect('success')
    else:
        form = TicketPurchaseForm()
    return render(request, 'sales/purchase_ticket.html', {'form': form, 'route': route})

def success(request):
    return render(request, 'sales/success.html')

def report(request):
    tickets_by_transport = Ticket.objects.values('route__transport_type__name').annotate(total=Count('id'))
    return render(request, 'sales/report.html', {'tickets_by_transport': tickets_by_transport})