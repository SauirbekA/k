from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from Register.decorators import *
from selenium import webdriver
from django.core.mail import send_mail, BadHeaderError
import smtplib
from email.mime.text import MIMEText



def mainpage(request):
    
    menu = Course.objects.all()
    context = {
        'title': 'Main Page',
        'menu': menu,
    }
    return render(request,'main/mainpage.html', context=context)

# @allowed_users(allowed_roles=['moderator'])
def catalogue(request): #, cat_id = 0
    
    menu = Course.objects.filter(is_published=True)
    cats = Category.objects.all()
    
    context = {
        'title': 'Catalogue',
        'menu': menu,
        'cats': cats,
        'cat_selected': 0,
    }
    return render(request, 'main/catalogue.html', context=context)

def category(request, cat_id):
    courses = Course.objects.filter(cat_id=cat_id, is_published=True)
    cats = Category.objects.all()

    context = {
        'courses': courses,
        'cats': cats,
        'cat_selected': cat_id,

    }
    return render(request, 'main/category.html', context)




@login_required
@allowed_users(allowed_roles=['teacher'])
def create(request):
    id = request.user.pk
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, initial={'idUser': id}) #2
        if form.is_valid():
            try:
                form.save()
                return redirect('mainpage')
            except:
                form.add_error(None, "Error at adding Course")
    else:
        form = AddPostForm(initial={'idUser': id})
    context = {
        'title': 'Create Course',
        'form': form,
    }
    return render(request, 'main/create.html', context=context)

@login_required
@allowed_users(allowed_roles=['teacher'])
def create_lesson(request, id):
    if request.method == 'POST':
        form = AddLessonForm(request.POST, request.FILES, initial={'idCourse': id})
        if form.is_valid():
            try:
                form.save()
                return redirect( f'/coursepage/{id}' )
            except:
                form.add_error(None, "Error at adding Lesson")
    else:
        form = AddLessonForm(initial={'idCourse': id})
    context = {
        'title': 'Create lesson',
        'form': form,
        'id': id,
    }
    return render(request, 'main/create_lesson.html', context=context)
    

@login_required
def coursepage(request, id):
    user = request.user.pk
    videos = Video.objects.filter(idCourse=id)
    menu = Course.objects.filter(id=id)
    lesson = LessonContainer.objects.filter(idUser=user, idCourse=id)
    context = {
        'title': "Coursepage",
        'menu': menu,
        'videos': videos,
        'id': id,
        'lesson': lesson,
    }
    return render(request, 'main/coursepage.html', context=context)

@login_required
def lesson(request, id):
    user = request.user.pk

    videos = Video.objects.filter(idCourse=id)
    menu = Course.objects.filter(id=id)
    lesson = LessonContainer.objects.filter(idUser=user, idCourse=id)
    context = {
        'title': "Coursepage",
        'menu': menu,
        'videos': videos,
        'id': id,
        'lesson': lesson,
    }
    return render(request, 'main/lessonpage.html', context=context)








@login_required
def profile(request):
    user = request.user.pk
    course = Course.objects.filter(idUser=user)
    container = LessonContainer.objects.filter(idUser=user)
    UserChoice = Course.objects.all()
    group = request.user.groups.all()[0].name
    context = {
        'title': "Profile page",
        'course': course,
        'container': container,
        'UserChoice': UserChoice,
        'group': group,
    }
    return render(request, 'main/profile.html', context=context)

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Course.objects.all().filter(title__contains=search, is_published=True)
        return render(request, 'main/searchbar.html', {'post': post})



def accountSettings(request):
    post = Learner.objects.all().filter(user_id=request.user.pk)
    if post:
        print(post)
        user = request.user.learner
    else:
        Learner.objects.create(user_id=request.user.pk, name=request.user.username)
        user = request.user.learner

    form = UpdateUserForm(instance=user)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
            
    context = {
        'title': "Edit Profile page",
        'form': form,

    }
    return render(request, 'main/accountSettings.html', context=context)



from django.http import HttpResponseRedirect

def add_course_to_user(request, id):
    
    course = Course.objects.filter(pk = id)
    cost = False
    for c in course:
        # print("Title: ", c.price)
        if c.price > 0:
            cost = True
    # print('Cost: ', cost) 
    # print('email: ', request.user.email)       
    if cost == True:
        print('I am here')
        context = {'cost': c.price, 'id': id}
        return render(request, 'main/payment.html', context) 
    else:
           
        user = request.user.pk
        lesson = LessonContainer.objects.create(idUser=user, idCourse=id)
        return redirect('profile')    
        
