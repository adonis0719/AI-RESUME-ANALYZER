from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from resumes.models import Resume
from jobs.models import JobDescription


def is_admin(user):
    return user.is_staff


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    users = User.objects.all()

    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_staff": u.is_staff,
            "date_joined": u.date_joined
        })

    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user(request, user_id):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_resumes(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    resumes = Resume.objects.select_related('user').all()

    data = []
    for r in resumes:
        user_display = r.user.username if r.user else None
        email_display = r.candidate_email or (r.user.email if r.user else None)
        data.append({
            "id": r.id,
            "title": r.title,
            "user": user_display,
            "candidate_email": email_display,
            "uploaded_at": r.uploaded_at
        })

    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_resume(request, resume_id):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        resume = Resume.objects.get(id=resume_id)
        resume.delete()
        return Response({"message": "Resume deleted"})
    except Resume.DoesNotExist:
        return Response({"error": "Resume not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_jobs(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    jobs = JobDescription.objects.select_related('user').all()

    data = []
    for j in jobs:
        data.append({
            "id": j.id,
            "title": j.title,
            "user": j.user.username if j.user else None,
            "created_at": j.created_at
        })

    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_job(request, job_id):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        job = JobDescription.objects.get(id=job_id)
        job.delete()
        return Response({"message": "Job deleted"})
    except JobDescription.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)