from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'dimension/index.html')
def dimension(request):
    return render(request,'dimension/index.html')
def hackoverflow(request):
    return render(request,'dimension/hackoverflow.html')