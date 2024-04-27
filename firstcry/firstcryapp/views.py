import io
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Count, F, Value
from django.contrib.auth.models import auth
from firstcryapp.utils import generate_otp, send_otp_email
from .models import  CroppedImage, User, address, brands, cart, categories, color, coupon, order, order_items, testimage, products, variation, whishlist,return_order
from django.contrib import messages
import re
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import ImageUploadForm
import base64
import xlsxwriter
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template

from xhtml2pdf import pisa




# testing image croping--------------



# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Customize the login template
    success_url = reverse_lazy('user_login')

def detailedpage(request,pk):
    details = products.objects.all().filter(category=pk)
    print(details)
    return render(request,'selectproductnotLogin.html',{'details':details})

def first(request):
    products = categories.objects.all().exclude(image='')
    context = {'products':products}
 
    return render(request,'index.html',context)

def register(request):
    if 'name' in request.GET:
        val = 1
    else:
        val = 0
    return render(request, 'for_otp.html',{'val':val})
def reg(request):
    return render(request,'register.html')


def forgotpwd(request):
    if request.method == 'POST':
        email = request.session.get('email')
        new_password= request.POST.get('pwd')
        if email:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'data':'success'})
        else:
            return JsonResponse()
        

def pwd_verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('email')
        submitted_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp')
        email = request.session.get('email')
        if submitted_otp == generated_otp:
            print(email)
            return render(request, 'resetpwd.html',{'email' :email})
        
        messages.error(request, "Invalid OTP")
        return render(request, 'otp_verify.html', {'error': 'Invalid OTP'})
    return render(request, 'otp_pwd_verify.html')


def request_otp(request):
    if request.method == 'POST':
        request.session.flush()
        email = request.POST.get('email')
        
        if 'forgot' in request.POST:
            val = 1
        else:
            val = 0
        valid=is_valid_email(email)
        if valid:
            user = User.objects.all().filter(email=email)
# forgot Password goes here --------------------------
            if 'forgot' in request.POST:
                val = 1
                if user:
                    generated_otp = request.session.get('generated_otp')

                    if generated_otp:
                        # Resend OTP
                        #send_otp_email(email, generated_otp)
                        return render(request, 'otp_pwd_verify.html')
                    else:
                        # New OTP generation and sending
                        otp = generate_otp()
                        print(otp)
                        #send_otp_email(email, otp)
                        request.session['generated_otp'] = otp
                        print(otp)
                        request.session['email'] = email
                        return render(request, 'otp_pwd_verify.html')
                    
                else:
                    messages.info(request,'Your are not Registered with Us')
                    return render(request, 'for_otp.html',{'val':1})

            
            else:
                val = 0
# For senting OTP for registeration
                if user:
                    messages.info(request,'Your are already Registered with Us')
                    return render(request, 'for_otp.html')
                else:
                    generated_otp = request.session.get('generated_otp')
                    if generated_otp:
                        # Resend OTP
                        send_otp_email(email, generated_otp)
                        return redirect('verify_otp')
                    else:
                        # New OTP generation and sending
                        print("yes")
                        otp = generate_otp()
                        print(otp)
                        send_otp_email(email, otp)
                        request.session['generated_otp'] = otp
                        print(otp)
                        request.session['email'] = email
                        return render(request, 'otp_verify.html')
        else:
            messages.info(request,'Email should be in format')
            return render(request, 'for_otp.html',{'val':val})
    return False

def resend_otp(request):
    if 'email' in request.session:
        email = request.session['email']
        otp = generate_otp()
        send_otp_email(email, otp)
        request.session['generated_otp'] = otp
        print(otp)
        return redirect('verify_otp')
    else:
        # Handle the case when there is no email in the session
        return HttpResponse("Email not found in session.")


def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('email')
        submitted_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp')
        email = request.session.get('email')
        if submitted_otp == generated_otp:
            return render(request, 'register.html',{'email' :email})
        
        messages.error(request, "Invalid OTP")
        return render(request, 'otp_verify.html', {'error': 'Invalid OTP'})
    return render(request, 'otp_verify.html')

def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)

def validate_mobile_number(mobile_number):
    pattern = re.compile(r'^\d{10}$')
    return bool(pattern.match(mobile_number))


def registration(request):
    if request.method == 'POST':
        email = request.session.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phonenumber')
        password1 = request.POST.get('password1')
        password2=request.POST.get('password2')
        if validate_mobile_number(phone):
            if password1 == password2:
                user = User.objects.create_user(email=email,first_name=firstname,last_name=lastname,password = password1,mobile=phone)
                user.save()
                return render(request, 'index.html',{'email' :email})
            else:
                messages.info(request,'Password and confirm password must match')
                return render(request, 'register.html',{'email' :email})
        else:
            messages.info(request,'not a valid Phone Number')
            return render(request, 'register.html',{'email':email})
    pass

# User Register Ends Here --------------------------------------------------------------


# Login ---------------------------------------------------------------

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        valid=is_valid_email(email)
        if valid:
            user = authenticate(email=email,password=password)
            if user :
                login(request, user)
                print("thish",user)
                ban = user.ban_status
                if user.is_staff:
                    request.session['email'] = email
                    return redirect(adminhome)
                if ban:
                    messages.info(request,'You are banned to access please contact administator')
                    return redirect(user_login)
                else:
                    request.session['email'] = email
                   
                    addr = address.objects.all().filter(user=user.id)
                    if addr:
                        return redirect(userhome)
                    else: 
                        return redirect(show_address)
                
            else:
                messages.info(request,'invalid username or password')
                return redirect(user_login)
        else:
            messages.info(request,'invalid username or password')
            return redirect(user_login)
    else:
        return render(request,'login.html')

    
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def userhome(request):
    if 'email' in request.session:
        email =  request.session['email'] 
        uname = User.objects.get(email=email)
        product = categories.objects.all().exclude(image='')
        #boyscategory =categories.objects.all().filter(Q(gender="Unisex") | Q(gender="Boys")).order_by('-id')
        boyscategory =categories.objects.all().filter(gender="Boys").order_by('-id')
        
        girlscategory = categories.objects.all().filter(Q(gender="Unisex") | Q(gender="Girls")).order_by('-id')
        print(boyscategory)
        brand = brands.objects.all()
        context1 = {'products':product}
        uid = User.objects.get(email=email).pk
        mydata = User.objects.filter(pk= uid).values()
        context2 = {'mydata':mydata}
        data ={'products':product,'mydata':mydata,
               'brand':brand,
               'boyscateg':boyscategory,
               'girlscateg':girlscategory}
        return render(request,'userhome.html',data)
    return redirect(user_login)

from django.db.models import Sum
from django.db.models.functions import ExtractMonth

@user_passes_test(lambda u: u.is_staff)
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')    
def adminhome(request):
    today = datetime.now()
    #start_date = end_date - timedelta(days=7)
    #print(start_date)
  
    start_date = today - timedelta(weeks=1)
    end_date = today
    order_data = order.objects.filter(date__range=[start_date,end_date ])
    return_data = return_order.objects.filter(date__range=[start_date,end_date ])
    total = 0
    return_amount = 0
    for item in order_data:
        if item.total_amount:
            total = total+  item.total_amount

    for item in return_data:
        if item.order.total_amount:
            return_amount = return_amount + item.order.total_amount
    total_value = total - return_amount
    order_count = order_data.count()
    # testing for correct count  
    top_selling_products_with_count = order_items.objects.values('product_id') \
                                                .annotate(count=Count('product_id')) \
                                                .order_by('-count')[:10]

    # Retrieve the corresponding Product objects and create a list of tuples
    top_selling_product = [(products.objects.get(id=item['product_id']), item['count']) 
                            for item in top_selling_products_with_count]
    


    top_selling_productsIds = order_items.objects.values('product_id') \
                                    .annotate(total_quantity_sold=Sum('quantity')) \
                                    .order_by('-total_quantity_sold')[:10]\
                                    .values_list('product_id', flat=True)
    top_selling_products = products.objects.filter(id__in=top_selling_productsIds)
 
    top_selling_products_dict = products.objects.in_bulk(top_selling_productsIds)
    top_selling_products = [top_selling_products_dict[id] for id in top_selling_productsIds]
    print(top_selling_products)
    data = {'order_count':order_count,
                'total':total_value,'bestpro':top_selling_products
                }
    return render(request,'adminhome1.html',data)
    

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect(first)
    
