from random import sample

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


from tours.data import departures, tours


def main_view(request):
    context = {
        'tours': {id_tour: tours[id_tour] for id_tour in sample(list(tours), 6)}
        }
    return render(request, 'tours/index.html', context)


def departure_view(request, departure):
    tours_and_departure = {id_tour: tour_item for id_tour, tour_item in tours.items() if
                            tour_item['departure'] == departure}
    context = {
            'tours': tours_and_departure,
            'departure_addres': departures[departure],
            'total_tours': len(tours_and_departure),
            'min_price': new_price(min_price(tours_and_departure, 'price')),
            'max_price': new_price(max_price(tours_and_departure, 'price')),
            'min_nights': min_price(tours_and_departure, 'nights'),
            'max_nights': max_price(tours_and_departure, 'nights'),
            }
    return render(request, 'tours/departure.html', context)


def tour_view(request, id_tour):
    tour = tours[id_tour]
    context = {
            'stars_string': '★' * int(tour['stars']),
            'tour': tour,
            'departure': departures[tour['departure']],
            }
    return render(request, 'tours/tour.html', context)

def max_price(data_dict, param):
    return max([data_dict[key][param] for key in data_dict])


def min_price(data_dict, param):
    return min([data_dict[key][param] for key in data_dict])


def new_price(price):
    price = str(price)[::-1]
    return ' '.join(price[i:i + 3] for i in range(0, len(price), 3))[::-1]

def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
