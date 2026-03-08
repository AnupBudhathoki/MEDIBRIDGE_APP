from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserRole, Slot


@login_required(login_url='log_in')
def home(request):
    try:
        user_role = request.user.userrole
    except UserRole.DoesNotExist:
        return redirect('log_in')

    if user_role.role == 'doctor':
        return redirect('ha_home')

    return render(request, 'core/home.html')


@login_required(login_url='log_in')
def ha_home(request):
    try:
        user_role = request.user.userrole
    except UserRole.DoesNotExist:
        return redirect('log_in')

    if user_role.role != 'doctor':
        return redirect('home')

    return render(request, 'core/ha_home.html')


def doctors_list(request):
    doctors = UserRole.objects.filter(role='doctor').select_related('user')
    return render(request, 'doctors.html', {'doctors': doctors})


def appointment_page(request, doctor_id):
    doctor_user = get_object_or_404(User, id=doctor_id)
    profile = get_object_or_404(UserRole, user=doctor_user, role='doctor')
    # Only show available (unbooked) slots for this specific doctor
    slots = Slot.objects.filter(doctor=profile, is_booked=False).order_by('start_time')

    context = {
        'doctor': doctor_user,
        'profile': profile,
        'slots': slots,
    }
    return render(request, 'appoinment_page.html', context)