def pay(request, id):   
    user = request.user.pk
    lesson = LessonContainer.objects.create(idUser=user, idCourse=id)
    name = Course.objects.filter(pk = id)
    
    try:
        send_mail('FES team', f'You successfully purchased the course: {name[0].title} for {name[0].price}$', 'a.nurmuhan03@gmail.com', ['artikbaisauirbek@gmail.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')    
    return redirect('profile')
    

def delete_course_from_user(request, id):
    user = request.user.pk
    lesson = LessonContainer.objects.filter(idUser=user, idCourse=id).delete()
    return redirect('profile')
    
def delete_course(request, id):
    user = request.user.pk
    course = Course.objects.filter(pk=id).delete()
    return redirect('profile')

@allowed_users(allowed_roles=['moderator'])
def accept_course(request, id):
    
    course = get_object_or_404(Course, pk=id)
    if course.is_published == True:
        course.is_published = False
    else:
        course.is_published = True      
    course.save()
    return redirect('moderator')



# def send_form_to_telegram_bot(form_data):
#     # Create a bot object using the API token
#     bot = Bot(token='YOUR_API_TOKEN')
#     # Send the form data to the Telegram chat
#     bot.send_message(chat_id='YOUR_CHAT_ID', text=form_data)

@allowed_users(allowed_roles=['moderator'])
def moderator(request):
    group = request.user.groups.all()[0].name
    course = Course.objects.filter(is_published=False)

    context = {
        'title': 'Moderator page',
        'group': group,
        'course': course,
    }

    return render(request, 'main/moderator.html', context)


from django.http import JsonResponse
import requests

@login_required
def send_message(request):
    u_name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message', '')
   
    message = "Name: " + u_name + "\nEmail: " + email + "\nPhone: " + phone + "\nMessage: " + message
    telegram_bot_id = "5970994672:AAHR5Mux2ikEkRm5VmHK-s--LBSsCK_1x6k"
    chat_id = -1001821458102
    data = {
        "chat_id": chat_id,
        "text": message
    }

    
    url = "https://api.telegram.org/bot" + telegram_bot_id + "/sendMessage"
    response = requests.post(url, json=data)
    # return JsonResponse({'status': response.status_code})    
    return render(request, 'main/mainpage.html')


def currency(request):
    driver = webdriver.Chrome()
    driver.get('https://ru.investing.com/currencies/usd-kzt?ysclid=le3xenttgf36537185')

    course = driver.find_element('xpath', "//span[contains(@class, 'text-2xl')]")
    resultk, resultu = 0, 0
    if request.method == 'POST':
        input_valuek = int(request.POST['input_valuek'])
        input_valueu = int(request.POST['input_valueu'])
        resultu = input_valuek * float(course.text[:3])
        resultk = float(course.text[:3]) // input_valueu
        
    
    context = {
        'title': 'Main Page',
        'course': float(course.text[:3]),
        'result': resultk,
        'resultu': resultu,
    }
    return render(request,'main/currency.html', context=context)

from .forms import MyModelForm


def my_view(request, id):
    my_model_instance = Cart(idUser = request.user.pk, idCourse = id)
    my_model_instance.save()
        
    user = request.user.pk
    videos = Video.objects.filter(idCourse=id)
    menu = Course.objects.filter(id=id)
    lesson = LessonContainer.objects.filter(idUser=user, idCourse=id)
    context = {
        'title': "Coursepage",
        'menu': menu,
        'videos': videos,
        'id': id,
        'lesson': lesson,
    }    
    return render(request, 'main/coursepage.html', context)

def cart(request):

    cartItems = Cart.objects.filter(idUser = request.user.pk)
    cart = []
    idc = []
    price = []
    for c in cartItems:
        course = Course.objects.filter(pk =c.idCourse)
        cart.append([course[0].title, course[0].price])
        idc.append(c.idCourse)
        price.append(course[0].price)
    overall = 0    
    for p in price:
        overall+=p
            
    context = {
        'cart': cart,
        'price': price,
        'overall': overall,
        'idc': idc,
    }
    return render(request, 'main/cart.html', context)

def payall(request):
    user = request.user.pk
    cartItems = Cart.objects.filter(idUser = request.user.pk)
    
    for c in cartItems:
        lesson = LessonContainer.objects.create(idUser=user, idCourse=c.idCourse)
        lesson.save()
        Cart.objects.filter(idCourse = c.idCourse).delete()
    
    return redirect('profile')

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView

class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(APIView):
    def get(self, request, id):
        users = User.objects.filter(pk = id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class UserListAll(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)   
     
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(model_to_dict(user))
    
    
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class SendMessageView(APIView):
    def post(self, request, format=None):
        data = request.data
        # data = {'form': 'hello'}
        response = requests.post('http://localhost:4000/receive_message/', data=data)
        print('Proceed')
        return Response(response.json())

def map(request):
    context = {
        'title': 'Maps'
    } 
    
    return render(request, 'main/map.html', context)
