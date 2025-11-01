from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Student, Staff
from django.db.models import Avg

# ------------------------------
# Common Views
# ------------------------------
def index(request):
    return render(request, 'students/index.html')

def contact(request):
    return render(request, 'students/contact.html')

def about(request):
    return render(request, 'students/about.html')


# ------------------------------
# Student Registration
# ------------------------------
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        class_name = request.POST.get('class_name')
        student_id = request.POST.get('student_id')
        raw_password = request.POST.get('password')

        # Basic validation
        if not email or not raw_password or not name:
            messages.error(request, 'Please fill required fields.')
            return redirect('register')

        # Hash password
        password = make_password(raw_password)

        # Check duplicate email
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        Student.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            class_name=class_name,
            student_id=student_id,
            password=password
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'authentication_r.html')


# ------------------------------
# Login View (Student/Staff/Admin)
# ------------------------------
def login(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''
        print("Login attempt:", email)

        # Quick validation
        if not email or not password:
            messages.error(request, "Please enter email and password.")
            print("Login failed: missing email or password")
            return redirect('login')

        # --- Staff Login (static credentials) ---
        static_email = "staff@school.com"
        static_password = "staff123"

        if email == static_email and password == static_password:
            request.session['staff_logged_in'] = True
            messages.success(request, "Welcome Staff!")
            print("Staff login successful")
            return redirect('staff')

        # --- Student Login (database auth) ---
        student = Student.objects.filter(email=email).first()
        print("Found student:", student)
        if student:
            try:
                valid = check_password(password, student.password)
            except Exception:
                valid = (password == student.password)
            if valid:
                request.session['user_role'] = 'student'
                request.session['user_id'] = student.id
                messages.success(request, f"Welcome back, {student.name}!")
                print("Student login successful")
                return redirect('dashboard')

        # If no valid login
        messages.error(request, "Invalid email or password.")
        print("Login failed: invalid credentials")
        return redirect('login')

    # GET request → render login page
    return render(request, 'authentication.html')
# ------------------------------
# Dashboard routing (common route)
# ------------------------------
def dashboard(request):
    user_role = request.session.get('user_role')
    user_id = request.session.get('user_id')

    if not user_role:
        messages.warning(request, "Please log in first.")
        return redirect('login')

    if user_role == 'admin':
        return render(request, 'admin/admin_dashboard.html')
    elif user_role == 'staff':
        staff = get_object_or_404(Staff, id=user_id)
        return render(request, 'staff/staff_profile.html', {'staff': staff})
    elif user_role == 'student':
        student = get_object_or_404(Student, id=user_id)
        return render(request, 'students/dashboard.html', {'student': student})
    else:
        # unknown role -> logout and force login
        request.session.flush()
        return redirect('login')


# Staff profile view (optional separate route)
def staff(request):
    
    return render(request, 'staff/staff_profile.html', {'staff': staff})

# Admin dashboard (unchanged)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_staff = Staff.objects.count()
    # protect against missing fields on Student (total_fee), use getattr
    total_revenue = sum(getattr(s, 'total_fee', 0) for s in Student.objects.all())
    total_salary = sum(getattr(st, 'salary', 0) for st in Staff.objects.all())
    paid_students = Student.objects.filter(**{}).count()  # placeholder if you don't have fees_paid field
    unpaid_students = max(0, total_students - paid_students)
    avg_attendance = Student.objects.aggregate(Avg('attendance_percentage'))['attendance_percentage__avg'] or 0

    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'total_revenue': total_revenue,
        'total_salary': total_salary,
        'paid_students': paid_students,
        'unpaid_students': unpaid_students,
        'avg_attendance': round(avg_attendance, 2),
        'students': Student.objects.all(),
        'staffs': Staff.objects.all(),
    }
    return render(request, 'admin/admin_dashboard.html', context)

from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('login')