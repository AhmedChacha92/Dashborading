from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .models import Mission, Complaint, Consultant
from .forms import MissionForm, ComplaintForm, ConsultantCreationForm, LoginForm, PasswordResetForm, AssignMissionForm

#creation des vues pour les missions et les utilisateurs afin de les afficher 
#ces vues auron pour but de permettre a l'utilisateur de voir les missions et les utilisateurs

#le login_required permet de verifier si l'utilisateur est connecté ou pas avant d'acceder a la page
# @login_required

def dashboard(request):
    missions = Mission.objects.all()
    total_budget = sum(mission.budget_per_day for mission in missions)
    return render(request, 'missions/dashboard.html', {'missions': missions, 'total_budget': total_budget})

def list_missions(request):
    missions = Mission.objects.all()
    form = MissionForm()
    return render(request, 'missions/list_missions.html', {'missions': missions, 'form': form})

def user_missions(request):
    if request.user.is_authenticated:
        missions = request.user.missions.all()
    else:
        missions = []
    return render(request, 'missions/user_missions.html', {'missions': missions})

def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    return render(request, 'missions/mission_detail.html', {'mission': mission})

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

def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            mission = form.save()
            if request.is_ajax():
                return JsonResponse({
                    'success': True,
                    'mission': {
                        'id': mission.id,
                        'name': mission.name,
                        'type': mission.type,
                        'budget_per_day': str(mission.budget_per_day),
                        'end_date': mission.end_date.strftime('%Y-%m-%d'),
                    }
                })
            return redirect('dashboard')
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MissionForm()
    return render(request, 'missions/create_mission.html', {'form': form})

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

def delete_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    if request.method == 'POST':
        mission.delete()
        return redirect('dashboard')
    return render(request, 'missions/delete_mission.html', {'mission': mission})

def register(request):
    if request.method == 'POST':
        form = ConsultantCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = ConsultantCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = Consultant.objects.filter(email=email).first()
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'registration/password_reset.html', {'form': form, 'error': 'Email not found'})
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset.html', {'form': form})


def home(request):
    return render(request, 'missions/base.html')