# Barchart-------------------------------------
@user_passes_test(lambda u: u.is_staff)
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)   
@login_required(login_url='user_login')
def get_monthly_order_data(request):
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Define the start month
    start_month = 1  # January

    # Create a list to store the months
    monthsnum = []

    # Loop through each year and month from the start year to the current year/month
    for year in range(2024, current_year + 1):
        start = start_month if year == current_year else 1
        end = current_month if year == current_year else 12
        for month in range(start, end + 1):
            monthsnum.append(month)

    # Now, months contains the list of month numbers from January 2024 up to the current month
    monthly_sales_order_count = order.objects.filter( date__year=current_year,
        date__month__lte=current_month).values('date__month').annotate(order_count=Count('id'))
    print(monthly_sales_order_count)

    monthdata = []
    for i in reversed(monthly_sales_order_count):
        monthdata.insert(0,i['order_count'])
    
    monthdata.reverse() 
    print(monthdata)
   
    length_difference = len(monthsnum) - len(monthdata)
    monthdata.extend([0] * length_difference)
    monthdata.reverse() 
    print(monthdata)

    
    # for line chart
    linechartMonthData = []
    monthly_totals = order.objects.annotate(month=ExtractMonth('date')).values('month').annotate(total_amount=Sum('total_amount'))
    for i in reversed(monthly_totals):
        linechartMonthData.append(float(i['total_amount']))

    
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_names = [months[number - 1] for number in monthsnum]
    
    l_difference = len(monthsnum) - len(linechartMonthData)
    linechartMonthData.extend([0] * l_difference)
   
    linechartMonthData.reverse() 
    print(linechartMonthData) 
    return JsonResponse({'label':month_names,'varibles':monthdata,'ldata':linechartMonthData}, safe=False)

#changing chart data
@user_passes_test(lambda u: u.is_staff)
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)   
@login_required(login_url='user_login')
def changeChartData(request):
    value = request.GET.get('value')
    print("this value",value)
    if value == 'month':
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Define the start month
        start_month = 1  # January

        # Create a list to store the months
        monthsnum = []

        # Loop through each year and month from the start year to the current year/month
        for year in range(2024, current_year + 1):
            start = start_month if year == current_year else 1
            end = current_month if year == current_year else 12
            for month in range(start, end + 1):
                monthsnum.append(month)

        # Now, months contains the list of month numbers from January 2024 up to the current month
        monthly_sales_order_count = order.objects.filter( date__year=current_year,
            date__month__lte=current_month).values('date__month').annotate(order_count=Count('id'))
        print(monthly_sales_order_count)

        monthdata = []
        for i in reversed(monthly_sales_order_count):
            monthdata.insert(0,i['order_count'])
        
        monthdata.reverse() 
        print(monthdata)
    
        length_difference = len(monthsnum) - len(monthdata)
        monthdata.extend([0] * length_difference)
        monthdata.reverse() 
        print(monthdata)

        
        # for line chart
        linechartMonthData = []
        monthly_totals = order.objects.annotate(month=ExtractMonth('date')).values('month').annotate(total_amount=Sum('total_amount'))
        for i in reversed(monthly_totals):
            linechartMonthData.append(float(i['total_amount']))

        
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_names = [months[number - 1] for number in monthsnum]
        
        l_difference = len(monthsnum) - len(linechartMonthData)
        linechartMonthData.extend([0] * l_difference)
    
        linechartMonthData.reverse() 
     
        return JsonResponse({'label':month_names,'varibles':monthdata,'ldata':linechartMonthData}, safe=False)
    elif value == 'week':
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Define start and end dates of the current month
        start_date = datetime(current_year, current_month, 1)
        end_date = start_date + timedelta(days=32)

        # Segment the month into weeks
        week_start = start_date
        week_end = week_start + timedelta(weeks=1)
        weeks_count = []
        week_amount = []

        while week_start < end_date:
            # Aggregate data for the week
            weekly_data = order.objects.filter(
                date__range=[week_start, week_end]
            ).aggregate(
            order_count=Count('id'),
            total_amount=Sum('total_amount') )

            # Extract data for the week
                    # Extract data for the week
            order_count = weekly_data['order_count'] or 0
            total_amount = weekly_data['total_amount'] or 0
             # Append the data to the list of weeks
            weeks_count.append( order_count)
            week_amount .append( total_amount)

            # Move to the next week
            week_start = week_end
            week_end = min(week_start + timedelta(weeks=1), end_date)

        # Prepare labels for each week
        week_labels = [f"Week {i}" for i in range(1, len(weeks_count) + 1)]
        print("week order count",weeks_count)
        print("week revnue",week_amount)
        return JsonResponse({'label':week_labels,'varibles':weeks_count,'ldata':week_amount}, safe=False)
    elif value == 'year':
        current_year = datetime.now().year

        # Define start and end years for the last 5 years
        start_year = current_year - 4
        end_year = current_year

        # Segment the years
        yearly_data = []
        yearly_count = []
        yearly_amount = []

        for year in range(start_year, end_year + 1):
            # Aggregate data for the year
            yearly_sales_order_count = order.objects.filter(
                date__year=year).values('date__year').annotate(
                order_count=Count('id'),total_amount=Sum('total_amount')).order_by('date__year')

            # Extract data for the year
            year_data = yearly_sales_order_count.first()
            if year_data:
                order_count = year_data['order_count'] or 0
                total_amount = year_data['total_amount'] or 0
            else:
                order_count = 0
                total_amount = 0

            # Append the data to the list of years
            yearly_data.append({'year': year, 'order_count': order_count, 'total_amount': total_amount})
            yearly_count.append(order_count)
            yearly_amount.append(total_amount)
        # Prepare labels for each year
        year_labels = [str(year['year']) for year in yearly_data]
        return JsonResponse({'label':year_labels,'varibles':yearly_count,'ldata':yearly_amount}, safe=False)
   


# user personal data ------------------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def personal_data(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        return render(request,'user_personal.html',{'user':user})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def updateuser(request):
    if 'email' in request.session:
        userid = User.objects.get(email=request.session['email']).pk
        user = User.objects.get(id=userid)
        user.first_name=request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.mobile = request.POST.get('mobile')
        user.save()
        return redirect(personal_data)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def show_changepassword(request):
    if 'email' in request.session:
        return render(request,'user_changepassword.html')
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def change_password(request):
    if 'email' in request.session:
        email = request.session['email']
        password = request.POST.get('oldpassword')
        npass = request.POST.get('newpassword1')
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            user = User.objects.get(email=email)
            user.set_password(npass)
            user.save()
            return JsonResponse({'success': True})
        else:
            print("NOt")
            return JsonResponse({'error': 'Passwords do not match'})
        print("ok")
        return redirect(show_changepassword)
    return redirect(user_login)


# User Address Management ----------------------------------

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def show_address(request):
    if 'email' in request.session:
        email = request.session['email']
        userid = User.objects.get(email=email).pk
        addr = address.objects.all().filter(user=userid)
        count = addr.count()
        if not addr:
            start = True
        else:
            start = False
        return render(request,'user_address.html',{'address':addr,'start':start,'count':int(count)})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def update_address(request,pk):
        if 'email' in request.session:
            if request.method =='POST':
                addr = address.objects.get(id=pk)         
                addr.name= request.POST.get('name')
                addr.house_name = request.POST.get('housename')
                addr.street_name = request.POST.get('streetname')
                addr.landmark = request.POST.get('landmark')
                addr.pincode = request.POST.get('pincode')
                addr.city = request.POST.get('city')
                addr.state = request.POST.get('state')
                addr.country = request.POST.get('country')
                addr.default_value = True
                addr.save()
                print("saved")
                return redirect(show_address)
        return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def add_address(request):
    if request.method =='POST':
        if request.session['email']:
            email = request.session['email']
            user = User.objects.get(email=email)
            addr1 = address.objects.all().filter(user=user.id) 
            if addr1:
                for items in addr1:
                    ad = address.objects.get(id=items.id)
                    ad.default_value = False
                    print("yes")
                    ad.save()
            addr = address()           
            addr.user=user
            addr.name= request.POST.get('name')
            addr.house_name = request.POST.get('housename')
            addr.street_name = request.POST.get('streetname')
            addr.landmark = request.POST.get('landmark')
            addr.pincode = request.POST.get('pincode')
            addr.city = request.POST.get('city')
            addr.state = request.POST.get('state')
            addr.country = request.POST.get('country')
            addr.default_value = True
            addr.save()
            if 'cart' in request.POST:
                return redirect(confirmorder)
            return redirect(show_address)
        return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def delete_address(request,pk):
    if 'email' in request.session:
        if request.method =='POST':
                user = User.objects.get(email=request.session['email'])
                addr = address.objects.get(id = pk)
                if addr.default_value == True:
                    addr1 = address.objects.filter(user = user).exclude(id=pk)
                    print("this",addr1)
                    for items in addr1:
                        if items.default_value == True:
                            ids = 0
                            break
                        else:
                            ids = items.id
                    print(ids)
                    if ids == 0:
                        addr.delete()
                    else:
                        ad = address.objects.get(id=ids)
                        ad.default_value = True
                        ad.save()
                        addr.delete()
                else:
                    addr.delete()
                return redirect(show_address)     
    return redirect(user_login) 

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def make_default(request,pk):
        if 'email' in request.session:
            email = request.session['email']
            n = request.GET.get('n')
            print(n)
            user = User.objects.get(email=email)
            addr1 = address.objects.all().filter(user=user.id)
            
            if addr1:
                for items in addr1:
                    ad = address.objects.get(id=items.id)
                    ad.default_value = False
                   
                    ad.save()
            
            addr2 = address.objects.get(id=pk)
            addr2.default_value = True
            addr2.save()
            if n:
                return redirect(confirmorder)
            else:
                return redirect(showcart)
        return redirect(user_login)




