from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from admin_dashboard.models import JobPost,Question
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# expert_dashboard/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import json

@csrf_exempt
def upload_job_post_csv(request, job_post_id):
    if request.method == 'POST':
        try:
            job_post = JobPost.objects.get(id=job_post_id)
            questions_csv = request.FILES.get('questions_csv')

            if not questions_csv:
                return JsonResponse({'error': 'No CSV file uploaded.'}, status=400)

            # Process the CSV file
            csv_data = questions_csv.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_data)

            # Save each question to the database
            for row in csv_reader:
                # Ensure the row has all necessary keys
                if not all(key in row for key in ['question', 'answer', 'difficulty', 'keywords']):
                    return JsonResponse({'error': 'Invalid CSV format. Missing required fields.'}, status=400)

                # Save the question to the database
                Question.objects.create(
                    job_post=job_post,
                    command_id=job_post.command_id,
                    question=row['question'],
                    answer=row.get('answer', None),  # Nullable field
                    difficulty=row['difficulty'],
                    keywords=json.loads(row['keywords'])  # Convert JSON string to dictionary
                )

            return JsonResponse({'message': 'CSV uploaded successfully!'}, status=200)

        except JobPost.DoesNotExist:
            return JsonResponse({'error': 'Job post not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
