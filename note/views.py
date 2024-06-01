from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import User
from blog.models import Post
from .models import Notes,AllSubject,Contact
from .forms import NoteForm,ContactForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# note shareing views here started
# |
        # Q(branch__icontains=q) |
        # Q(description__icontains=q)
def note(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.all()

    posts = Post.objects.all()[:5]
    # pagination 
    Notedata = Notes.objects.filter(status=True and
        Q(subject__name__icontains=q) 
    )
    Note_count = Notes.objects.filter(status=True).count()
    subjects = AllSubject.objects.all()[0:5]
    page = Paginator(Notedata, 5)
    page_number = request.GET.get('page', 1)
    NoteDataFinal = page.get_page(page_number)
    totalpage = NoteDataFinal.paginator.num_pages
    context = {'data':NoteDataFinal,'subjects':subjects, 'posts':posts, 'note_count':Note_count, 'users':users, 'lastpage':totalpage,'totalpagelist':[n+1 for n in range (totalpage)],'page':page_number}
    return render(request,'note/note.html',context)

def download_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    note.downloads += 1
    note.save()
    context = {"note":note}
    return render(request, "note/sucess.html", context)

def update_download_count(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        if note_id is not None:
            note = get_object_or_404(Notes, pk=note_id)
            note.downloads += 1
            note.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required(login_url='login')
def upload_notes(request):
    error=""
    form = NoteForm()
    subjects = AllSubject.objects.all()
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        subject_name = request.POST.get('subject')
        subject, created = AllSubject.objects.get_or_create(name = subject_name)
        if request.method=='POST':
            notes = form.save(commit=False)
            notes.user = request.user
            notes.branch = request.POST.get('branch')
            notes.subject = subject
            notes.notesfile = request.FILES.get('notesfile')
            notes.filetype = request.POST.get('filetype')
            notes.description = request.POST.get('description')
            notes.save()
            messages.info(request, 'Note createrd successfully')
            return redirect('my_notes')
        else:
            messages.error(request, 'Note not createrd')
    context = {'form':form, 'subjects':subjects}
    return render(request,'note/upload_note.html',context)

def my_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user=user)
    #print(notes)

    context = {'notes':notes}
    return render(request, 'note/my_notes.html',context)




def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect('my_notes')


def AllSubjectPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    subjects = AllSubject.objects.filter(name__icontains=q)
    return render(request, 'note/allsubjects.html', {'subjects': subjects})

def contact(request):
    error=""
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if request.method=='POST':
            contact = form.save(commit=False)
            contact.user = request.user
            contact.notesfile = request.FILES.get('notesfile')
            contact.description = request.POST.get('description')
            contact.save()
            messages.info(request, 'Note createrd successfully')
            return redirect('contact')
        else:
            messages.error(request, 'Note not createrd')
    context = {'form':form,}
    return render(request,'note/contact.html',context)