#from django.views import ListView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product

# Create your views here.

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "wandsproducts/list.html"

#    def get_context_data(self, *args, **kwargs):
#        context = super(ProductListView, self).get_context_data(*args, **kwargs)
#        print(context)
#        return context



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "wandsproducts/list.html", context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "wandsproducts/detail.html"

#    def get_context_data(self, *args, **kwargs):
#        context = super(ProductListView, self).get_context_data(*args, **kwargs)
#        print(context)
#        return context

#class ProductDetailView(DetailView):
#    template_name = 'wandsproducts/detail.html'
#    queyset = Post.Objects.all()

#    def get_object(self, *args, **kwargs):
#        url_id = self.kwargs.get("id") #regex id
#        return get_object_or_404(Post, id=url_id)
#def product_detail_view(request, id, *args, **kwrgs):
#    return render(request, template_name, {})



def product_detail_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "wandsproducts/detail.html", context)
