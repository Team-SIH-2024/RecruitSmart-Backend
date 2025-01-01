from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JobPost,Question,SelectedUser
import json


from .models import Admin

import uuid
import io

import csv
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JobPost, Question



@csrf_exempt
def upload_selected_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            discipline = data.get("discipline")
            area_of_expertise = data.get("area_of_expertise")

            if not all([name, discipline, area_of_expertise]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            selected_user = SelectedUser.objects.create(
                name=name,
                discipline=discipline,
                area_of_expertise=area_of_expertise,
            )
            return JsonResponse({"message": "User uploaded successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def create_job_post(request):
    if request.method == 'POST':
        try:
            # Get the data from the form
            title = request.POST.get('title')
            description = request.POST.get('description')

            # Ensure title and description are provided
            if not title or not description:
                return JsonResponse({'error': 'Title and description are required.'}, status=400)

            # Create the JobPost instance
            job_post_command_id = str(uuid.uuid4())  # Generate unique ID (UUID)

            # Create the JobPost instance
            job_post = JobPost.objects.create(
                title=title,
                description=description,
                command_id=job_post_command_id,
            )

            # Return a success response
            return JsonResponse({'message': 'Job post created successfully!', 'job_post_id': job_post.id}, status=200)

        except Exception as e:
            # Catch any exception and return an error response
            return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
def list_job_posts(request):
    if request.method == "GET":
        job_posts = JobPost.objects.all().values("id", "title", "description", "created_at")
        return JsonResponse(list(job_posts), safe=False)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import JobPost



@csrf_exempt
def delete_job_post(request, job_id):
    if request.method == "DELETE":
        try:
            job_post = JobPost.objects.get(id=job_id)
            job_post.delete()
            return JsonResponse({"message": "Job post deleted successfully!"})
        except JobPost.DoesNotExist:
            return JsonResponse({"error": "Job post not found!"}, status=404)








@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Validate input
            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            # Authenticate admin
            try:
                admin_user = Admin.objects.get(email=email)
                if admin_user.password != password:  # Use a secure hash function in production
                    return JsonResponse({"error": "Invalid email or password."}, status=401)
            except Admin.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password."}, status=401)

            # Login successful
            return JsonResponse({"message": "Admin login successful!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