# to retrieve all user data ----User management------------------------------------



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')  
def alluser(request):
    if 'email' in request.session:
        details = User.objects.all().order_by('pk').values().exclude(email='admin@admin.com')
        return render(request,'adminuser1.html',{'users':details})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def edituser(request,pk):
    if 'email' in request.session:
        instance = User.objects.filter(pk=pk).values()
        return render(request,'adminedituser1.html',{'users':instance})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True) 
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')    
def update_user(request,pk):
    instance_edit = User.objects.get(pk=pk)
    if request.POST:
        if 'email' in request.session:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            instance_edit.first_name = firstname
            instance_edit.last_name =lastname
            instance_edit.email = email
            instance_edit.mobile=mobile
            instance_edit.save()
            return redirect(alluser)
        return redirect(user_login)
    
    
    
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def block_user(request,pk):
    if 'email' in request.session:
        user = User.objects.get(id=pk)
        user.ban_status = True
        user.save()
        return redirect(alluser)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def unblock_user(request,pk):
    if 'email' in request.session:
        user=User.objects.get(id=pk)
        user.ban_status = False
        user.save()
        return redirect(alluser)
    return redirect(user_login)


# add category-------- Category management--------------------------------------------------



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def category(request):
    if 'email' in request.session:
        return render(request,'admin_add_category.html')
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_category(request):
    if 'email' in request.session:
        if request.method == 'POST':
            instance = categories()
            instance.titile = request.POST.get('titile')
            instance.description = request.POST.get('description')
            instance.visibility = request.POST.get('add')
            if 'image' in request.FILES:
                instance.image = request.FILES['image']
            instance.type = request.POST.get('types')
            instance.gender = request.POST.get('gender')
            #instance = categories(titile=name,description=descrip,image=image,visibility=add, type=type,gender=gender)
            instance.save()
            return redirect(view_category)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def view_category(request):
    if 'email' in request.session:
        if request.method =='POST':
            details = categories.objects.all().order_by('pk').values()
            print(details)
            return render(request,'admin_view_category.html',{'details':details})
        details = categories.objects.all().order_by('pk').values()
        return render(request,'admin_view_category.html',{'details':details})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def edit_category(request,pk):
     details = categories.objects.filter(pk=pk).values()
     print(details)
     return render(request,'admin_edit_category.html',{'desc':details})

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def update_category(request,pk):
    if 'email' in request.session:
        instance = categories.objects.get(pk=pk)
        if request.method == 'POST':
            instance.titile = request.POST.get('titile')
            instance.description = request.POST.get('description')
            instance.type = request.POST.get('types')
            instance.gender = request.POST.get('gender')
            if 'image' in request.FILES:
                instance.image = request.FILES['image']
        

            instance.save()
            return redirect(view_category)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def delete_category(request,pk):
    if 'email' in request.session:
        instance= categories.objects.get(pk=pk)
        instance.soft_delete()
        return redirect(view_category)
    return redirect(user_login)



# add and update product------ Product Management------------------------------------------


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def product(request):
    if 'email' in request.session:
        cat = categories.objects.all()
        prod = products.objects.all()
        col = color.objects.all()
        brand = brands.objects.all()
        details = {'context':cat,
                   'context2':prod,
                   'color':col,
                   'brand':brand}
        return render(request,'adminproduct1.html' ,details)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_product(request):
    if 'email' in request.session:
        if request.method == 'POST':
            prod = products()
            variant = variation() 
            variant.zerotothreeM = request.POST.get('0to3')
            variant.threetosixM = request.POST.get('3to6')
            variant.sixtonineM = request.POST.get('6to9')
            variant.ninetotwelveM = request.POST.get('9to12')
            variant.twelvetoeighteenM = request.POST.get('12to18')
            variant.eighteentotwentyfourM = request.POST.get('18to24')
            variant.twotofourY = request.POST.get('2to4y')
            variant.fourtosixY = request.POST.get('4to6y')
            variant.sixtoeightY =request.POST.get('6to8y')
            variant.total = request.POST.get('total')
            variant.colors = color.objects.get(id = request.POST.get('color'))
            variant.save()
            vobj = variation.objects.get(id = variant.pk)
            id = request.POST.get('categ')
            obj = categories.objects.get(id=id)
            prod.category = obj
            prod.brand = brands.objects.get(id = request.POST.get('brand'))
            prod.name = request.POST.get('pname')
            prod.image = request.FILES['image']
            prod.description = request.POST.get('desciption')
            prod.necktype = request.POST.get('neck')
            print(request.POST.get('neck'))
            prod.sleevetype = request.POST.get('sleeve')
            print( request.POST.get('sleeve'))
            prod.length = request.POST.get('length')
            prod.waist = request.POST.get('waist')
            prod.price = request.POST.get('price')
            prod.deal = request.POST.get('deal')
            prod.Offer_price = request.POST.get('offer')
            prod.varient = vobj 
            prod.save()
            return JsonResponse({'successs':'success'})
            messages.info(request,'Added Successfully')
            return redirect(product)
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def change_for_types(request):
    if request.method == 'GET':
        value = request.GET.get('selected_value')
        categ = categories.objects.get(id = value)
        print(categ.type)
        response_data = categ.type
        return JsonResponse({'res':response_data})


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_color(request):
    if 'email' in request.session:
        if request.method == 'GET':
            name = request.GET.get('name')
            code = request.GET.get('code')
            instance = color(name=name,code = code)
            instance.save()
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_color_js(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        code = request.GET.get('code').lower()
        b = 0
        print(name,code)
        col = color.objects.all()
        for i in col:
            if i.code == code:
                b = 1
                break
        if b == 0:        
            instance = color(name=name,code = code)
            instance.save()
            col = color.objects.all()
            return render(request, 'reloading_color.html', {'color':col})
        else:
            return JsonResponse({'value':1})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def editproduct(request ,pk):
    if 'email' in request.session:
        product = products.objects.get(id=pk)
        cat = categories.objects.all()  
        return render(request,'admin_edit_product1.html',{'details':product,'context':cat})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def productupdation(request,pk):
    if 'email' in request.session:
        if 'update' in request.POST:
            instance=products.objects.get(id=pk)
            if request.method == 'POST':
                instance.name = request.POST.get('name')
                if 'image' in  request.FILES:
                    instance.image = request.FILES['image']

                instance.description = request.POST.get('description')
                instance.necktype = request.POST.get('necktype')
                categ = categories.objects.get(id=request.POST.get('categ'))
                instance.category = categ
                instance.sleevetype = request.POST.get('sleevetype')
                instance.gender = request.POST.get('gender')
                instance.qnty = request.POST.get('qnty')
                instance.price = request.POST.get('price')
                instance.deal = request.POST.get('deal')
                instance.Offer_price =request.POST.get('offer')
                instance.save()
                print("saved")
                print(request.POST)
                return redirect(showproduct)
        else:
            return redirect(edit_varient,pk)
        return redirect(showproduct)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def deleteproduct(request,pk):
    if 'email' in request.session:
        instance=products.objects.get(id=pk)
        instance.soft_delete()
        return redirect(showproduct)
    return redirect(user_login)



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def showproduct(request):
    if 'email' in request.session:
        product = products.objects.all().order_by('pk')
        wishli = whishlist.objects.all()
        return render(request,'admin_view_product1.html',{'products':product,'wishlist':wishli})
    return redirect(user_login)


# varient management -------------------------------------------

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def view_product_varient(request,pk):
    if 'email' in request.session:
        product = products.objects.get(id = pk)
        print(product.varient.zerotothreeM)
        return render(request,'admin_view_product_varient.html',{'details':product})
    return redirect(user_login)



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def edit_varient(request,pk):
    if 'email' in request.session:
        product = products.objects.get(id = pk)
        col = color.objects.all()
        return render(request,'admin_edit_varient.html',{'details':product,'color':col})
    return redirect(user_login)



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def update_varient(request,pk):
    if 'email' in request.session:
        if request.method=='POST':
            pro = products.objects.get(id=pk)
        
            variant = variation.objects.get(id=pro.varient.id)
            variant.zerotothreeM = request.POST.get('0to3')
            variant.threetosixM = request.POST.get('3to6')
            variant.sixtonineM = request.POST.get('6to9')
            variant.ninetotwelveM = request.POST.get('9to12')
            variant.twelvetoeighteenM = request.POST.get('12to18')
            variant.eighteentotwentyfourM = request.POST.get('18to24')
            variant.twotofourY = request.POST.get('2to4y')
            variant.fourtosixY = request.POST.get('4to6y')
            variant.sixtoeightY =request.POST.get('6to8y')
            variant.total = request.POST.get('total')
            variant.colors = color.objects.get(id = request.POST.get('color'))
            variant.save()
            product = products.objects.get(id=pk)
            messages.info(request,'updated Successfully')
            return render(request,'admin_view_product_varient.html',{'details':product})
           
        return redirect(user_login)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def back_product(request):
    if 'email' in request.session:
        return redirect(showproduct)
    return redirect(user_login)



# Brand Management-----------------------------------------------------------------



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def view_brand(request):
    if 'email' in request.session:
        brand = brands.objects.all()
        return render(request,'admin_view_brands.html',{'details':brand})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_brand_page(request):
    if 'email' in request.session:
        return render(request,'admin_add_brand.html')
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_brand(request):
    print("thish is working")
    if 'email' in request.session:
        name = request.POST.get('name')
        desc = request.POST.get('description')
        specs = request.POST.get('specs')
        image = request.FILES['logo']
        print(image)
        br = brands(name=name,description = desc,specs = specs,logo=image)
        br.save()
        return JsonResponse({"status":"success"})
        # messages.info(request,'Brand added successfully')
        #return redirect(view_brand)
    return redirect(user_login)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def add_brand_js(request):
    
    if 'email' in request.session:
        print("ok")
        br = brands()
        print(request.GET.get('brandname'))
        br.name = request.GET.get('brandname')
        br.description = request.GET.get('description')
        if 'specs' in request.GET:
            br.specs = request.GET.get('specs')
        #br.logo = request.FILES['logo']
        print(request.FILES['logo'])
        #br.save()
        return JsonResponse("ok")
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def edit_brand_page(request,pk):
    if 'email' in request.session:
        brand = brands.objects.get(id=pk)
        return render(request,'admin_edit_brand.html',{'details':brand})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)  
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')   
def update_brand(request,pk):
    if 'email' in request.session:
        brand = brands.objects.get(id = pk)
        brand.name = request.POST.get('name')
        brand.description = request.POST.get('description')
        if request.POST.get('specs'):
            brand.specs = request.POST.get('specs')
        if 'logo' in request.FILES:
            brand.logo = request.FILES['logo']
        brand.save()
        return JsonResponse({'success':'success'})
        # messages.info(request,'Updated success')
        # return redirect(edit_brand_page,pk)
    return redirect(user_login)




