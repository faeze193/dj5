from django.shortcuts import render, redirect
from .form import UserLoginForm, UserRegisterPhoneForm, UserRegisterCodeForm, UserRegisterInfoForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import otm
import random
from .models import User, Otp, Address
# Create your views here.



class UserLoginView(View):
    
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request, 'accounts/login.html', {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request, 'شما با موفقیت وارد شدید.', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.', 'danger')
        return render(request, 'accounts/login.html', {'form':form})

class UserLogoutView(LoginRequiredMixin, View):

    def get(self,request):
        logout(request)
        return redirect('home:home')
    

class UserRegisterPhoneView(View):

    form_class = UserRegisterPhoneForm
    template_name = 'accounts/register_phone.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.subject.filter(phone=cd['phone']).exists()
            if user :
                messages.error(request, 'این شماره از قبل وجود داشته است.')
                return render(request, self.template_name, {'form':form})
                
            else:
                code = random.randint(1000,9999)
                Otp.objects.create(phone=cd['phone'], code=code)
                otm(cd['phone'],code)
                request.session['user_phone_info'] = cd['phone']
                return redirect('accounts:user_register_code')
        return render(request, 'home/index.html', {'form':form})
    

class UserRegisterCodeView(View):

    form_class = UserRegisterCodeForm
    template_name = 'accounts/register_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        phone_session = request.session['user_phone_info']
        otp = Otp.objects.get(phone=phone_session)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == otp.code:
                return redirect('accounts:user_register_info')
            else:
                messages.error(request, 'کد وارد شده اشتباه است', 'danger')
                return redirect('accounts:user_register_code')
        return render(request, self.template_name, {'form':form})
    

class UserRegisterInfoView(View):

    form_class = UserRegisterInfoForm
    template_name  = 'accounts/user_register_info.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = request.session['user_phone_info']
            user = User.subject.create_user(phone=phone, first_name=cd['first_name'],
                                       last_name=cd['last_name'],email=cd['email'],password=cd['password2'])
            messages.success(request, 'حساب کاربری شما با موفقیت ثبت شد، اکنون وارد شوید.', 'success')
            return redirect('accounts:user_login')
        return render(request, self.template_name, {'form':form})

                

class AddressesView(LoginRequiredMixin,View):
    
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'accounts/addresses.html', {'addresses':addresses})



            
            
            
