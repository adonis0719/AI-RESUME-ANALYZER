from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resumes.views import home
from resumes.views import upload_resume
from jobs.views import upload_job
from matching.views import compare
from accounts.views import register, user_login, user_logout
from accounts.views import register_api


from resumes.views import resume_list_api
from jobs.views import job_list_api
from matching.views import compare_api

from resumes.views import delete_resume_api
from jobs.views import delete_job_api

from recruiter.views import bulk_analyze

from accounts.views import send_otp, verify_otp

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('upload/', upload_resume, name='upload'),
    path('job/', upload_job, name='upload_job'),
    path('compare/', compare, name='compare'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('api/resumes/', resume_list_api),
    path('api/resumes/<int:resume_id>/', delete_resume_api),
    path('api/jobs/', job_list_api),
    path('api/jobs/<int:job_id>/', delete_job_api),
    path('api/compare/', compare_api),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_api),
    path('api/recruiter/analyze/', bulk_analyze),
    path('api/send-otp/', send_otp),
    path('api/verify-otp/', verify_otp),
]
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)