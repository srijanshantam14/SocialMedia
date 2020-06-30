
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Connect.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login1, name='login'),
    path('in/<str:Username>/', UserProfile1,name="UserProfile"),
    path('Register/', register, name='Register'),
    path('logout/',logout1 , name='logout'),
    path('in/Edit/<str:Username>/', Update_User_Details,name="UpdateUserProfile"),
    path('all_professionals/<str:what>', All_Profession, name='professional'),
    path('connection/<str:action>/<int:u_id>/', Manage_your_connections,name="connections"),
    path('all_professional_html/<str:what>/', All_professional_Html, name='professional_html'),
    path('add_company/', Add_Company, name='addCompany'),
    path('company_details/', CompanyDetails, name='Companydetails'),
    path('post_new_blog/', NewPost, name='post'),
path('likes/<int:b_id>/<str:Username>/',  Like_By_Me,name="likes"),
path('donate_amount/<str:u_id>', SendPaymentRequest, name='donate'),
path('paycheck/', PaymentCheck, name='paycheck'),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
