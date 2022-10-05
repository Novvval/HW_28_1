import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from HW_28_1 import settings
from ads.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User
    query = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.filter(ad__is_published=True).annotate(total_ads=Count("ad"))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        return JsonResponse({
            "items": [
                {
                    "id": user.pk,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role,
                    "age": user.age,
                    "locations": list(map(str, user.location_id.all())),
                    "total_ads": user.total_ads
                } for user in page_object
            ],
            "num_pages": page_object.paginator.num_pages,
            "total": page_object.paginator.count
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.location_id.all()))
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ("first_name", "last_name", "username", "password", "role", "age", "locations")

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            first_name=data["name"],
            last_name=data["author"],
            username=data["price"],
            password=data["description"],
            role=data["is_published"],
            age=data["age"],
            locations=data["locations"]
        )
        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.location_id.all()))
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ("first_name", "last_name", "username", "password", "role", "age", "locations")

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.first_name = data["first_name"]
        self.object.last_name = data["last_name"]
        self.object.username = data["username"]
        self.object.password = data["password"]
        self.object.role = data["role"]
        self.object.age = data["age"]
        self.object.locations = data["locations"]

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.location_id.all()))
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({}, status=204)