# admin View all orders and update status---------------------------------

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def view_order(request):
    if 'email' in request.session:
        orders = order.objects.all().order_by('-pk')
        return render(request,'admin_view_order.html',{'orders':orders})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def orderDetails(request,pk):
    print("ok")
    if 'email' in request.session:
        ord = order.objects.get(id=pk)
        orders = order_items.objects.filter(order=ord)
        return render(request,'admin_view_order_detailed.html',{'orders':orders,'ord':ord})


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def order_processed(request,pk):
    if 'email' in request.session:
        orders = order.objects.get(id=pk)
        orders.order_status = 'Processed'
        orders.save()
        return redirect(view_order)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def order_shipping(request,pk):
    if 'email' in request.session:
        orders = order.objects.get(id=pk)
        orders.order_status = 'Shipped'
        orders.save()
        return redirect(view_order)  
    return redirect(user_login)



@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def order_deliver(request,pk):
    if 'email' in request.session:
        orders = order.objects.get(id=pk)
        orders.order_status = 'Delivered'
        orders.save()
        return redirect(view_order) 
    return redirect(user_login) 


# user selecr from menu shop by size--------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def menulinkSize(request):
    if 'email' in request.session:
        if request.GET.get('size'):
            size = request.GET.get('size')
            if 'cat' in request.session:
                del request.session['cat']
            annotations = {f'{size}_value': F('varient__' + size)}
            filtered_products = products.objects.annotate(**annotations).filter(**{f'{size}_value__gt': 0})
            return render(request,'4.both_type_products.html',{'details':filtered_products ,})
    return redirect(user_login)

# User select from category ------------------
        
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def detailpage(request,pk):
    if 'email' in request.session:
        email = request.session['email']
        uid =  User.objects.get(email=email).pk
        request.session['cat']=pk
        print("thishs",request.session['cat'])
        boyscategory =categories.objects.all().filter(Q(gender="Unisex") | Q(gender="Boys")).order_by('-id')
        
        types = categories.objects.get(id = pk)
        cattype = ''
        print(types)

        details = products.objects.all().filter(category=pk).order_by('-id')
        wishli = whishlist.objects.all().filter(user_id=uid)
 
        cattype = types.type
        print(cattype)
        boyscategory1 =categories.objects.all().filter(gender="Boys").order_by('-id')
        
        if cattype == '1':
            return render(request,'2.shirt_type_products.html',{'details':details ,'wishlist':wishli,'boyscateg':boyscategory1})
        elif cattype == '2':
            return render(request,'3.pants_type_products.html',{'details':details ,'wishlist':wishli,'boyscateg':boyscategory1})
        else: 
            return render(request,'4.both_type_products.html',{'details':details ,'wishlist':wishli,'boyscateg':boyscategory1})
       

    return redirect(user_login)






#filtered products---------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def filter_data(request):
    if 'email' in request.session:
        if 'cat' in request.session:
            cat = request.session['cat']
            allproduct = products.objects.all().filter(category=cat).order_by('-id')
        else:
             allproduct = products.objects.all().order_by('-id')
        if 'cat' in request.session:
            print("session",request.session['cat'])
        ctype = request.POST.getlist('necktype[]')
        print("neck   :",ctype)
        offer_price = request.POST.getlist('Offer_price[]')
        length = request.POST.getlist('length[]')
        size = request.POST.getlist('size[]')
        print(size)
        prices = []
        num = ""
        print(type(ctype))

        combined_filter = Q()
        if len(ctype)>0:
            allproduct = allproduct.filter(necktype__in = ctype)
        if len(offer_price)>0:
            x = offer_price
            y = ''.join(x) # converting list into string
            for char in y:
                if char.isdigit():
                    num += char
                elif num:
                    prices.append(int(num))
                    num = ""
            if num:
                prices.append(int(num))
            allproduct = allproduct.filter(Offer_price__range =(prices[0],prices[len(prices)-1]))
            print(prices[0])
            print(prices[len(prices)-1])
        if len(length)>0:
             allproduct = allproduct.filter(length__in = length)
        if len(size) >0:
                for i in size:
                    print(i)
                    filter_key = f"varient__{i}__gt"
                    filter_query = Q(**{filter_key: 0})
                    combined_filter |= filter_query
            # for i in range(len(size)):
            #     print(size[i])
            #     filter_params = {
            #         f"varient__{size}__gt": 0
            #         }
                allproduct = allproduct.filter(combined_filter)
        print(allproduct)
        print(prices)
       
        t=render_to_string('detailed_filter.html',{'data':allproduct}, request=request)
      
        return JsonResponse({'data':t})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def selectoneproduct(request,pk):
    if 'email' in request.session:
        email=request.session['email']
        userid = User.objects.get(email=email).pk
        if 'size' in request.GET:
            print(request.GET)
        size = request.GET.get('size')
        
        details = products.objects.all().filter(id=pk)
        wish = whishlist.objects.all().filter(product=pk,user=userid,size=size)
        car = cart.objects.all().filter(product=pk,user=userid,size=size) # for goto cart button
        
        print("thishs sixe",size)
        if size:
            default = size
        else:
            for i in details:
                if i.varient.zerotothreeM > 0:
                    default = "zerotothreeM"
                elif i.varient.threetosixM > 0:
                    default = "threetosixM"
                elif i.varient.sixtonineM > 0:
                    default ="sixtonineM"
                elif i.varient.ninetotwelveM > 0:
                    default = "ninetotwelveM"
                elif i.varient.twelvetoeighteenM > 0:
                    default = "twelvetoeighteenM"
                elif i.varient.eighteentotwentyfourM > 0:
                    default = "eighteentotwentyfourM"
                elif i.varient.twotofourY > 0:
                    default = "twotofourY"
                elif i.varient.fourtosixY > 0:
                    default = "fourtosixY"
                elif i.varient.sixtoeightY > 0:
                    default = "sixtoeightY"
                else:
                    default = "nodefault"
        for i in details:
            if i.varient.__getattribute__(default) <=0:
                default = "nodefault"
        wishlist ={}
        cartdata ={}
        if car:
            cartdata ={'yes':'yes'}
        else:
            cartdata = {'no':False}
        if wish:
            wishlist={'yes':True}
        else:
            wishlist={'yes':False}
        if request.POST:
            print(list(request.POST.keys())[1])
            if hasattr(variation,list(request.POST.keys())[1]):
                print("yes")
                default = (list(request.POST.keys())[1])
        print(default)

        return render(request,'oneprodwithlogin.html',{'details':details,'wish':wishlist,'cart':cartdata,'default':default})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def oneprod_filter(request):
    if 'email' in request.session:
        default = request.POST.get('size')
        pk = request.POST.get('pid')
        print("ok")
        email=request.session['email']
        userid = User.objects.get(email=email).pk
        details = products.objects.all().filter(id=pk)
        wish = whishlist.objects.all().filter(product=pk,user=userid,size=default)
        car = cart.objects.all().filter(product=pk,user=userid) # for goto cart button
        wishlist ={}
        cartdata ={}
        if car:
            cartdata ={'yes':True}
        else:
            cartdata = {'yes':False}
        if wish:
            wishlist={'yes':True}
        else:
            wishlist={'yes':False}
        
        t = render_to_string('oneprodwithloginfiltered.html', {'details':details,'default':default,'wish':wishlist,'cart':cartdata})
        return JsonResponse({'data':t})
    return redirect(user_login)


