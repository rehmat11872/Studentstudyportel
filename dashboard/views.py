from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.views import generic
# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Note(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")    
    else:
        form = NotesForm()
    notes = Note.objects.filter(user=request.user)
    context = {
        'notes': notes,
        'form': form,
    }
    return render(request, 'dashboard/notes.html', context)    


def delete_note(request, pk=None):
    Note.objects.get(id=pk).delete()
    return redirect('notes')   

class NotesDetailView(generic.DetailView):
    model = Note   
    template_name = 'dashboard/notes_detail.html'


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )  
            homeworks.save() 
            messages.success(request,f"Homework Added from {request.user.username} Successfully")
    else: 
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    # homework_done = 0
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homeworks,
        'homework_done': homework_done,
        'form': form
    }
    return render(request, 'dashboard/homework.html', context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')        

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')   


def youtube(request):
    return render(request, 'dashboard/youtube.html')