from django.shortcuts import render
from .forms import EmailAuthenticationForm,UserRegisterForm,UserUpdateForm,UserUpadetEmailForm,SetPasswordForm1,PasswordResetForm1, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
#from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser,Profile
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
import json
from django.db.models import Q,Max
from .decorators import email_verified_required,user_authentication_required
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    
    form= EmailAuthenticationForm()
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print('login success')
            else:
                print('invalid details')
                return redirect('login')
    return render(request, 'index.html', {'form':form})
def activate(request, uidb64, token):
	User=get_user_model()

	try:
		uid=force_str(urlsafe_base64_decode(uidb64))
		user= User.objects.get(pk=uid)
	except:
		user= None
	if user is not None and account_activation_token.check_token(user, token):
		user.email_verified=True
		user.save()
		return redirect('/')
	else:
		messages.error(request, 'Activation link is invalid')

	return redirect('index')

def activateEmail(request, user, to_email):
	mail_subject = 'Activate your user account.'
	message= render_to_string("accounts/template_activate_account.html",
		{
			'user': user.username,
			'domain': get_current_site(request).domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
			'protocol': 'https' if request.is_secure() else 'http',

		}

		)
	email= EmailMessage(mail_subject, message, to=[to_email])
	if email.send():
		return redirect('email_confirmation')
		#messages.success(request, f'Please check your email to complete your resgistration. N.B check your spam folder')

	else:
		messages.error(request, f'Problem sending email to {to_email}, check if you type it correctly')

def EmailConfirmPage(request):
	
    user=get_user_model()
	
    if request.user.is_authenticated:
        user = request.user
        if user.email_verified:
            messages.success(request, ('You have already been verified...'))
            return redirect('/')

        else:
            form=UserUpadetEmailForm(instance=user )
            if request.method =='POST':
                form=UserUpadetEmailForm(request.POST or None, instance=user )
                if form.is_valid():
                    user_email=form.save(commit=False)
                    user_email.user=request.user
                    user_email.save()	
                              
                    activateEmail(request, user, form.cleaned_data.get('email'))
                    messages.success(request, 'please check your email to confirm your account')
                    return redirect(request.META.get("HTTP_REFERER"))


    else:
        return redirect('/')
		
    return render(request, 'accounts/email_comfirmation.html', {'form':form })

def logout_user(request):
	logout(request)
	messages.success(request, ('logged out successful...'))
	return redirect('/')
@user_authentication_required
@email_verified_required
def Profile_view(request, username):
    current_user = request.user
    user_profile=get_object_or_404(CustomUser, username=username)
    profile_num = get_object_or_404(Profile, profile=user_profile )
    
    form = UserUpdateForm(instance=user_profile)
    
    if request.method == "POST":
        num= request.POST.get('phone_number')
        profile_num.phone_number = num
        profile_num.save()
        form = UserUpdateForm(request.POST, instance=user_profile)
        if form.is_valid:
            user = form.save(commit=False)
            user.user_profile = current_user 
            user.save()
            return redirect(request.META.get("HTTP_REFERER"))
        

      


    context ={
        'user_profile':user_profile,
        'form':form,
    }

    return render(request, 'profile_view.html', context)

def send_profile_Id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('action')=='post':
            profile_id = int(data.get('profile_id'))
            print('the id is ',profile_id)
            profile = get_object_or_404(Profile, id=profile_id)
            print(profile)
            return JsonResponse({'sent_message':'yes'}, safe=False)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import urllib   
def save_cropped_image(request):
    if request.method == 'POST':
        user_id =int( request.POST.get('user_Id'))
        print(user_id)
        if 'croppedImage' in request.FILES:
            file_upload=request.FILES['croppedImage']
            
            print(file_upload)
            filename, ext = os.path.splitext(file_upload.name)
            sanitized_filename = filename.replace(' ', '_') + ext  # Replace spaces with underscores
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))

            saved_filename = fs.save(sanitized_filename, file_upload)
            file_url = f"/images/{saved_filename}"
            user_profile=get_object_or_404(CustomUser, id=user_id)
            user_profile.profile_picture=file_url
            user_profile.save()
            return JsonResponse({'file_url':file_url})
        else:

            return JsonResponse({'error': 'Invalid action'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
@email_verified_required
def password_change(request):
	user=get_user_model()
	user = request.user
	if request.method == 'POST':
		form = SetPasswordForm1(user, request.POST)
		if form.is_valid():
			form.save()
			logout(request)
			messages.success(request, "Your password has been changed, Please log in again....")
			return redirect('/')
			
        

	form = SetPasswordForm1(user)
	return render(request, 'accounts/password_reset_confirm.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm1(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("accounts/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                  
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly. Check your spam folder.
                        
                        """
                    )
                else:

                    messages.error(request, "Problem sending email, SERVER PROBLEM")
                    return redirect('/')
            else:
                messages.error(request, "Email does not exists in our database")
                return redirect('/')



    form = PasswordResetForm1()
    context={"form": form}

    return render(request, "accounts/password_reset.html", context )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm1(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in  now.")
                return redirect('/')
            

        form = SetPasswordForm1(user)
        return render(request, 'accounts/password_reset_confirm2.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")
