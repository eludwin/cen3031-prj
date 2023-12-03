from .forms import LoginForm, RegisterForm
from django.views.generic.edit import FormView
from django.contrib import messages
from interviewbuddy.config import Config
from pymongo import MongoClient
from django.shortcuts import render
from .database import Database
from .config import Config
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
client = MongoClient(Config.DB_CONNECTION)
dbname = client['test_database']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = Database()

def home_view(request):
    return render(request, 'home.html')

def chat_view(request):
    # insert chat logic
    return render(request, 'chat.html')

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/home'  # Redirect to this URL on successful form submission

    def login_user(self, username, password):
        # Your custom login logic here
        # This could involve checking credentials, setting session variables, etc.
        pass

    def form_valid(self, form):
        # Call your custom function

        # You can also access form data using form.cleaned_data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Add your authentication logic here (e.g., check credentials)
        print(username,password)
        response = db.login_user(username, password)
        print(response)
        if "successful" in response:
            return redirect('chat')
        else:
            messages.error(self.request, response)

        return super().form_invalid(form)

    def form_invalid(self, form):
        # Your form validation failed, handle it here
        # You might want to add a message to inform the user about the error
        messages.error(self.request, 'Invalid login credentials. Please try again.')

        # Redirect to the login page or any other appropriate URL
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm  # Create a RegisterForm similar to the LoginForm
    success_url = '/accounts/login'  # Redirect to this URL on successful form submission

    def form_valid(self, form):
        # Get the registration form data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        # Add your registration logic using the Database class here
        result_message = db.register_user(username, password)

        # Add a success or error message based on the result
        if "successful" in result_message:
            messages.success(self.request, result_message)
            return super().form_valid(form)
        else:
            messages.error(self.request, result_message)

        # If registration is unsuccessful, do not redirect to the success URL
        return super().form_invalid(form)

    def form_invalid(self, form):
        # Your form validation failed, handle it here
        # You might want to add a message to inform the user about the error

        # Redirect to the login page or any other appropriate URL
        return super().form_invalid(form)