#from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product

# Create your views here.


class ProductFeaturedListView(ListView):
    template_name = "wandsproducts/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "wandsproducts/featured-detail.html"


class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "wandsproducts/list.html"

#    def get_context_data(self, *args, **kwargs):
#        context = super(ProductListView, self).get_context_data(*args, **kwargs)
#        print(context)
#        return context
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "wandsproducts/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "wandsproducts/detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #item_instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            item_instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found.")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            item_instance = qs.first()
        except:
            raise Http404("Rare case slug error.")

        return item_instance


class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "wandsproducts/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        item_instance = Product.objects.get_by_id(pk)
        if item_instance is None:
            raise Http404("Product does not exist.")
        return item_instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)



#class ProductDetailView(DetailView):
#    template_name = 'wandsproducts/detail.html'
#    queyset = Post.Objects.all()

#    def get_object(self, *args, **kwargs):
#        url_id = self.kwargs.get("id") #regex id
#        return get_object_or_404(Post, id=url_id)
#def product_detail_view(request, id, *args, **kwrgs):
#    return render(request, template_name, {})



def product_detail_view(request, pk=None, *args, **kwargs):
    #item_instance = Product.objects.get(pk=pk, featured=True) #product id
    #item_instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     item_instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('Product does not exist.')
    #     raise Http404("Product does not exist.")
    # except:
    #     print('Unknown error.')

    item_instance = Product.objects.get_by_id(pk)
    if item_instance is None:
        raise Http404("Product does not exist.")

    # qs = Product.objects.filter(id=pk)
    #
    # if qs.exists() and qs.count() == 1:
    #     item_instance = qs.first()
    # else:
    #     raise Http404("Product does not exist.")

    context = {
        'object_list': item_instance
    }
    return render(request, "wandsproducts/detail.html", context)