def oneproduct(request,pk):  # one product details with out login
    details = products.objects.all().filter(id=pk)
    return render(request,'oneprodwithoutlogin.html',{'details':details})
    


# add to wish list----------------------------------------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def add_to_wishlist(request):
    if 'email' in request.session:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            email =  request.session['email'] 
            uobject = User.objects.get(email=email)
            probj = products.objects.get(id=product_id)
            size = request.POST.get('size')
            print(size)

            data = {}
            checking =whishlist.objects.filter(product=product_id,user=uobject.id,size=size).count()
            if checking > 0:
                data = {'bool':False}
            else:
                wish = whishlist()
                wish.user=uobject
                wish.product=probj
                wish.size = size
                wish.save()
                data={'bool':True}
            return JsonResponse(data)
    return redirect(user_login)

        
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def remove_from_wishlist(request):
    if 'email' in request.session:   
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            email = request.session['email']
            user = User.objects.get(email=email)
            print("this is ",product_id)
            wish = whishlist.objects.filter(user=user.id,product=product_id)
            print(wish)
            wish.delete()
            data = {'bool':True}
            return JsonResponse(data)
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def wishlistpage(request):
    if 'email' in request.session:
        email =  request.session['email'] 
        uid = User.objects.get(email=email)
        details = whishlist.objects.all().filter(user=uid.id)
        if details:
            starter = False
        else:
            starter = True

        return render(request,'userwishlist.html',{'details':details,'start':starter})
    return redirect(user_login)
    #return render(request,'wishlist.html',{'combined_querysets': combined_querysets})

# add to cart --------------------------------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def add_to_cart(request):
    if 'email' in request.session:
        if request.method == 'POST':
            email =  request.session['email'] 
            uobject = User.objects.get(email=email)
            product_id = request.POST.get('product_id')
            probj = products.objects.get(id=product_id)
          
            if request.POST.get('size'):
                size = request.POST.get('size')
            else:
                if probj.varient.zerotothreeM > 0:
                    size = "zerotothreeM"
                elif probj.varient.threetosixM > 0:
                    size = "threetosixM"
                elif probj.varient.sixtonineM > 0 :
                    size = "sixtonineM"
                elif probj.varient.ninetotwelveM > 0:
                    size = "ninetotwelveM"
                elif probj.varient.twelvetoeighteenM > 0:
                    size = "twelvetoeighteenM"
                elif probj.varient.eighteentotwentyfourM > 0:
                    size = "eighteentotwentyfourM"
                elif probj.varient.twotofourY > 0:
                    size = "twotofourY"
                elif probj.varient.fourtosixY > 0:
                    size = "fourtosixY"
                elif probj.varient.sixtoeightY > 0:
                    size = "sixtoeightY"
            print(size)

            data = {}
            checking =cart.objects.filter(product=product_id,user=uobject.id,size = size).count()
            print(checking)
            if checking > 0:
                data = {'bool':False}
            else:
                print(size)
                add_tocart = cart()
                add_tocart.user=uobject
                add_tocart.product=probj
                add_tocart.size = size
                add_tocart.save()
                data={'bool':True}
            return JsonResponse(data)
    return redirect(user_login)
    
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)  
@login_required(login_url='user_login')   
def showcart(request):
    if 'email' in request.session:
        email = request.session['email']
        user = User.objects.get(email=email)
        cart_items = cart.objects.all().filter(user=user.id)
        total_amount = 0
        if not cart_items:
            starter = True
        else:
            starter = False
        for item in cart_items:
            size = item.size
            if item.product.varient.__getattribute__(size) > 0: 
                total_amount = total_amount+item.product.Offer_price * item.quantity

        alladdr = address.objects.all().filter(user=user.id)
        addr = address.objects.get(user=user,default_value=True)
        return render(request,'usercart.html' ,{'cart_items': cart_items ,'total_amount': total_amount,'start':starter,'address':addr,'alladdress':alladdr})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def update_cart_item(request, item_id):
    if 'email' in request.session:
        user = request.session['email']
        cart_item = cart.objects.get(id=item_id)
        new_quantity = int(request.POST.get('quantity'))
        print("quatinty",new_quantity)
        size = request.POST.get('size')
        print(new_quantity)
        cart_item.quantity = new_quantity
        cart_item.save()
        userid=User.objects.get(email=user)
        # Recalculate the total amount
        cart_items = cart.objects.filter(user=userid.id)
        total_amount = 0
        for item in cart_items:
            #if item.product.varient.__getattribute__(size) > 0:
            print("item offer",item.product.Offer_price)
            print(item.product.name)
            print("item qua",item.quantity)
            total_amount = total_amount+item.product.Offer_price * item.quantity
        # #total_amount = sum(item.product.Offer_price * item.quantity for item in cart_items)
        print(total_amount)
        # Return the updated total amount and total amount for the specific item as JSON
        return JsonResponse({
            'total_amount': total_amount,  
            'item_total_amount': cart_item.product.Offer_price * cart_item.quantity
        })
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def remove_cart_item(request, item_id):
    if 'email' in request.session:
        user = request.session['email']
        cart_item = cart.objects.get(id=item_id)
        cart_item.delete()
        userid=User.objects.get(email=user)
        # Recalculate the total amount
        cart_items =  cart.objects.filter(user=userid.id)
        total_amount = sum(item.product.Offer_price * item.quantity for item in cart_items)
        # Return the updated total amount as JSON
        return JsonResponse({'total_amount': total_amount})
    return redirect(user_login)




# order -----------------------------------------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def paytoproceed(request):
    if 'email' in request.session:
        user = request.session['email']
        user=User.objects.get(email=user)
        cart_items =  cart.objects.filter(user=user.id)
        total = 0
        for item in cart_items:
            total = total+item.product.Offer_price*item.quantity
            size_available = getattr(item.product.varient, item.size)
            print("thishs",size_available)

        
            if size_available is  size_available == 0:
          
                return JsonResponse({"error":"size not available"})
            

        print(total)

        return JsonResponse({"total":total})
    return redirect(user_login)

# Order updating for the link from order history

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def order_product_from_orderhistory(request):
    if 'email' in request.session:
        user = request.session['email']
        paymentId=request.GET.get('payment_id')
        cpnid = request.GET.get('cid')
        paymentmode = request.GET.get('paymentmode')
        totalamount = request.GET.get('total') 
        ordid= request.GET.get('ord') 
        user=User.objects.get(email=user)
        addr = address.objects.get(user=user.id,default_value=True)
        orders = order.objects.get(id=ordid)
        orders.user=user
        orders.user_name = addr.name
        orders.user_housename = addr.house_name
        orders.user_street = addr.street_name
        if addr.landmark:
            orders.user_landmark = addr.landmark
        orders.user_pincode = addr.pincode
        orders.user_city = addr.city
        orders.user_state = addr.state
        orders.user_country =addr.country
        orders.user_mobile = addr.mobile 
        orders.total_amount = totalamount
        orders.payment_method = paymentmode
        if paymentId:
            orders.payment_id = paymentId
        if cpnid:
            coupnobj = coupon.objects.get(id = cpnid)
            orders.coupon = coupnobj
        orders.save()
        return JsonResponse({"status":"success"}) 
    return redirect(user_login)








