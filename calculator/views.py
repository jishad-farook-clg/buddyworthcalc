from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

@api_view(['POST'])
def calculate_price(request):
    # For now, return random prices (add image processing later)
    prices = {
        "heart": f"₹{random.randint(5, 20)} lakh",
        "kidney": f"₹{random.randint(10, 50)} lakh",
        "liver": "Free (used condition)",
    }
    return Response({"prices": prices})