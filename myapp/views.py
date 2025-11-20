from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from .forms import BookForm


def book_list(request):
    books = Book.objects.all()
    context = {
        'books': books,
        'total_books': books.count(),
        'available_books': sum(1 for book in books if book.quantity > 0),
    }
    return render(request, 'myapp/book_list.html', context)


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{form.cleaned_data['title']}' created successfully!")
            return redirect('myapp:book_list')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Add New Book',
        'button_text': 'Create Book'
    }
    return render(request, 'myapp/book_form.html', context)


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{form.cleaned_data['title']}' updated successfully!")
            return redirect('myapp:book_list')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'title': f'Edit: {book.title}',
        'button_text': 'Update Book'
    }
    return render(request, 'myapp/book_form.html', context)


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"Book '{book_title}' deleted successfully!")
        return redirect('myapp:book_list')
    
    context = {
        'book': book,
    }
    return render(request, 'myapp/book_confirm_delete.html', context)
