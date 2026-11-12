from django.shortcuts import render, redirect, get_object_or_404
from .models import Chats
from accounts.forms import EmailAuthenticationForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import Chatform
from django.db.models import Q, Max
from accounts.models import CustomUser
import json
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from .models import ChatPreview
from accounts.views import activateEmail
from django.contrib import messages
from accounts.decorators import email_verified_required, user_authentication_required
from django.contrib.auth.decorators import login_required


def index(request):
    chats = Chats.objects.all()
    user = get_user_model()
    form = EmailAuthenticationForm()
    form_register = UserRegisterForm()
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "login":
            form = EmailAuthenticationForm(request, request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.email_verified:
                        login(request, user)
                        print("login success")
                        # messages.success(request, ("Logged in successful..."))
                        return redirect("index")
                    else:

                        login(request, user)
                        print(
                            "Account is not active. Check your email for activation instructions"
                        )
                        messages.error(
                            request,
                            "Account is not active. Check your email for activation instructions.",
                        )
                        return redirect("email_confirmation")
                        # login(request, user)
                        # print('login success')
                        # return redirect('/')
                else:
                    print("invalid details")
                    return redirect("/")
        elif form_type == "register":

            form_register = UserRegisterForm(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.email_verified = False
                user.save()
                email = form_register.cleaned_data["email"]
                password = form_register.cleaned_data["password1"]
                user = authenticate(request, username=email, password=password)
                login(request, user)
                activateEmail(request, user, form_register.cleaned_data.get("email"))
                return redirect("email_confirmation")
    context = {"chats": chats, "form": form, "form_register": form_register}
    return render(request, "index.html", context)


@user_authentication_required
@email_verified_required
def chat_preview(request):
    user = request.user

    # Get the latest message between the logged-in user and any other user
    # latest_chats = Chats.objects.filter(
    #     Q(sender=user) | Q(recipient=user)
    # ).annotate(
    #     last_message_time=Max('timestamp')
    # ).order_by('-last_message_time')

    # # Filter out only one message per conversation (latest one)
    # seen_conversations = set()
    # previews = []

    # for chat in latest_chats:
    #     if chat.sender == user:
    #         conversation_with = chat.recipient
    #     else:
    #         conversation_with = chat.sender

    #     if conversation_with.id not in seen_conversations:
    #         previews.append(chat)
    #         seen_conversations.add(conversation_with.id)

    context = {
        # 'previews': previews,
        "user": user
    }

    return render(request, "messages.html", context)


def chatm_view(request, recipient_id=None):
    user = request.user
    recipient = (
        get_object_or_404(get_user_model(), id=recipient_id) if recipient_id else None
    )

    if recipient:
        # Filter messages between the logged-in user and the recipient
        messages = Chats.objects.filter(
            (Q(sender=user) & Q(recipient=recipient))
            | (Q(sender=recipient) & Q(recipient=user))
        ).order_by("timestamp")
    else:
        messages = []

    context = {
        "messages": messages,
        "recipient": recipient,
    }
    return render(request, "chat.html", context)


def save_messagePreviewto_db(request):
    if request.method == "POST":
        user = request.user

        data = json.loads(request.body)

        if data.get("action") == "post":
            save_message = data.get("messages_preview")

            if save_message is not None:
                if user.Messsage_preview:
                    existing_previews = json.loads(user.Messsage_preview)

                else:
                    existing_previews = []
                if isinstance(save_message, list):
                    existing_previews.extend(save_message)
                else:
                    existing_previews.append(save_message)

                unique_dic = {}
                for msg in existing_previews:
                    key = f"{min(int(msg['sender_number']), int(msg['recipient_number']))}_{max(int(msg['sender_number']), int(msg['recipient_number']))}"

                    unique_dic[key] = msg
                    # unique_previews = list(unique_dic.values())[::-1]
                    unique_previews = list(unique_dic.values())
                    user.Messsage_preview = json.dumps(unique_previews)
                    user.save()

                return JsonResponse({"priview_messages": user.Messsage_preview})

            else:
                # Return null in JSON format if no message preview is available
                return JsonResponse({"priview_messages": None}, safe=False)
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import urllib


def upload_files(request):
    if request.method == "POST":

        if "files" in request.FILES:
            file_upload = request.FILES["files"]
            filename, ext = os.path.splitext(file_upload.name)
            sanitized_filename = (
                filename.replace(" ", "_") + ext
            )  # Replace spaces with underscores
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "images"))

            saved_filename = fs.save(sanitized_filename, file_upload)
            file_url = f"/images/{saved_filename}"
            return JsonResponse({"file_url": file_url})
        else:

            return JsonResponse({"error": "Invalid action"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_private_message(request):
    if request.method == "POST":
        first_user = request.user
        data = json.loads(request.body)
        if data.get("action") == "post":
            second_user_id = data.get("receipient_id")
            external_user = data.get("external_user")
            if external_user:
                # other_user = get_object_or_404(get_user_model(), id=second_user_id)
                print("the phone number is", external_user)
                messages = Chats.objects.filter(
                    (Q(sender=first_user) & Q(external_user=external_user))
                    | (Q(external_user=external_user) & Q(recipient=first_user))
                ).order_by("timestamp")
                response_json = serializers.serialize("json", messages)
                return JsonResponse(
                    {
                        "private_messages": response_json,
                        "second_user_username": external_user,
                        "second_user": external_user,
                        "user_id": first_user.id,
                    },
                    safe=False,
                )
            else:

                other_user = get_object_or_404(get_user_model(), id=second_user_id)
                messages = Chats.objects.filter(
                    (Q(sender=first_user) & Q(recipient=other_user))
                    | (Q(sender=other_user) & Q(recipient=first_user))
                ).order_by("timestamp")

                response_json = serializers.serialize("json", messages)
                if other_user.profile_picture:
                    profile_picture_url = other_user.profile_picture.url
                else:
                    profile_picture_url = None
                response_data = json.loads(response_json)
                for message in response_data:
                    if message["fields"]["image"]:
                        # Correct the image URL
                        message["fields"]["image"] = (
                            settings.MEDIA_URL + message["fields"]["image"]
                        )

                # Re-serialize after modifying the image URL
                modified_response_json = json.dumps(response_data)
                return JsonResponse(
                    {
                        "private_messages": modified_response_json,
                        "second_user_username": other_user.username,
                        "second_user": other_user.first_name,
                        "second_user_img": profile_picture_url,
                        "user_id": first_user.id,
                    },
                    safe=False,
                )
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


# def get_recipient(request):
#     User = CustomUser
#     if request.method == 'POST':

#         data = json.loads(request.body)
#         if data.get('action')=='post':
#             sendto_email = data.get('recipient_email')
#             print(sendto_email)
#             try:
#                     # Attempt to get the user by email
#                 user = CustomUser.objects.get(email=sendto_email)
#                 print('The user details are:', user, user.id)
#                 return JsonResponse({'sent_message': 'User found', 'user_id': user.id}, safe=False)

#             except CustomUser.DoesNotExist:
#                     # Handle the case where no user was found with the provided email
#                 return JsonResponse({'error': 'User does not exist'}, status=404)
#         else:
#                 return JsonResponse({'error': 'Invalid action'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)


def send_message(request):
    if request.method == "POST":
        first_user = request.user
        data = json.loads(request.body)
        if data.get("action") == "post":
            second_user_id = data.get("otheruser_id")
            second_user = get_object_or_404(get_user_model(), id=second_user_id)
            message = data.get("message")
            sending_message = Chats.objects.create(
                sender=first_user, recipient=second_user, content=message
            )
            response_json = serializers.serialize("json", [sending_message])
            return JsonResponse(
                {"sent_message": response_json, "user_id": first_user.id}, safe=False
            )
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


from accounts.models import Profile
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse


def get_recipient_details(request):
    sender_user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if data.get("action") == "post":

                sendto_email_or_number = data.get("recipient_email")
                try:
                    # handle email by an internal user
                    user = CustomUser.objects.get(email=sendto_email_or_number)

                    return JsonResponse(
                        {
                            "sent_message": "User found",
                            "recipient_phone_number": str(user.profile.phone_number),
                            "external_user": False,
                            "userId": user.id,
                        },
                        safe=False,
                    )

                except CustomUser.DoesNotExist:
                    try:
                        # handle phone_number by an internal user
                        get_profile = Profile.objects.get(
                            phone_number=sendto_email_or_number
                        )
                        print(get_profile.phone_number)
                        return JsonResponse(
                            {
                                "sent_message": "Profile found",
                                "external_user": False,
                                "phone_number": str(sender_user.profile.phone_number),
                                "recipient_phone_number": str(get_profile.phone_number),
                                "userId": get_profile.profile.id,
                            },
                            safe=False,
                        )
                    except Profile.DoesNotExist:
                        # handle external user
                        return JsonResponse(
                            {
                                "external_user": True,
                                "recipient_phone_number": str(sendto_email_or_number),
                                "sender_twilio_number": settings.TWILIO_PHONE_NUMBER,
                            },
                            status=200,
                        )
                    # return JsonResponse({'error': 'User does not exist in database'}, status=404)

            else:
                return JsonResponse({"error": "Invalid action"}, status=400)

        except json.JSONDecodeError:
            # Handle invalid JSON format
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


##twilio views


def send_sms_to_external_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message_body = data.get("message_content")
        to_number = data.get("recipient_number")

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message_body, from_=settings.TWILIO_PHONE_NUMBER, to=to_number
        )
        return JsonResponse({"status": "Message sent successfully", "sid": message.sid})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def receive_sms(request):
    if request.method == "POST":
        # Capture incoming SMS details (such as from Twilio)
        from_number = request.POST.get("From")
        body = request.POST.get("Body")
        print(from_number, body)

        # Process the incoming SMS and potentially save it to your Chats model
        # You might also want to forward this to your WebSocket consumer to display in-app
        # ...

        return JsonResponse({"status": "Message received successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)
