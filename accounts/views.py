from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib.auth.tokens import default_token_generator
from accounts.utils import detectUser, send_verification_email
from django.utils.http import urlsafe_base64_decode
from vendor.forms import VendorForm
from vendor.models import Vendor

# restrict the restaurant from accessing the customer page
def check_role_restaurant(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied # when permission denied occur, django will automatically reach to 403.html

# restrict the customer from accessing the restaurant page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    # prevent logged in user go to login/register page
    if request.user.is_authenticated: 
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if (form.is_valid()):
            ''' create user using form '''
            # password = form.cleaned_data['password']
            # user = form.save(commit=False) # no need to save in DB
            # user.set_password(password) # save password in hash format
            # user.role = User.CUSTOMER
            # user.save()

            ''' create user using create_user method '''
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.CUSTOMER
            user.save()
            
            # send verification email
            mail_subject = 'Verify your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    # prevent logged in user go to login/register page
    if request.user.is_authenticated: 
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # stored data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if (form.is_valid() and v_form.is_valid()):
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False) # don't save immediately, due to assign user data
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            # send verification email
            mail_subject = 'Please verify your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()   
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    # activate user by setting the is_active status = True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    
    if ((user is not None) and (default_token_generator.check_token(user, token))):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated.')
        return redirect('myAccount')
    else:
        print(user)
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

def login(request):
    # prevent logged in user go to login/register page
    if request.user.is_authenticated: 
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if(user):
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid account')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

# check user role and redirect to customer or restaurant dashboard
@login_required(login_url='login')
def myAccount(request):
    user = request.user # person who logged in only
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def restaurantDashboard(request):
    return render(request, 'accounts/restaurantDashboard.html')
 
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email) # can you email=email (email__exact is more specific)
            
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template) # send reset password email
            
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist') # entered email is not exist in DB
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Password not match, please try again.')
            return redirect('reset_password')
        
    return render(request, 'accounts/reset_password.html')

# validate user by decoding token (user's pk)
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if ((user is not None) and (default_token_generator.check_token(user, token))):
        request.session['uid'] = uid # store uid in the session
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')