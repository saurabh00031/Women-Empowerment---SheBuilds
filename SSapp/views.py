from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from .decorators import user_required,mentor_required
from .models import *
from .forms import BlogForm, UsrReg,MentorReg,MentorinfoForm
from django.core.mail import send_mail
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog_Post
from SSapp.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from SSapp.models import SchollershipList

from django.conf import settings
from django.core.mail import send_mail
import uuid

from SSapp.models import WommenRights




def frontend_home(request):
    return render(request,'frontend_home.html')


def dashboard(request):
    return render(request,'dashboard.html')

@user_required
def contact_us(request):
    return render(request,'frontend_contact.html')

@user_required
def index(request):
    posts = Blog_Post.objects.all()
    return render(request, 'frontend_index.html', {'posts': posts})



class UsrView(CreateView):
    model = User
    form_class = UsrReg
    template_name = 'frontend_sg_user.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'User has been created successfully!')
        login(self.request, user)
        return redirect("sgin_user")


class MentorView(CreateView):
    model = User
    form_class = MentorReg
    template_name = 'frontend_sg_mentor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mentor'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Mentor has been created successfully!')
        login(self.request, user)
        return redirect("sgin_mentor")



def sgin_user(request):
    if request.method == "POST":
        # check if user has entered correct credientials
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_user == True:
                login(request, user)
                return redirect("sginpg_user")
            else:
                messages.error(
                    request, 'You are not authorized to access this page!')
        else:
            messages.error(request, 'Invalid Credentials!,plz try again')
            return render(request, 'frontend_sgin_user.html')
    return render(request, 'frontend_sgin_user.html')



def sgin_mentor(request):
    if request.method == "POST":
        # check if user has entered correct credientials
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_mentor == True:
                login(request, user)
                return redirect("sginpg_mentor")
            else:
                messages.error(
                    request, 'You are not authorized to access this page!')
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Invalid Credentials!,plz try again')
            return render(request, 'frontend_sgin_mentor.html')
    return render(request, 'frontend_sgin_mentor.html')




def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been log out !')
        return redirect('frontend_home')
    else:
       messages.success(request, 'You are not logged in !')
       return redirect('frontend_home')





@user_required
def addPost(request):
    if request.method=='POST':
        title=request.POST.get('title')
        slug=request.POST.get('slug')
        body=request.POST.get('body')
        image=request.FILES['image']
        blog=Blog_Post(title=title,slug=slug,body=body,writer=request.user,image=image)
        blog.save()
        messages.success(request,"post has been updates successfully")
        return redirect('addPost')
    return render(request,'frontend_addPost.html')

        
@user_required
def my_posts(request):
     if request.user.is_authenticated:
        blog_data = Blog_Post.objects.filter(writer=request.user.id)
        return render(request , 'frontend_blog_data.html' , {'blog_data' : blog_data})



@user_required
def blog_detailView(request, slug):
    post = Blog_Post.objects.get(slug = slug)
    comments = post.comments.all()
    new_comment = None
    
    if request.method == 'POST':
        form = CommentForm(request.POST,initial={'commenter': request.user})
        if form.is_valid():
            x= form.cleaned_data['body']
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.body=x
            new_comment.commenter=request.user
            new_comment.save()
            print("done......")
            messages.success(request, 'User commented successfully!')
            return HttpResponseRedirect(reverse('blog_detail', args = [str(post.slug)]))
            
    else:
        form = CommentForm()
    return render(request, 'frontend_blog_detail.html', {'post': post, 'form': form, 'comments':comments, 'new_comment':new_comment})


