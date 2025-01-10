from users.models import EmailUser
from django.contrib.auth.forms import UserCreationForm

class EmailSignupForm(UserCreationForm):
    class Meta:
        model=EmailUser
        fields =('email' , 'password1' , 'password2')