@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def order_product(request):
    if 'email' in request.session:
        user = request.session['email']
        paymentId=request.GET.get('payment_id')
        cpnid = 0 # initializing coupon id
     
        print("thishs coupon id",cpnid)

        if request.method == 'POST':
            paymentmode = request.POST.get('paymentmode')
            totalamount = request.POST.get('total')
            cpnid = request.POST.get('cid')
        else:
            paymentmode = request.GET.get('paymentmode')
            totalamount = request.GET.get('total')
            cpnid = request.GET.get('cid')
        
        print(paymentmode)
        print(totalamount)
        # if request.POST:
        #     print("thishs",list(request.POST.keys())[1])
        #     totalamount = list(request.POST.keys())[1]
        
        user=User.objects.get(email=user)
        cart_items =  cart.objects.filter(user=user.id)
        addr = address.objects.get(user=user.id,default_value=True)
        orders = order()
        orders.user=user
        orders.user_name = addr.name
        orders.user_housename = addr.house_name
        orders.user_street = addr.street_name
        if addr.landmark:
            orders.user_landmark = addr.landmark
        orders.user_pincode = addr.pincode
        orders.user_city = addr.city
        orders.user_state = addr.state
        orders.user_country =addr.country
        orders.user_mobile = addr.mobile 
        orders.total_amount = totalamount
        orders.payment_method = paymentmode
        if paymentId:
            orders.payment_id = paymentId
        print("xoupon is",cpnid)
        if cpnid:
            coupnobj = coupon.objects.get(id = cpnid)
            orders.coupon = coupnobj
        orders.save()
       

        
        print(paymentId)
       
            # print(item.product.Offer_price)
            # if item.product.varient.__getattribute__(item.size) > 0:
               
                # oreders_items.order=user
                # .product=item.product
                # .user_address = addr
                # .price = item.product.price
                # .deal = item.product.deal
                # .size = item.size
                # .Offer_price=item.product.Offer_price
        
                # .total = total+item.product.Offer_price*item.quantity
        order_obj = order.objects.get(id=orders.pk)
        for item in cart_items:    
            
            orders_items = order_items()
            orders_items.order = order_obj
            orders_items.product = item.product
            orders_items.size = item.size
            orders_items.quantity = item.quantity
            orders_items.price = item.product.price
            orders_items.deal = item.product.deal
            orders_items.Offer_price = item.product.Offer_price
            orders_items.total = item.product.Offer_price*item.quantity
            orders_items.save()

            product = products.objects.get(id=item.product.id)
            varient = product.varient
            varient.total= F('total')-item.quantity
            setattr(varient, item.size, F(item.size) - item.quantity)
            varient.save()
            cart_items.delete()

        if paymentmode == "Paid by Razorpay":
            print("ok")
            return JsonResponse({"status":"success"})
        else:
            return JsonResponse({"status":"success"})               
       
    return redirect(user_login)

