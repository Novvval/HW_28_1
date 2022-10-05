import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from HW_28_1 import settings
from ads.models import Ad


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad
    query = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related("author").order_by("price")
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        return JsonResponse(
            {"items": [
                {
                    "id": ad.pk,
                    "name": ad.name,
                    "author": ad.author.username,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "category_id": ad.category_id,
                    "image": ad.image.url if ad.image else None
                }
                for ad in page_object
            ],
                "numb_pages": page_object.paginator.num_pages,
                "total": page_object.paginator.count
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ("name", "author", "price", "description", "is_published", "category",)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ad = Ad.objects.create(
            name=data["name"],
            author=data["author"],
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"]
        )
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ("name", "author", "price", "description", "is_published", "category",)

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.author = data["author"]
        self.object.price = data["price"]
        self.object.description = data["description"]
        self.object.is_published = data["is_published"]

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ("image",)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, status=200, safe=False)