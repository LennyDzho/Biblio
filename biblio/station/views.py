from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Reader, Book
from django.shortcuts import get_object_or_404
from .forms import IssueBookForm, ReturnBookForm, ReaderForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
@login_required
def home(request):
    available_books = Book.objects.filter(status='available')
    return render(request, 'station/home.html', {'available_books': available_books})
@login_required
def Admin(request):
    return render(request, 'station/Admin.html')
@login_required
def Anather(request):
    return render(request, 'station/Anather.html')
@login_required
def my_books(request):
    try:
        reader = Reader.objects.get(user=request.user)
        borrowed_books = reader.borrowed_books.all()
        return render(request, 'station/my_books.html', {'borrowed_books': borrowed_books})
    except Reader.DoesNotExist:
        return HttpResponse('У вас нет связанной записи Reader. Создайте свою учетную запись Reader.')


# Ваш файл views.py

@login_required
def issue_book(request):
    if not request.user.is_staff:
        return redirect('Home')
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            reader = form.cleaned_data['reader']
            book = form.cleaned_data['book']
            reader.borrowed_books.add(book)
            book.status = 'checked_out'
            book.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = IssueBookForm()

    return render(request, 'station/issue_book.html', {'form': form})


# Ваш файл views.py


@login_required
def manage_readers(request):
    if not request.user.is_staff:
        return redirect('Home')

    readers = Reader.objects.all()  # Получите список всех читателей

    if request.method == 'POST':
        if 'add_reader' in request.POST:
            # Если отправлена форма для добавления читателя
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            birth_date = request.POST['birth_date']
            # Создайте читателя и связанный с ним пользователя Django
            user = User.objects.create_user(username=last_name + first_name, password='password')
            reader = Reader.objects.create(user=user, last_name=last_name, first_name=first_name, birth_date=birth_date)
        elif 'edit_reader' in request.POST:
            # Если отправлена форма для редактирования читателя
            reader_id = request.POST['reader_id']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            birth_date = request.POST['birth_date']
            # Обновите информацию о читателе
            reader = get_object_or_404(Reader, id=reader_id)
            reader.user.username = last_name + first_name
            reader.last_name = last_name
            reader.first_name = first_name
            reader.birth_date = birth_date
            reader.user.save()
            reader.save()
        elif 'delete_reader' in request.POST:
            # Если отправлена форма для удаления читателя
            reader_id = request.POST['reader_id']
            # Удалите читателя и связанный с ним пользователя Django
            reader = get_object_or_404(Reader, id=reader_id)
            user = reader.user
            reader.delete()
            user.delete()

        return redirect('manage_readers')  # Перенаправьте обратно на страницу управления читателями после операции

    if request.method == 'GET' and 'edit_reader' in request.GET:
        # Если пользователь нажал "Редактировать", покажем форму редактирования
        reader_id = request.GET['edit_reader']
        reader = get_object_or_404(Reader, id=reader_id)
        return render(request, 'station/edit_reader.html', {'reader': reader})

    return render(request, 'station/manage_readers.html', {'readers': readers})

@login_required
def edit_reader(request, reader_id):
    if not request.user.is_staff:
        return redirect('Home')

    reader = get_object_or_404(Reader, id=reader_id)

    if request.method == 'POST':
        # Если отправлена форма для редактирования читателя
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        birth_date = request.POST['birth_date']
        # Обновите информацию о читателе
        reader.user.username = last_name + first_name
        reader.last_name = last_name
        reader.first_name = first_name
        reader.birth_date = birth_date
        reader.user.save()
        reader.save()
        return redirect('manage_readers')  # Перенаправьте обратно на страницу управления читателями после операции

    return render(request, 'station/edit_reader.html', {'reader': reader})

@login_required
def return_book(request):
    if not request.user.is_staff:
        return redirect('Home')
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            reader = form.cleaned_data['reader']
            book = form.cleaned_data['book']
            print(f"Reader: {reader}")
            print(f"Book: {book}")
            reader.read_books.add(book)  # Добавляем в read_books
            reader.borrowed_books.remove(book)  # Удаляем из borrowed_books
            book.status = 'available'
            book.save()
            return redirect(request.META.get('HTTP_REFERER'))  # Перенаправьте на страницу со списком книг
    else:
        form = ReturnBookForm()

    return render(request, 'station/return_book.html', {'form': form})
@login_required
def read_books(request):
    if request.user.is_authenticated:
        try:
            reader = Reader.objects.get(user=request.user)
            returned_books = reader.read_books.all()
            return render(request, 'station/read_books.html', {'returned_books': returned_books})
        except Reader.DoesNotExist:
            return HttpResponse('У вас нет связанной записи Reader. Создайте свою учетную запись Reader.')
    else:
        return HttpResponse('Вы должны войти в систему, чтобы просматривать свои прочитанные книги.')

@login_required
def reader_list(request):
    if not request.user.is_staff:
        return redirect('Home')
    readers = Reader.objects.all()
    return render(request, 'station/reader_list.html', {'readers': readers})
@login_required
def add_reader(request):
    if not request.user.is_staff:
        return redirect('Home')
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reader_list')
    else:
        form = ReaderForm()
    return render(request, 'station/add_reader.html', {'form': form})
@login_required
def edit_reader(request, reader_id):
    if not request.user.is_staff:
        return redirect('Home')
    reader = Reader.objects.get(pk=reader_id)
    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            return redirect('reader_list')
    else:
        form = ReaderForm(instance=reader)
    return render(request, 'station/edit_reader.html', {'form': form, 'reader': reader})
@login_required
def delete_reader(request, reader_id):
    if not request.user.is_staff:
        return redirect('Home')
    reader = Reader.objects.get(pk=reader_id)
    if request.method == 'POST':
        reader.delete()
        return redirect('reader_list')
    return render(request, 'station/delete_reader.html', {'reader': reader})