from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.files import File
from django.contrib.auth import hashers as hash
from django.http import HttpResponse
from django.http import Http404
from cryptography.exceptions import InvalidSignature

from .forms import CustomUserCreationForm
from .forms import MessageForm
from .forms import PermissionForm
from .models import CustomUser
from .models import Key
from .models import Message
from .models import Permission
import x509ceryficat as certyficat
import signature


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def user_registration_view(request):
    my_form = CustomUserCreationForm()

    if request.method == "POST":
        my_form = CustomUserCreationForm(request.POST)
        if my_form.is_valid():
            username, email, password = from_user(**my_form.cleaned_data)
            key = certyficat.return_key_core()
            obj = CustomUser.objects.create(username=username,
                                            email=email, password=hash.make_password(password=password))
            obj.private_key = certyficat.return_private_key(key)
            obj.save()
            Key.objects.create(user=obj, public_key=certyficat.return_public_key(key))
            return redirect('/users/login')
    context = {
        "form": my_form
    }
    return render(request, "signup.html", context)


def user_message_view(request):
    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            if request.user.is_authenticated:
                message = message_form.save(commit=False)
                message.user_from = request.user
                message.save()

                f = open(message.contain.path, 'rb')
                file_to_sign = File(f)
                private_key = request.user.private_key.tobytes()
                obj = Message.objects.get(id=message.pk)
                sign_file = signature.create_sign(private_key, file_to_sign)
                obj.sign_data = sign_file
                obj.save()

    context = {
        "message_form": message_form
    }
    return render(request, 'message.html', context)


def user_incoming_message_view(request):
    queryset = Message.objects.all().filter(user_to=request.user)
    context = {
        "object_list": queryset

    }
    return render(request, 'incoming.html', context)


def user_dynamic_incoming_message_view(request, id):
    obj = Message.objects.get(id=id)
    context = {
        "object": obj
    }
    return render(request, 'message_detail.html', context)


def user_incoming_message_verify(request, id):
    obj = Message.objects.get(id=id)
    user_from = obj.user_from
    user_key_id = Key.objects.get(user=user_from)
    if Permission.objects.filter(user=request.user, user_key=user_key_id).first():
        key_object = Key.objects.get(user=obj.user_from)
        public_key = key_object.public_key.tobytes()
        sign = obj.sign_data.tobytes()
        try:
            signature.verify_sign(sign, public_key)
            information = "Sign is correct!"
        except InvalidSignature:
            information = "Negative result!"
    else:
        information = 'You do not have permission to know public key of this user '

    context = {
        "object": obj,
        "info": information
    }
    return render(request, 'message_detail.html', context)


def user_incoming_message_file_view(request, id):

    obj = Message.objects.get(id=id)
    if request.user == obj.user_to:

        f = open(obj.contain.path, 'rb')
        file_to_read = File(f)
        return HttpResponse(file_to_read, content_type='xml')
    else:
        raise Http404


def user_settings(request):
    settings_form = PermissionForm()

    if request.method == "POST":
        settings_form = PermissionForm(request.POST)
        if settings_form.is_valid():
            if request.user.is_authenticated:
                checking_user = settings_form.cleaned_data['user']
                checking_key = Key.objects.get(user=request.user)
                if Permission.objects.filter(user=checking_user, user_key=checking_key).first():
                    return HttpResponse("<h3>This user have acces to your public key</h3>")
                else:
                    obj_key = Key.objects.get(user=request.user)
                    settings_tmp = settings_form.save(commit=False)
                    settings_tmp.user_key = obj_key
                    settings_tmp.save()
    context = {
        'settings_form': settings_form
    }
    return render(request, 'settings.html', context)


def from_user(username, email, password1, password2):
    return username, email, password1


