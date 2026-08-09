from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Grade, Subject


def journal_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # 1. Додавання учня
        if action == 'add_student':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            description = request.POST.get('description', '')
            if first_name and last_name:
                Student.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    description=description
                )
            return redirect('journal')

        # 2. Додавання оцінки (1-100)
        elif action == 'add_grade':
            student_id = request.POST.get('student_id')
            score = request.POST.get('score')
            if student_id and score:
                student = get_object_or_404(Student, id=student_id)
                subject, _ = Subject.objects.get_or_create(name="Програмування")
                score_int = int(score)
                if 1 <= score_int <= 100:
                    Grade.objects.create(student=student, subject=subject, score=score_int)
            return redirect('journal')

        # 3. Видалення учня
        elif action == 'delete_student':
            student_id = request.POST.get('student_id')
            if student_id:
                student = get_object_or_404(Student, id=student_id)
                student.delete()
            return redirect('journal')

        # 4. Видалення оцінки
        elif action == 'delete_grade':
            grade_id = request.POST.get('grade_id')
            if grade_id:
                grade = get_object_or_404(Grade, id=grade_id)
                grade.delete()
            return redirect('journal')

    students = Student.objects.prefetch_related('grades').all()
    return render(request, 'journal.html', {'students': students})