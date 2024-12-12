from django.db import models

class TransportType(models.Model):
    name = models.CharField(max_length=100)  # Название вида транспорта (самолет, поезд и т.д.)

    def __str__(self):
        return self.name

class Route(models.Model):
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    departure_location = models.CharField(max_length=100)  # Пункт отправления
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    destination = models.CharField(max_length=100)  # Пункт назначения
    total_seats = models.IntegerField()  # Общее количество мест
    available_seats = models.IntegerField()  # Количество свободных мест
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена билета

    def __str__(self):
        return f"{self.transport_type} from {self.departure_location} to {self.destination} on {self.departure_date}"

class Client(models.Model):
    full_name = models.CharField(max_length=200)  # ФИО клиента
    passport_series = models.CharField(max_length=10)  # Серия паспорта
    passport_number = models.CharField(max_length=10)  # Номер паспорта

    def __str__(self):
        return self.full_name

class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)  # Дата покупки билета

    def __str__(self):
        return f"Ticket for {self.client.full_name} on {self.route}"