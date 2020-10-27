from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from user_management.views import register, register_vendor, account_profile_view, close_account, \
    ban_user_view, unban_user_view, get_orders_view
from django.contrib.auth import views as auth_views
from user_management.views import logout_view

app_name = "user_management"

urlpatterns = [
    # registration
    path('register/', register, name='register'),
    path('register/vendor', register_vendor, name='register_vendor'),

    # login/logout
    path('logout/', logout_view, name='logout'),
    path('login/', LoginView.as_view(success_url=reverse_lazy('home'),
                                     template_name='login.html'), name='login'),

    # password_management
    path('changepassword/',
         PasswordChangeView.as_view(success_url=reverse_lazy('user_management:change_password_success'),
                                    template_name='change_password.html'),
         name='change_password'),
    path('changepassword/success', PasswordChangeDoneView.as_view(template_name='change_password_success.html'),
         name='change_password_success'),

    path('resetpassword/', PasswordResetView.as_view(success_url=reverse_lazy('user_management:reset_password_done'),
                                                     template_name='reset_password_form_user.html',
                                                     email_template_name='reset_password_email_user.html'),
         name='reset_password'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_done_user.html'),
         name='reset_password_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('user_management:reset_password_success'),
        template_name='reset_password_confirm_user.html'),
         name='reset_password_confirm'),
    path('reset/success/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete_user.html'),
         name='reset_password_success'),

    # close_account
    path('close_account/', close_account, name='close_account'),

    # profile
    path('profile/', account_profile_view, name='profile'),

    # ban/unban
    path('ban_user/', ban_user_view, name='ban_user'),
    path('unban_user/', unban_user_view, name='unban_user'),
    path('get_user_order', get_orders_view, name='get_orders'),
]