@mentor_required 
def sginpg_mentor(request):
    this_usr = request.user
    usr_inf = Mentorinfo.objects.get(user = request.user)
    if request.method == "POST":
        full_Name = request.POST.get('full_Name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        git_hub = request.POST.get('git_hub')
        insta_link = request.POST.get('insta_link')
        linked_in= request.POST.get('linked_in')
        city = request.POST.get('city')
        address = request.POST.get('address')
        states = request.POST.get('states')
        country = request.POST.get('country')
        field_of_interest = request.POST.get('field_of_interest')
        total_earnings_by = request.POST.get('total_earnings_by')
        company_name = request.POST.get('company_name')
        future_goals = request.POST.get('city')
        experience_yrs = request.POST.get('experience_yrs')
        description_in_short=request.POST.get('description_in_short')



        

        usr_inf.full_Name = full_Name
        usr_inf.country=country
        usr_inf.states=states
        usr_inf.address=address
        usr_inf.phone = phone
        usr_inf.git_hub =git_hub
        usr_inf.insta_link = insta_link
        usr_inf.linked_in= linked_in
        usr_inf.city = city
        usr_inf.email=email
        usr_inf.field_of_interest = field_of_interest
        usr_inf.total_earnings_by = total_earnings_by
        usr_inf.company_name = company_name
        usr_inf.future_goals = future_goals
        usr_inf.experience_yrs = experience_yrs
        usr_inf.description_in_short=description_in_short
        usr_inf.save()
        
        this_usr.email = email
        this_usr.save()
        messages.success(request, 'Data Updated Successfully!') 
        
    usr_dat = {
        "usr_info" : usr_inf,
        "my_usr_inf" : this_usr
    }
    return render(request, 'frontend_sginpg_mentor.html', usr_dat)



@user_required
def sginpg_user(request):
    obj=Mentorinfo.objects.all()
    Mentor_data={
        "obj_ment":obj,
    }
    return render(request,'frontend_sginpg_user.html',Mentor_data)



@user_required
def search(request):
    qur = request.GET.get('search')
    ct = Mentorinfo.objects.filter(city__contains=qur)
    return render(request, 'frontend_search1.html', {'ct': ct})



def getAllSchollerships(request):
    data=SchollershipList.objects.all()
    context ={
        'data':data
    }
    return render(request,'schollershipList.html',context)




@user_required
def send_request(request,id):
    obj=Mentorinfo.objects.all()
    Mentor_data={
        "obj_ment":obj,
    }
    y=request.user
    print(y)
    z=uuid.uuid1()
    print(id)
    subject = 'Welcome to SheBuilds !!'
    message = f'Entrepreneur {y} requests you for chat in room number  :  ( {str(z)} )'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [id]
    send_mail( subject, message, email_from, recipient_list )
    messages.success(request, 'Email Sent!')
    return render(request,'frontend_sginpg_user.html',Mentor_data)


@user_required
def send_request_user(request,username):
    xy=str(username)
    try:
        yz=Usrinfo.objects.get(full_Name=username)
        print(yz.email)
        y=request.user
        print(y)
        print(yz.email)
        print("................................")
        z=uuid.uuid1()
        print(id)
        subject = 'Welcome to SheBuilds.... !!'
        message = f'Mentor {y} requests you for chat in room number  :  ( {str(z)} )'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [yz.email]
        send_mail( subject, message, email_from, recipient_list )
    except Usrinfo.DoesNotExist:
        print("exception........")
        yz=None
    messages.success(request, 'Email Sent to User!')
    return redirect('index')



@user_required
def contact_us(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        usr_eml = request.POST.get('email')
        phone = request.POST.get('phnum')
        message = request.POST['message']
        send_mail(fname,
                    "User Phone:-  "+phone+"\n"+"User Email:- "+usr_eml+"\n"+message,
                    usr_eml,
                    ['patilsaurabh7777777@gmail.com'],
                    fail_silently=True)
        messages.success(request, 'Thank you for the message! We\'ll respond to you shortly!!')      
    return render(request, 'frontend_contact.html')


def getAllRights(request):
    data=WommenRights.objects.all()
    context = {
        'data':data
    }
    return render(request,'wommen_rights.html',context)
        

