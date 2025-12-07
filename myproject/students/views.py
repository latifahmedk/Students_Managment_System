from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, StudentHistory
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    students = Student.objects.all()
    return render(request, "index.html", {"students": students})

@login_required
def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            student_number=request.POST['student_number'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            field_of_study=request.POST['field_of_study'],
            gpa=request.POST['gpa']
        )
        return redirect("index")
    return render(request, "add.html")

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == "POST":
        student.student_number = request.POST['student_number']
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.email = request.POST['email']
        student.field_of_study = request.POST['field_of_study']
        student.gpa = request.POST['gpa']
        student.save()
        return redirect("index")
    
    return render(request, "edit.html", {"student": student})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    # Save to history before deletion
    StudentHistory.objects.create(
        student_number=student.student_number,
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        field_of_study=student.field_of_study,
        gpa=student.gpa,
    )

    student.delete()
    return redirect("index")


@login_required
def history(request):
    deleted_students = StudentHistory.objects.order_by('-deleted_at')
    return render(request, "history.html", {"history": deleted_students})


def restore_student(request, id):
    deleted = get_object_or_404(StudentHistory, id=id)

    # Move back to main table
    Student.objects.create(
        student_number=deleted.student_number,
        first_name=deleted.first_name,
        last_name=deleted.last_name,
        email=deleted.email,
        field_of_study=deleted.field_of_study,
        gpa=deleted.gpa
    )

    deleted.delete()
    return redirect("history")


def permanent_delete(request, id):
    deleted = get_object_or_404(StudentHistory, id=id)
    deleted.delete()
    return redirect("history")
