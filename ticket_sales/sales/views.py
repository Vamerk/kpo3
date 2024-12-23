from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, Ticket, Client
from .forms import TicketPurchaseForm, TicketFilterForm, TransportType
from django.db.models import Count


def route_list(request):
    # Получаем все виды транспорта для фильтра
    transport_types = TransportType.objects.all()

    # Инициализируем фильтры
    filters = {}
    departure_date = request.GET.get('departure_date')
    destination = request.GET.get('destination')
    transport_type = request.GET.get('transport_type')
    sort_by = request.GET.get('sort_by')

    # Применяем фильтры, только если они заданы
    if departure_date:
        filters['departure_date'] = departure_date
    if destination:
        filters['destination__icontains'] = destination
    if transport_type:
        filters['transport_type_id'] = transport_type

    # Если фильтры не заданы, возвращаем пустой список
    if not filters:
        routes = Route.objects.none()  # Возвращает пустой QuerySet
    else:
        routes = Route.objects.filter(**filters)

    # Применяем сортировку, если она задана
    if sort_by:
        routes = routes.order_by(sort_by)

    return render(request, 'sales/route_list.html', {
        'routes': routes,
        'transport_types': transport_types,
    })

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
            ticket = Ticket.objects.create(route=route, client=client)
            route.available_seats -= 1
            route.save()
            # Передаем ticket.id в redirect
            return redirect('success', ticket_id=ticket.id)
    else:
        form = TicketPurchaseForm()
    return render(request, 'sales/purchase_ticket.html', {'form': form, 'route': route})

def success(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    route = get_object_or_404(Route, id=ticket.route.id)
    return render(request, 'sales/success.html', {'ticket': ticket, 'route': route})

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

    # Группировка по пунктам назначения и видам транспорта
    popular_destinations = tickets.values(
        'route__destination',  # Используем поле destination напрямую
        'route__transport_type__name'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    return render(request, 'sales/report.html', {
        'form': form,
        'tickets_by_transport': tickets_by_transport,
        'popular_destinations': popular_destinations,
    })


def head_page(request):
    return render(request, 'sales/head.html')