from django.shortcuts import render

# Create your views here.
from . models import *
from . serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#for login <start>
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer

    
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')  # Admin username or Customer phone
    password = request.data.get('password')  # Password for both
    is_admin = request.data.get('is_admin', False)  # Admin flag from request

    if is_admin:
        # Admin login
        user = authenticate(username=username, password=password)
        if user and user.is_staff:  # Check if the user is an admin
            refresh = RefreshToken.for_user(user)  # Generate JWT token
            return JsonResponse({
                "message": "Admin login successful",
                "redirect": "/admin",
                "token": str(refresh.access_token),
            }, status=200)
        else:
            return JsonResponse({"error": "Invalid admin credentials Toka apa!"}, status=401)

    else:
        # Normal user login
        try:
            customer = Customer.objects.get(phone=username)  # Assume 'username' is the phone
            if customer.password == password:  # Replace with a hashed password check in production
                refresh = RefreshToken.for_user(customer)  # Generate JWT token
                return JsonResponse({
                    "message": "User login successful",
                    "redirect": "/home",
                    "token": str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid user credentials"}, status=401)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Invalid user credentials Toka apa!"}, status=401)

#for login <end>



@permission_classes([IsAuthenticated])
def generic_api(model_class, serializer_class):
    @api_view(['GET', 'POST', 'DELETE', 'PUT'])
    def api(request, id=None):
        if request.method == 'GET':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            else:
                instance = model_class.objects.all()
                serializer = serializer_class(instance, many=True)
                return Response(serializer.data)
        
        elif request.method == 'POST':
            # If it is an Order, handle customer and food_items
            if model_class == Order:
                customer = request.user  # Assuming customer is the authenticated user
                food_items = request.data.get('food_items')
                total_price = request.data.get('total_price')

                # Create the order
                order = Order.objects.create(customer=customer, total_price=total_price)
                food_items_obj = FoodItem.objects.filter(id__in=food_items)
                order.food_items.set(food_items_obj)
                order.save()

                return Response({'message': 'Order created successfully', 'order_id': order.id}, status=201)
            
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        elif request.method == 'PUT':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)

        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'message': 'Deleted successfully'}, status=204)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)

    return api
from rest_framework.response import Response
from .models import Customer, FoodItem, Order
from rest_framework.decorators import api_view

@api_view(['POST'])
def confirm_order(request):
    try:
        name = request.data.get('customer_name')
        phone = request.data.get('phone')
        food_items = request.data.get('food_items')
        total_price = request.data.get('total_price')

        if not (name and phone and food_items and total_price):
            return Response({'message': 'Missing required fields'}, status=400)

        # Validate customer by phone
        try:
            customer = Customer.objects.get(phone=phone)
            if customer.name != name:
                return Response({'message': 'Name does not match the phone number.'}, status=401)
        except Customer.DoesNotExist:
            return Response({'message': 'Invalid phone number.'}, status=401)

        # Validate food items
        food_items_objs = FoodItem.objects.filter(id__in=food_items)
        if not food_items_objs.exists():
            return Response({'message': 'Invalid food item IDs.'}, status=400)

        # Create the order
        order = Order.objects.create(customer=customer, total_price=total_price)
        order.food_items.set(food_items_objs)
        order.save()

        return Response({'message': 'Order successfully placed!', 'order_id': order.id}, status=201)
    except Exception as e:
        print(f"Error confirming order: {e}")
        return Response({'message': 'An unexpected error occurred'}, status=500)


manage_foodItem= generic_api(FoodItem, FoodItemserializers)
manage_customer= generic_api(Customer, Customerserializers)
manage_order= generic_api(Order, Orderserializers)        


