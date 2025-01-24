from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Mission, Complaint
from .forms import MissionForm, ComplaintForm
#creation des vues pour les missions et les utilisateurs afin de les afficher 
#ces vues auron pour but de permettre a l'utilisateur de voir les missions et les utilisateurs

#le login_required permet de verifier si l'utilisateur est connecté ou pas avant d'acceder a la page
# @login_required
def dashboard(request):
    missions = Mission.objects.all()#recuperation de toutes les missions
    total_budget = sum(mission.budget_per_day for mission in missions)#calcul du budget total
    return render(request, 'missions/dashboard.html', {'missions': missions, 'total_budget': total_budget})

# @login_required
def user_missions(request):
    missions = request.user.missions.all()
    return render(request, 'missions/user_missions.html', {'missions': missions})

# @login_required
def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    return render(request, 'missions/mission_detail.html', {'mission': mission})

# @login_required
def create_complaint(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.mission = mission
            complaint.user = request.user
            complaint.save()
            return redirect('mission_detail', mission_id=mission.id)
    else:
        form = ComplaintForm()
    return render(request, 'missions/create_complaint.html', {'form': form, 'mission': mission})

def list_missions(request):
    missions = Mission.objects.all()
    return render(request, 'missions/list_missions.html', {'missions': missions})

# @login_required
def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MissionForm()
    return render(request, 'missions/create_mission.html', {'form': form})

# @login_required
def edit_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return redirect('mission_detail', mission_id=mission.id)
    else:
        form = MissionForm(instance=mission)
    return render(request, 'missions/edit_mission.html', {'form': form, 'mission': mission})

# @login_required
def delete_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    if request.method == 'POST':
        mission.delete()
        return redirect('dashboard')
    return render(request, 'missions/delete_mission.html', {'mission': mission})


def login(request):
    
    return render(request, 'missions/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'missions/register.html', {'form': form})

def home(request):
    return render(request, 'missions/base.html')