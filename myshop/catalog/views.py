from django.http import HttpResponse, Http404

#baza
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1800},
    {"id": 2, "name": "Headphones", "price": 1500},
    {"id": 3, "name": "Mouse", "price": 40},
]

def home(request):
    return HttpResponse('<h1>myshop</h1><a href="/products/">პროდუქტების სია</a>')

def about(request):
    return HttpResponse('ეს არის myshop პროექტი, შექმნილი Django-ს შესასწავლად.')

def product_list(request):
    items = "".join([
        f'<li><a href="/products/{p["id"]}/">{p["name"]}</a>: {p["price"]} ₾</li>'
        for p in PRODUCTS
    ])
    html = f'<ul>{items}</ul>'
    return HttpResponse(html)

def product_detail(request, pk):
    product = next((p for p in PRODUCTS if p["id"] == pk), None)

    if product is None:
        raise Http404("პროდუქტი ვერ მოიძებნა")

    html = f'<h1>{product["name"]}</h1><p>ფასი: {product["price"]} ₾</p>'
    return HttpResponse(html)