# Admin coupon managemnt---------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def show_coupon(request):
    coupons = coupon.objects.all()
    return render(request,'admin_view_coupon.html',{'coupons':coupons})

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def add_coupon_page(request):
    if 'email' in request.session:
        return render(request,'admin_add_coupon.html')
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def add_coupon(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        allcop = coupon.objects.filter(name=name)
        
        if allcop:
            messages.info(request,'Coupon alredy exits')
            return render(request,'admin_add_coupon.html')
        else:
        
            description = request.POST.get('description')
            discount = request.POST.get('discount')
            edate = request.POST.get('edate')
            sdate = request.POST.get('sdate')
            mamount = request.POST.get('mamount')
            cop = coupon()
            cop.name = name
            cop.description = description
            cop.discount = discount
            cop.start_date = sdate
            cop.end_date = edate
            cop.min_amount = mamount
            cop.save()
            messages.info(request,'Added success')
            return render(request,'admin_add_coupon.html')
    


def convert_to_standard_date_format(date_object):
    # Parse the date string to a datetime object
    return date_object.strftime('%Y-%m-%d')

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def show_edit_couponpage(request,pk):
    cop = coupon.objects.get(id = pk)
    start_date_standard_format = convert_to_standard_date_format(cop.start_date)
    end_date_standerd = convert_to_standard_date_format(cop.end_date)
    return render(request, 'admin_edit_coupon.html', {'coupons': cop,'end_date':end_date_standerd, 'start_date_standard_format': start_date_standard_format})


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def update_coupon(request,pk):
    cop = coupon.objects.get(id = pk)
    name = request.POST.get('name')
   
    description = request.POST.get('description')
    discount = request.POST.get('discount')
    edate = request.POST.get('edate')
    sdate = request.POST.get('sdate')
    mamount = request.POST.get('mamount')
    allcop = coupon.objects.filter(name=name)
    if allcop:
        start_date_standard_format = convert_to_standard_date_format(cop.start_date)
        end_date_standerd = convert_to_standard_date_format(cop.end_date)
        messages.info(request,'Coupon alredy exits')
        return render(request, 'admin_edit_coupon.html', {'coupons': cop,'end_date':end_date_standerd, 'start_date_standard_format':start_date_standard_format})
    else:
        
        cop.name = name
        cop.description = description
        cop.discount = discount
        cop.start_date = sdate
        cop.end_date = edate
        cop.min_amount = mamount
        print("thishs",cop.start_date)     
        cop.save()
        # start_date_standard_format = convert_to_standard_date_format(cop.start_date)
        # end_date_standerd = convert_to_standard_date_format(cop.end_date)
        messages.info(request,'Updated success')
        return render(request, 'admin_edit_coupon.html', {'coupons': cop,'end_date':cop.end_date, 'start_date_standard_format': cop.start_date})

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def delete_coupon(request,pk):
    if 'email' in request.session:
        instance= coupon.objects.get(pk=pk)
        instance.soft_delete()
        return redirect(view_category)
    return redirect(user_login)


# coupon ----------------------------------

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def coupon_check(request):
    if 'email' in request.session:
        try:
            total = request.GET.get('total')
            if 'couponId' in request.GET:
                co = request.GET.get('couponId')
                coupon_obj = coupon.objects.get(id=co)
            elif 'coupon' in request.GET:
                co = request.GET.get('coupon')
                coupon_obj = coupon.objects.get(name=co)
            current_date = datetime.now().date()
            if coupon_obj.start_date > current_date:
                return JsonResponse({'error':'Coupon Has not started Yet'})
            elif coupon_obj.end_date < current_date:
                return JsonResponse({'error':'Coupon Expired'})
            elif coupon_obj.min_amount > float(total):
                return JsonResponse({'error':'Minimum amount should be'+str(coupon_obj.min_amount)})
            email = request.session['email']
            user = User.objects.get(email=email)
            orders = order.objects.filter(user=user, coupon=coupon_obj.id).exclude(payment_method='Pending') # checking if the user already used this coupon
            if orders.exists():
                return JsonResponse({'error':"You have redeemed the Coupon"})
            else:
                return JsonResponse({'Success':coupon_obj.id})
        except coupon.DoesNotExist:
            return JsonResponse({'error':'Invalid Coupon Code'})


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def confirmorder(request):
    if 'email' in request.session:
        print(request.method)
        current_date = datetime.now().date()
        couponDis = []
        couponId = 0
        dispercentage = 0
        total_amount = 0
        discount = 0
        total=0
        if request.method == 'POST':
            email = request.session['email']
            user = User.objects.get(email=email)
            addr = address.objects.get(user=user.id,default_value=True)
            alladdr = address.objects.all().filter(user=user.id)
            id = request.POST.get('id')
            ord = order.objects.get(id = id)
            cid = request.POST.get('cid')
            if cid:
                print(cid)
                couponDis = coupon.objects.get(id=cid)
                dispercentage = float(couponDis.discount)

            if ord.coupon:
                orders = order.objects.filter(user = user,coupon=ord.coupon).exclude(payment_method='Pending')
                if orders.exists():
                    pass
                else:
                    couponDis = coupon.objects.get(id=ord.coupon.id)
                    dispercentage = float(couponDis.discount)
                    
            allcoupon = coupon.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
        
            ord_items = order_items.objects.filter(order__id=ord.id)
            for item in ord_items:
                total_amount = total_amount+item.product.Offer_price * item.quantity
                discount = discount + item.product.Offer_price * item.quantity - item.product.price * item.quantity
                total = total + item.product.price * item.quantity
            print("dispercentage",dispercentage)
            temp = float(total_amount)
            if dispercentage > 0:
                dis_amount = round(float(total_amount) * (dispercentage / 100),2) # reducing the coupon based discount
                total_amount = round(float(total_amount) - dis_amount,2)
                discount = round(float(discount) - (temp-total_amount),2)
            print("coupobn",couponDis)
            #  return redirect(showcart)
            data = {'address':addr,'total':total,
                    'discount':discount,
                    'total_amount': total_amount,
                    'alladdress':alladdr,
                    'couponDetails':couponDis,
                    'allcoupon':allcoupon ,'checkingid':1,
                    'ord':ord
                    }

            return render(request,'user_confirmcart.html' ,data)

        else:
            print("Get method")
            print(request.GET)
            if 'val' in request.GET:
                couponId = request.GET.get('val')
            if couponId != 0:
                couponDis = coupon.objects.get(id=couponId)
                dispercentage = float(couponDis.discount)
            email = request.session['email']
            user = User.objects.get(email=email)
            cart_items = cart.objects.all().filter(user=user.id)
            addr = address.objects.get(user=user.id,default_value=True)
            alladdr = address.objects.all().filter(user=user.id)
            for item in cart_items:
                if item.product.varient.__getattribute__(item.size) > 0:
                    total_amount = total_amount+item.product.Offer_price * item.quantity
                    discount = discount + item.product.Offer_price * item.quantity - item.product.price * item.quantity
                    total = total + item.product.price * item.quantity
                else:
                    messages.info(request,'Product Not Available')
                    return redirect(showcart)
            print(discount)
            temp = float(total_amount)
            if 'val' in request.GET:
                dis_amount = round(float(total_amount) * (dispercentage / 100),2) # reducing the coupon based discount
                print("discount coupn",dis_amount)
                total_amount = round(float(total_amount) - dis_amount,2)
                discount = round(float(discount) - (temp-total_amount),2)
                print("discount",discount)
            allcoupon = coupon.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
            data = {'address':addr,'total':total,
                    'discount':discount,
                    'total_amount': total_amount,
                    'alladdress':alladdr,
                    'couponDetails':couponDis,
                    'allcoupon':allcoupon
                    }

            return render(request,'user_confirmcart.html' ,data)
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def orderhistory(request):
    if 'email' in request.session:
        email= request.session['email']
        user = User.objects.get(email=email)
        details = order.objects.filter(user=user.id).order_by('-id').exclude(Q(order_status='Cancelled') | Q(order_status='Returned') | Q(order_status ='Cancelled by Admin')).all()
        print(details)
        if details :
            none_details = True
        else:
            none_details = False

        return render(request,'user_orderhistory.html',{'none_details':none_details,'details':details})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def orderItems(request,pk):
    if 'email' in request.session:
        orderid = order.objects.get(id = pk)
        order_item = order_items.objects.all().filter(order=orderid).order_by('-order__id')
        return render(request,'user_order_item.html',{'orders':order_item,'details':orderid})
    return redirect(user_login)

# Download Invoice------------------------------------

def invoice_pdf(request,pk):

    product = products.objects.all()
    ord = order.objects.get(id = pk)
    ord_items = order_items.objects.filter(order__id = pk).order_by('-order__id')
    ord_items_with_index = [(index + 1, item) for index, item in enumerate(ord_items)]
    print(ord_items_with_index)
    template_path = 'user_invoice.html'

    context = {'ord':ord,'ord_items':ord_items,'ord_indx':ord_items_with_index}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

 #--Return a product-----------------------------------------

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def userreturnPage(request,pk):
    if 'email' in request.session:
        if request.method == 'POST':
            orders = order.objects.get(id = pk)
        
            if 'return' in request.POST:
                s = 1
            else:
                s = 2
       
            return render(request,'user_returnproductPpage.html',{'orders':orders,'s':s})
        return redirect(user_login)
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def returnOrder(request,pk):
    if 'email' in request.session:
        if request.method == 'POST':
            type = request.POST.get('type')
            user = User.objects.get(email = request.session['email'])
            ord = order.objects.get(id = pk)
            ordproduct = order_items.objects.filter(order__id = pk).all()
            print(ordproduct.count())
            returnOrder = return_order()
            #returnProduct = return_product()
            returnOrder.order = ord
            returnOrder.reason = request.POST.get('reason')
            returnOrder.user = user
            print(type)
            if type == '1':
                returnOrder.status = 'Returned'
                ord.order_status = 'Returned'                                                       
            else:
                returnOrder.status = 'Cancelled'
                ord.order_status = 'Cancelled'
            returnOrder.save() 
            ord.save()
            # returnOrderObj = return_order.objects.get(id = returnOrder.pk)

            # for items in ordproduct:
            #     return_product.objects.create(return_order=returnOrderObj, 
            #                                  order=ord,product=items.product, 
            #                                  size=items.size,
            #                                     quantity=items.quantity )
                # returnProduct.return_order = returnOrderObj
                # returnProduct.order = ord
                # returnProduct.product = items.product
                # returnProduct.size = items.size
                # returnProduct.quantity = items.quantity
                # returnProduct.save()

            return render(request,'user_afterReturnaOrder.html',{'type':type})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def admin_cancelOrder(request):
    if 'email' in request.session:
        print("ok")
        pk = request.POST.get('id') 
        
        ord = order.objects.get(id = pk)

        user = User.objects.get(email = ord.user)
        returnOrder = return_order()
        returnOrder.status = 'Cancelled by Admin'         
        returnOrder.order = ord
        returnOrder.reason = request.POST.get('reason')
        returnOrder.user = user
        returnOrder.save()
        ord.order_status = 'Cancelled by Admin'
        ord.save()
        # returnOrderObj = return_order.objects.get(id = returnOrder.pk)
        # for items in ordproduct:
        #     return_product.objects.create(return_order=returnOrderObj, 
        #                                         order=ord,product=items.product, 
        #                                         size=items.size,
        #                                             quantity=items.quantity )

        return JsonResponse({'success':'success'})

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def useraccount(request):
    if 'email' in request.session:
        email= request.session['email']
        user = User.objects.get(email=email)
        print("showing")
        print(user.id)
        return render(request,'user_personal.html',{'user':user})
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def show_returnpage(request):
    if 'email' in request.session:
        email= request.session['email']
        user = User.objects.get(email=email)
        details = order.objects.filter(user=user,order_status = 'Delivered').all()#exclude(Q(order_status='Cancelled') | Q(order_status='Returned')).all()
        if details:
            none_details = True
        else:
            none_details = False
        print(none_details)
        return render(request,'user_selectReturn.html',{'details':details,'none_details':none_details})
    return redirect(user_login)
    
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def editreturnpage(request):
    if 'email' in request.session:
        order_id = request.POST.get('prod')
        reason = request.POST.get('reason')
        order_details = order.objects.get(id=order_id)
        returns = return_order()
        returns.order = order_details
        returns.reason = reason
        returns.save()
        return redirect(personal_data)
    return redirect(user_login)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def showCancelledOrders(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        corder = order.objects.filter( Q(user=user) & (Q(order_status='Cancelled') | Q(order_status='Cancelled by Admin'))).order_by('-id')
        print(corder)
        return render(request,'user_return_cancelled.html',{'cancelled':corder})
    


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def showReturnedOrders(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        corder = order.objects.filter( Q(user=user) & Q(order_status='Returned')).order_by('-id')
        print(corder)
        return render(request,'user_returnlist1_page.html',{'cancelled':corder})



# User Wallet-----------------------------------------
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def show_wallet(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        returedOrder = return_order.objects.filter(user = user.id).all()
        total_returned_amount = returedOrder.aggregate(total_amount=Sum('order__total_amount'))
        print(total_returned_amount)
        print(returedOrder)
        return render(request,'user_wallet.html',{'total':total_returned_amount['total_amount']})


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login') 
def wallet_transaction(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        returedOrder = return_order.objects.filter(user = user.id).all()
        total_returned_amount = returedOrder.aggregate(total_amount=Sum('order__total_amount'))
        print(total_returned_amount)
        print(returedOrder)
        return render(request,'user_wallet_transaction.html',{'order':returedOrder,'total':total_returned_amount['total_amount']})
    
# sales Report-----------------------------
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def downloading_page(request):
    
    if 'email' in request.session:
        return render(request,'admin_sales_report.html')


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def generate_pdf(request):
    if 'email' in request.session:
        # Query data from your databasew
        today = datetime.now().date()
        if request.POST.get('period') == 'oneday':
            start_date = today - timedelta(days=1)
            end_date = today
        elif request.POST.get('period') == 'weekly':
            start_date = today - timedelta(weeks=1)
            end_date = today
        elif request.POST.get('period') == 'lmonth':
            start_date = today.replace(day=1)
            print(start_date)
            end_date = today
        elif request.POST.get('period') == 'pmonth':
            start_date =(today.replace(day=1) - timedelta(days=1)).replace(day=1)
            print(start_date)
            end_date = today.replace(day=1)- timedelta(days=1)
            print(end_date)
        elif request.POST.get('period') == '6month':
            start_date = today - timedelta(days=180)
            end_date = today
        elif request.POST.get('period') == 'year':
            start_date = today - relativedelta(years=1)
            end_date = today

     
        # Filter data from your database based on the date range
        if request.POST.get('details') == 'order':
            queryset = order.objects.filter(date__range=[start_date, end_date]).order_by('-id')
            print(queryset)
            if 'pdf' in request.POST:
                data = [['Order ID', 'Customer ID', 'Customer Email', 'Total Amount','Payment Method','Date']]
            else:
                data = ['Order ID', 'Customer ID', 'Customer Email', 'Total Amount','Payment Method','Date']
          
            
        else:
            queryset =  order_items.objects.filter(order__date__range=[start_date, end_date]).order_by('-order_id')
            print(queryset)
            if 'pdf' in request.POST:
                 data = [['Order ID', 'Customer Email', 'Product ID','Size','Quantity','Total Amount','Date']]
            else:
                data = ['Order ID', 'Customer Email', 'Product','Size','Quantity','Total Amount','Date']
          
     
       
        if 'pdf' in request.POST:
            # Populate table data with database records
            if request.POST.get('details') == 'order':
                for item in queryset:
                    data.append([item.id, item.user.id,item.user.email, item.total_amount,item.payment_method,item.date])  # Add data from each database record
            else:
                for item in queryset:
                    data.append([item.id, item.order.user.email,item.product.id, item.size,item.quantity,item.total,item.order.date])  # Add data from each database record
          

            # Create a PDF document
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_Report.pdf"'

            # Create a PDF document
            doc = SimpleDocTemplate(response, pagesize=letter)

            # Create a table and specify style
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), (0.9, 0.9, 0.9)),  # Header row background color
                ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),         # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),             # Alignment of content
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),          # Border around cells
            ]))

            # Add table to the PDF document
            doc.build([table])

            return response
        else:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            # Write headers
            #headers = ['Order ID', 'Customer', 'Total Amount', 'Date']
            for col, header in enumerate(data):
                worksheet.write(0, col, header)

            # Write data
            if request.POST.get('details') == 'order':
                row = 1
                for item in queryset:
                    worksheet.write(row, 0, item.id)
                    worksheet.write(row, 1, item.user.id)
                    worksheet.write(row, 2, item.user.email)
                    worksheet.write(row, 3, item.total_amount)
                    worksheet.write(row, 4, item.payment_method)
                    worksheet.write(row, 5, item.date.strftime('%Y-%m-%d %H:%M:%S'))  # Format date as needed
                    row += 1
            else:
                row = 1
                for item in queryset:
                    worksheet.write(row, 0, item.order.id)
                    worksheet.write(row, 1, item.order.user.email)
                    worksheet.write(row, 2, item.product.name)
                    worksheet.write(row, 3, item.size)
                    worksheet.write(row, 4, item.quantity)
                    worksheet.write(row, 5, item.total)
                    worksheet.write(row, 6, item.order.date.strftime('%Y-%m-%d %H:%M:%S'))  # Format date as needed
                    row += 1

            workbook.close()

            # Set response headers to force file download
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="sales_Report.xlsx"'
            output.seek(0)
            response.write(output.read())
            return response


