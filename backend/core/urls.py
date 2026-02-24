from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resumes.views import home
from resumes.views import upload_resume
from jobs.views import upload_job
from matching.views import compare

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('upload/', upload_resume, name='upload'),
    path('job/', upload_job, name='upload_job'),
    path('compare/', compare, name='compare'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)