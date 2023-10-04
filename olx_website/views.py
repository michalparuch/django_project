from django.http import HttpResponse
from django.views.generic import  View, CreateView, UpdateView, DeleteView, FormView
from olx_website import models
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

from olx_website import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from olx_website import filters
from .models import Room, Message, Item
from .forms import ChatMessage
# Create your views here.

def test(request):
    return HttpResponse('Siema')

def homepage(request):
    items = models.Item.objects.all().order_by('-created_at')[:14]

    return render(request, 'home_page.html', context={
        'items':items,
    })


class ItemDetailView(View):
    def get(self, request, pk):
        item = get_object_or_404(models.Item, pk=pk)
        return render(request, 'item-detail.html', context={'item': item})


class UserCreateView(CreateView):
    success_url = reverse_lazy('login')
    template_name = 'CreateUser.html'
    form_class = forms.SignUpForm
    model = User


@login_required
def item_create_view(request):
    if request.method == 'POST':
        form = forms.AddNewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            print(form.cleaned_data)
            item.save()

            return redirect('item-detail', pk=item.id)
    else:
        form = forms.AddNewItemForm()

    return render(request, 'CreateItem.html', context={
        'form': form,
    })

class EditItemView(LoginRequiredMixin, UpdateView):
    model = models.Item
    form_class = forms.EditItemForm
    template_name = 'edit_item.html'
    success_url = reverse_lazy('item-detail')

    def get_success_url(self):
        return reverse_lazy('item-detail', kwargs={'pk': self.object.pk})

@login_required
def DeleteItem(request, pk):
    item = get_object_or_404(models.Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('home-page')

@login_required
def dashboard(request):
    items = models.Item.objects.filter(created_by=request.user)
    item_count = items.count()

    return render(request, 'dashboard.html', context={
        'items': items,
        'item_count': item_count
    })


@login_required
def custom_logout(request):
    logout(request)

    return redirect('home-page')


class CustomLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home-page')


def sport_category(request):
    items = models.Item.objects.filter(category__name='Sport')

    return render(request, 'sport_category.html', context={
        'items': items,
    })

def clothes_category(request):
    items = models.Item.objects.filter(category__name='Clothes')

    return render(request, 'clothes_category.html', context={
        'items': items,
    })

def electronics_category(request):
    items = models.Item.objects.filter(category__name='Electronics')

    return render(request, 'electronics_category.html', context={
        'items': items,
    })

def browse(request):
    items = models.Item.objects.all()

    myFilter = filters.OrderFilters(request.GET, queryset=items)
    items = myFilter.qs

    if 'reset' in request.GET:
        myFilter = filters.OrderFilters(queryset=items)
        items = myFilter.qs

    return render(request, 'browse.html', context={
        'items': items,
        'myFilter': myFilter,
    })

@login_required
def new_room(request, pk):
    item = get_object_or_404(Item, pk=pk)

    room = Room.objects.filter(item=item, seller=item.created_by, buyer=request.user).first()
    if room:
        return redirect('room_detail', pk=room.pk)

    if request.method == 'POST':
        form = forms.ChatMessage(request.POST)

        if form.is_valid():
            room = Room.objects.create(item=item, seller=item.created_by, buyer=request.user)
            room.save()

            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()

            return redirect('room_detail', pk=room.pk)
    else:
        form = forms.ChatMessage()

    return render(request, 'new.html', context=
    {'form': form})

def room_list(request):
    seller_rooms = Room.objects.filter(seller=request.user)
    buyer_rooms = Room.objects.filter(buyer=request.user)

    return render(request, 'room_list.html', context=
    {'seller_rooms': seller_rooms, 'buyer_rooms': buyer_rooms})

@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = forms.ChatMessage(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()

            return redirect('room_detail', pk=pk)
    else:
        form = forms.ChatMessage()

    messages = Message.objects.filter(room=room)
    return render(request, 'room_detail.html', context=
    {'messages': messages, 'form': form})
