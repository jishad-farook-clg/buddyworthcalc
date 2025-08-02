from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import tempfile
import cv2
import mediapipe as mp
import random
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


def get_random_description(organ):
    descriptions = {
        "heart": ["CYBER-ENHANCED", "ORGANIC v2.3", "BLOOD PUMP 9000"],
        "kidney": ["FILTER SYSTEM v4.2", "BIOLOGICAL FILTER", "TOXIN PROCESSOR"],
        "liver": ["ALCOHOL PROCESSOR", "CHEMICAL LAB v3.1"],
        "eyes": ["OPTIC SCANNERS", "NEURAL LINKED", "ZOOM v2.0"]
    }
    return random.choice(descriptions.get(organ, ["STANDARD MODEL"]))



def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Save uploaded image temporarily
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
            filename = fs.save(request.FILES['image'].name, request.FILES['image'])
            file_path = fs.path(filename)
            
            # Resize image if too large (using OpenCV)
            img = cv2.imread(file_path)
            if img is None:
                return render(request, 'calculator/index.html', {
                    'error': 'Invalid image file'
                })
                
            # Resize to max 1000px width while maintaining aspect ratio
            height, width = img.shape[:2]
            if width > 1000:
                new_width = 1000
                new_height = int((new_width/width) * height)
                img = cv2.resize(img, (new_width, new_height))
            
            # Process image (your existing detection logic)
            body_parts = ["heart", "kidney", "liver"]  # Replace with actual detection
            prices = {
                part: f"₹{random.randint(1, 50)} lakh" 
                for part in random.sample(body_parts, k=2)
            }
            
            # Clean up temp file
            fs.delete(filename)
            
            return render(request, 'calculator/index.html', {
                'prices': prices,
                'uploaded_image': fs.url(filename)  # For displaying uploaded image
            })
            
        except Exception as e:
            return render(request, 'calculator/index.html', {
                'error': f"Error processing image: {str(e)}"
            })
    
    return render(request, 'calculator/index.html')
@api_view(['POST'])
def calculate_price(request):
    # Check if image exists in request
    if 'image' not in request.FILES:
        return Response(
            {"error": "No image uploaded. Send a file with key 'image'"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        image_file = request.FILES['image']
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_file.read())
            image_path = tmp.name

        # Process image (example with MediaPipe)
        mp_pose = mp.solutions.pose
        with mp_pose.Pose() as pose:
            image = cv2.imread(image_path)
            if image is None:
                return Response(
                    {"error": "Invalid image file"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Generate fake prices based on detection
            body_parts = []
            if results.pose_landmarks:
                body_parts = ["head", "shoulders", "knees", "toes"]  # Simplified
            
            prices = {
                part: f"₹{random.randint(1, 50)} lakh" 
                for part in body_parts
            }
            
            return Response({"prices": prices})
            
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )