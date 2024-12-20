from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, Ticket, Client
from .forms import TicketPurchaseForm, TicketFilterForm
from django.db.models import Count


def route_list(request):
    routes = Route.objects.all()
    return render(request, 'sales/route_list.html', {'routes': routes})

def adout_page(request):
    return render(request, 'sales/about.html')

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
    # Инициализация формы фильтрации
    form = TicketFilterForm(request.GET)
    tickets = Ticket.objects.all()

    # Применение фильтров, если форма валидна
    if form.is_valid():
        transport_type = form.cleaned_data.get('transport_type')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if transport_type:
            tickets = tickets.filter(route__transport_type=transport_type)
        if start_date:
            tickets = tickets.filter(purchase_date__gte=start_date)
        if end_date:
            tickets = tickets.filter(purchase_date__lte=end_date)

    # Группировка по типу транспорта
    tickets_by_transport = tickets.values('route__transport_type__name').annotate(total=Count('id'))

    return render(request, 'sales/report.html', {
        'form': form,
        'tickets_by_transport': tickets_by_transport,
    })