from django.shortcuts import render, redirect
from .models import UserPersonalDetails, UserQualificationDetails, UserProfessionalDetails
from .tasks import generate_resume
from django.http import JsonResponse
from celery.result import AsyncResult

def get_resume_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS':
        result = task.result  # This is the generated resume text
        return JsonResponse({'status': 'SUCCESS', 'resume': result})
    elif task.state == 'FAILURE':
        return JsonResponse({'status': 'FAILURE'})
    else:
        return JsonResponse({'status': task.state})


def user_form(request):
    if request.method == 'POST':
        # Save Personal Details
        user = UserPersonalDetails.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address']
        )

        # Save Qualification Details
        UserQualificationDetails.objects.create(
            user=user,
            degree=request.POST['degree'],
            university=request.POST['university'],
            year_of_passing=request.POST['year_of_passing']
        )

        # Save Professional Details
        UserProfessionalDetails.objects.create(
            user=user,
            company=request.POST['company'],
            designation=request.POST['designation'],
            experience=request.POST['experience']
        )

        # Send to Celery for processing
        user_data = f"Name: {user.name}, Email: {user.email}, Degree: {request.POST['degree']}"
        # generate_resume.delay(user_data)
        task=generate_resume.apply_async(
            args=[user_data],
            countdown=10,   # Start after 10 seconds
            expires=3600    # Task expires after 1 hour
        )
        
        return JsonResponse({'task_id': task.id})

    return render(request, 'user_form.html')