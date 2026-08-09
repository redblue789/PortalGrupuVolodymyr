from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    grade_level = models.CharField(max_length=50, default="Logika", verbose_name="Клас")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")

    class Meta:
        verbose_name = "Учень"
        verbose_name_plural = "Учні"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Subject(models.Model):
    name = models.CharField(max_length=100, default="Програмування", verbose_name="Назва предмета")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="Учень"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Оцінка"
    )
    date_added = models.DateField(auto_now_add=True, verbose_name="Дата отримання")

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"

    def __str__(self):
        return f"{self.student}: {self.score}"