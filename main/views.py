from django.shortcuts import render, redirect
from main.forms import MoodEntryForm
from main.models import MoodEntry
from django.http import HttpResponse
from django.core import serializers

# Create views here
def show_main(request):
    mood_entries = MoodEntry.objects.all()

    context = {
        'name': 'Shaine Glorvina Mathea',
        'class': 'PBP B',
        'npm': '2306245573',
        'mood_entries': mood_entries
    }

    return render(request, "main.html", context)

# Menghasilkan form yang dapat menambahkan data Mood Entry secara otomatis ketika data di-submit dari form
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
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