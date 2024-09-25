from django.shortcuts import render, redirect, reverse
from main.forms import MoodEntryForm
from main.models import MoodEntry
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create views here
@login_required(login_url='/login') # Only for users that logged in successfully
def show_main(request):
    mood_entries = MoodEntry.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'name': 'Shaine Glorvina Mathea',
        'class': 'PBP B',
        'npm': '2306245573',
        'mood_entries': mood_entries,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

# Menghasilkan form yang dapat menambahkan data Mood Entry secara otomatis ketika data di-submit dari form
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)

# Menyimpan hasil query dari seluruh data yang ada pada MoodEntry
def show_xml(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Menyimpan hasil query dari seluruh data yang ada pada MoodEntry
def show_json(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Menyimpan hasil query dari data dengan id tertentu yang ada pada MoodEntry
def show_xml_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Menyimpan hasil query dari data dengan id tertentu yang ada pada MoodEntry
def show_json_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Menghasilkan formulir registrasi secara otomatis dan menghasilkan akun pengguna ketika data di-submit dari form
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

# Mengautentikasi pengguna yang ingin login
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

# Melakukan mekanisme logout
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Menambahkan fitur edit mood pada aplikasi
def edit_mood(request, id):
    # Get mood entry berdasarkan id
    mood = MoodEntry.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = MoodEntryForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_mood.html", context)

# Menambahkan fitur delete mood pada aplikasi
def delete_mood(request, id):
    # Get mood berdasarkan id
    mood = MoodEntry.objects.get(pk = id)
    # Hapus mood
    mood.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))