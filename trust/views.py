from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, Subcategory, Category
from .forms import PersonForm
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class PersonListView(ListView):
    model = Person
    context_object_name = 'people'


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')


def load_subcat(request):
    category_id = request.GET.get('category')
    subcategory = Subcategory.objects.filter(catid_id=category_id).order_by('name')
    return render(request, 'trust/subcategory_dropdown.html', {'subcategory': subcategory})




def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(

                model=Category,
                mapdict=['name'])
            return redirect('person_changelist')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'trust/import.html',
        {'form': form,
         'title': 'Import excel data into database example',
         'header': 'Please upload sample-data.xls:'
         })
