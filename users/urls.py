from django.urls import include, path


from users.views import login, logout, registration, verify_email, password_reset, password_reset_confirm, profile

app_name = 'users'


urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
    path("verify_email/<uidb64>/<token>/", verify_email, name="verify_email"),
    path("password-reset/", password_reset, name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm, name="password-reset-confirm"),
]