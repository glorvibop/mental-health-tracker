from django.shortcuts import render

# Create views here
def show_main(request):
    context = {
        'npm' : '2306245573',
        'name': 'Shaine Glorvina Mathea',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)