import io
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def generate_excel(request):
    if 'email' in request.session:
        today = datetime.now().date()

        # Determine start and end dates based on selected period
        if request.POST.get('period') == 'oneday':
            start_date = today - timedelta(days=1)
            end_date = today
        elif request.POST.get('period') == 'weekly':
            start_date = today - timedelta(weeks=1)
            end_date = today
        elif request.POST.get('period') == 'month':
            start_date = today.replace(day=1)
            end_date = today
        else:
            start_date = today - timedelta(days=180)
            end_date = today

        # Filter orders based on the date range
        queryset = order.objects.filter(date__range=[start_date, end_date])

        # Create an in-memory Excel file
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Write headers
        headers = ['Order ID', 'Customer', 'Total Amount', 'Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write data
        row = 1
        for item in queryset:
            worksheet.write(row, 0, item.id)
            worksheet.write(row, 1, item.user.first_name)
            worksheet.write(row, 2, item.total_amount)
            worksheet.write(row, 3, item.date.strftime('%Y-%m-%d'))  # Format date as needed
            row += 1

        workbook.close()

        # Set response headers to force file download
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sales_Report.xlsx"'
        output.seek(0)
        response.write(output.read())
        return response
    else:
        # Handle case where user is not logged in or session does not exist
        return HttpResponse("Unauthorized", status=401)

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def listSales(request):
    if 'email' in request.session:
        today = datetime.now().date()
        print(request.GET.get('period'))
        print(request.GET.get('details'))
        
        if request.GET.get('period') == 'oneday':
            start_date = today - timedelta(days=1)
            end_date = today
        elif request.GET.get('period') == 'weekly':
            start_date = today - timedelta(weeks=1)
            end_date = today
        elif request.GET.get('period') == 'lmonth':
            start_date = today.replace(day=1)
            print(start_date)
            end_date = today
        elif request.GET.get('period') == 'pmonth':
            start_date =(today.replace(day=1) - timedelta(days=1)).replace(day=1)
            print(start_date)
            end_date = today.replace(day=1)- timedelta(days=1)
            print(end_date)
        elif request.GET.get('period') == '6month':
            start_date = today - timedelta(days=180)
            end_date = today
        elif request.GET.get('period') == 'year':
            start_date = today - relativedelta(years=1)
            end_date = today
        
        ord = order.objects.filter(date__range=[start_date, end_date]).order_by('-id')
        orddtl = order_items.objects.filter(order__date__range=[start_date, end_date]).order_by('-order_id')
        if request.GET.get('details') == 'order':
            details= ord
            type = 1
            
        else:
            details = orddtl
            type = 2
        return render(request, 'list_sales.html', {'dd':details,'type':type}) 



# admin manage returns.................................................
@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login') 
def show_return(request):
    if 'email' in request.session:
        orders = return_order.objects.all().order_by('-order__id')
        return render(request,'admin_managereturn.html',{'details':orders})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def show_returnProduct(request,pk):
    if 'email' in request.session:
        print(pk)
        orders = order_items.objects.filter(order__id = pk).order_by('-id').all()
        ord = return_order.objects.get(order__id = pk)
        return render(request,'admin_managereturn_products.html',{'details':orders,'id':pk,'stock_status':ord.stock_status})
    return redirect(user_login)


@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def addtostock(request,pk):
  
    returnOrder = return_order.objects.get(order__id=pk)
    orderItems = order_items.objects.filter(order__id = returnOrder.order.id)
    for items in orderItems:      
        product = products.objects.get(id = items.product.id)
        current_value = getattr(product.varient, items.size)
        new_value = current_value + items.quantity
        setattr(product.varient, items.size, new_value)
        product.save()
     
    returnOrder.stock_status = True
    returnOrder.save()
    #Increment the current value

    # Set the updated value to the attribute dynamically
    # var.stock_status = True
    # var.save()
    return redirect('show_returnProduct',pk)

@cache_control(no_cashe=True,must_revalidate=True,no_store=True)
@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='user_login')
def admin_orderCancelPage(request,pk):
    ord = order.objects.get(id = pk)
    return render(request,'admin_cancel_order.html',{'order':ord})



#testing----------------------------------------------------------------------------



def insert_img(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            descrip = "Hello"
            image = request.FILES['image']
            instance = testimage(titile=name,description=descrip,image=image)
            instance.save()
            details = testimage.objects.all()
            return render(request,'test1.html',{'details':details})

def submit(request,pk):
    print(pk)
    details = testimage.objects.all().filter(pk=pk)
    return render(request,'test1.html',{'details':details})
    
def test(request):
    print("test data")
    return render(request,'crop.html')

def upload_and_crop(request):

    imgobj = CroppedImage()
    name = request.POST.get('ss')

    # print("test9ing",name)
    # print("THISHS",name)
    # #fd_data_str = request.POST.get('fd_data')
    # image_file = request.FILES['file']
    # print(image_file)
    # imgobj.file = request.FILES['file']
    # imgobj.name = name
    # imgobj.save()
        
    # if fd_data_str:
    #         # Convert the FormData string back to FormData format
    #     import json
    #     fd_data = json.loads(fd_data_str)
            
    #         # Process the FormData object as needed
    #         # For example, save the file to the server
    #     image_file = fd_data['file']


    #     print(fd_data['file'])
        
    # if image_file:
    #         # Create an instance of the Product model
    #     print(request.FILES.get('file'))
    #form = ImageUploadForm(request.POST or None, request.FILES or None)
    # if request.FILES['file']:
    #     print( request.FILES['file'])
    # #else:
    #     
    #instance.image = request.FILES['image']
    # if form.is_valid():
    #     form.save()
    return JsonResponse({'message': 'works'})
    # context = {'form': form}
    return redirect(test)


def testttting(request):
    id = request.GET.get('id')
    print("thishs",id)
    return redirect(confirmorder)