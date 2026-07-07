

# Create your views here.
from django.shortcuts import redirect, render
from .models import Contact , Book
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

def home(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'home.html', {
        'books': books
    })

def about(response):
    return render(response, 'about.html')

def contact(response):
    if response.method == 'POST':
        name = response.POST.get('name')
        email = response.POST.get('email')
        subject = response.POST.get('subject')
        message = response.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(response, 'Your message has been sent successfully!')
        return redirect('contact')  # Redirect to the contact page after submission

    return render(response, 'contact.html')



def register(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Welcome {user.username}! Your account has been created successfully."
)
            login(request, user)
            return redirect('home')
           
        
        else:
            print("FORM ERRORS:")
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})
def loginUser(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)

    return render(request, 'book_detail.html', {
        'book': book
    })