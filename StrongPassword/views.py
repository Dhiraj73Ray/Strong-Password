from django.shortcuts import render
from .forms import StrongPassword

def MakePassword(req):
    if req.method == 'POST':
        Pform = StrongPassword(req.POST)
        if Pform.is_valid():
            password = Pform.cleaned_data['password']
            print(f"Password: {password}")
    else:
        Pform = StrongPassword()
    return render(req, 'makepassword.html', {'form': Pform})