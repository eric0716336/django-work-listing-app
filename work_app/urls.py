
from django.contrib import admin
from django.urls import path,include
from work_app.views import home , login , signup  , signout ,job_add,confirm_add,email_job,email_send,delete_job,show_profile,update_profile
from django.contrib.auth import views as auth_views

from work_app.views import password_reset_request

urlpatterns = [
   path('' , home , name='home' ), 
   path('login/' ,login  , name='login'), 
   path('logout/' , signout ), 
   path('signup/' , signup ), 
   path('add_job/', job_add),
   path('confirm_add/', confirm_add),
   path('email/<int:id>', email_job),
   path('email-sent/<int:id>', email_send),
   path('delete-job/<int:id>' , delete_job ), 
   path('show-profile/', show_profile, name='profile'),
   path('update-profile/', update_profile),

   path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
   
   path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
   name='password_reset_done'),

   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   
]
