from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import time

from .models import UserRole, HealthReport, Slot
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            role = form.cleaned_data['role']

            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match.')
                return render(request, 'register.html', {'form': form})

            if User.objects.filter(username=email).exists():
                form.add_error('email', 'Email is already registered.')
                return render(request, 'register.html', {'form': form})

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            UserRole.objects.create(user=user, phone=phone, role=role)

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('log_in')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'log_in.html', {'error': 'Invalid email or password.'})

    return render(request, 'log_in.html')


def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='log_in')
def pat_profile(request):
    try:
        user_role = request.user.userrole
    except UserRole.DoesNotExist:
        return redirect('log_in')

    if user_role.role != 'patient':
        return redirect('home')

    health_reports = HealthReport.objects.filter(patient=request.user).order_by('-created_at')
    return render(request, 'pat_profile.html', {
        'profile': user_role,
        'health_reports': health_reports,
    })


@login_required(login_url='log_in')
def ha_profile(request):
    try:
        user_role = request.user.userrole
    except UserRole.DoesNotExist:
        return redirect('log_in')

    if user_role.role != 'doctor':
        return redirect('home')

    # Only this doctor's slots
    slots = Slot.objects.filter(doctor=user_role).order_by('start_time')

    context = {
        'doctor': request.user,
        'profile': user_role,
        'available_slots': slots,
    }
    return render(request, 'ha_profile.html', context)


@login_required(login_url='log_in')
def add_slot(request):
    if request.method == 'POST':
        try:
            doctor = request.user.userrole
            if doctor.role != 'doctor':
                messages.error(request, "Only doctors can add slots.")
                return redirect('home')

            # Parse start time
            sh = int(request.POST.get('start_hour', 0))
            sm = int(request.POST.get('start_minute', 0))
            sp = request.POST.get('start_period', 'AM')
            if sp == 'PM' and sh != 12:
                sh += 12
            if sp == 'AM' and sh == 12:
                sh = 0
            start_time = time(sh, sm)

            # Parse end time
            eh = int(request.POST.get('end_hour', 0))
            em = int(request.POST.get('end_minute', 0))
            ep = request.POST.get('end_period', 'AM')
            if ep == 'PM' and eh != 12:
                eh += 12
            if ep == 'AM' and eh == 12:
                eh = 0
            end_time = time(eh, em)

            fee = float(request.POST.get('fee', 0))

            if end_time <= start_time:
                messages.error(request, "End time must be after start time.")
                return redirect('ha_profile')

            if end_time > time(14, 0):
                messages.error(request, "End time cannot be after 2:00 PM.")
                return redirect('ha_profile')

            Slot.objects.create(
                doctor=doctor,
                start_time=start_time,
                end_time=end_time,
                fee=fee,
            )
            messages.success(request, "Slot added successfully!")

        except Exception as e:
            messages.error(request, f"Error adding slot: {str(e)}")

    return redirect('ha_profile')


@login_required(login_url='log_in')
def remove_slot(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        # Only allow the owning doctor to remove their own slot
        slot = get_object_or_404(Slot, id=slot_id, doctor=request.user.userrole)
        slot.delete()
        messages.success(request, "Slot removed.")
    return redirect('ha_profile')


@login_required(login_url='log_in')
def health_status(request):
    health_reports = HealthReport.objects.filter(patient=request.user).order_by('-created_at')
    return render(request, 'profile_status/health_status.html', {'health_reports': health_reports})


@login_required(login_url='log_in')
def view_appointment(request):
    return render(request, 'doctors/view_appoinment.html')
