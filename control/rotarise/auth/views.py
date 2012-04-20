from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.template import RequestContext

INVALID_PASSWORD = "1"
NO_ERROR = "0"


#Template defnitions
REGISTRATION_TEMPLATE = 'auth/register.html'
LOGIN_TEMPLATE = 'auth/login.html'

#Defining forms. Django will take this definition and produce a form which can
#then be picked up by one of the django templates and customised.
class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    surname = forms.CharField()
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
#Fields left out of the form until we know what is wanted for a signup.
#Address Details
#house = forms.CharField()
#addrline1 = forms.CharField()
#addrline2 = forms.CharField()
#country = forms.CharField()
#postcode = forms.CharField()

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))


######## Helper Functions ######################################################

def generate_username(fname, sname):
    return "%s.%s" % (fname, sname)


######## Request Functions ####################################################

def register(request):
    c = {}
    c.update(csrf(request))
    context_inst = RequestContext(request)
    if request.method == 'POST':
        #Handle form submission
        form = RegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            surname = form.cleaned_data['surname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                #Check if someone has already used that email
                #address. The email is the username as well,
                #and so has to be unique.
                if User.objects.get(email__exact=email):
                    c['error'] = 'ALREADY_SIGNED_UP'
                    c['error_value'] = email
                    c['form'] = RegistrationForm()
                    return render_to_response(REGISTRATION_TEMPLATE, c, context_inst)
            except:
                pass
            print form.cleaned_data
            user = User.objects.create_user(email, email, password)
            user.first_name = firstname
            user.last_name = surname
            user.save()
            return render_to_response('thanks.html', c, context_inst)
    
    else:
        #First time visiting, return an empty form for filling in
        form = RegistrationForm()
    c['form'] = form
    return render_to_response(REGISTRATION_TEMPLATE, c)


def login(request, code=NO_ERROR):
    context_inst = RequestContext(request)
    redirect = request.GET.get('next', '')
    c = {}
    c.update(csrf(request))
    #Check for the invalid password error code
    if code == INVALID_PASSWORD:
        #Reload the login form pass the invalid_password variable to 
        #indicate to the user that the login has failed.
        form = LoginForm()
        c['form'] = form
        c['invalid_password'] = True
        return render_to_response(LOGIN_TEMPLATE, c, context_instance=context_inst)
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main/')
    
    #Handle submitting username & password
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['username']
            pass_text = form.cleaned_data['password']
            user = authenticate(username=user_text, password=pass_text)
            if not user:
                return HttpResponseRedirect('/login/%s/' % INVALID_PASSWORD)
            #Login the user
            login_user(request, user)
            
            #Get Redirect - the user may have navigated to a page that required
            #authentication, we want to log them in, and then pass them on their way.
            redirect = request.POST.get('next')
            
            if redirect != '':
                return HttpResponseRedirect(redirect)
            else:
                #Default location to send the user is to the main page.
                return HttpResponseRedirect('/main/')
    else:
        form = LoginForm()
    c['form'] = form
    c['next'] = redirect
    return render_to_response(LOGIN_TEMPLATE, c, context_instance=context_inst)

def reset_password(request):
    return password_reset(request, template_name='account_reset.html')

def logout(request):
    logout_user(request)
    return HttpResponseRedirect('/main/')

def main(request):
    #For the moment, make sure the user is authenticated,
    #and just send them to the static dashboard page.
    c = RequestContext(request, {'user': request.user})
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    return render_to_response('dashboard.html', c)



