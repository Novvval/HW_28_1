import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ads.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category
    query = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        response = []
        for category in self.object_list:
            response.append({
                "id": category.pk,
                "name": category.name,
            })
        return JsonResponse(response, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category.objects.create(
            name=data["name"]
        )
        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ("name",)

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({}, status=204)