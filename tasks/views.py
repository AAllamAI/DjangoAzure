from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    total_count = tasks.count()
    completed_count = tasks.filter(is_completed=True).count()
    pending_count = total_count - completed_count

    context = {
        "tasks": tasks,
        "total_count": total_count,
        "completed_count": completed_count,
        "pending_count": pending_count,
    }
    return render(request, "tasks/task_list.html", context)


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة المهمة بنجاح.")
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form, "is_edit": False})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل المهمة بنجاح.")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form, "is_edit": True, "task": task})


@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "تم حذف المهمة.")
    return redirect("task_list")


@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("task_list")
