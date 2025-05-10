import logging
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def user_list(request):
    """
    Handle GET and POST requests for users.
    - GET supports pagination, name filtering, and sorting.
    - POST allows creating a new user.
    """
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
        name = request.GET.get('name', '')
        sort = request.GET.get('sort', '')

        logger.info("Fetching user list: page=%s, limit=%s, name=%s, sort=%s", page, limit, name, sort)

        # Initial queryset
        users = User.objects.only(
            "id", "first_name", "last_name", "company_name", "age",
            "city", "state", "zip", "email", "web"
        )

        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
            logger.debug("Filtered by name: %s", name)

        if sort:
            users = users.order_by(sort)
            logger.debug("Sorted by: %s", sort)

        start = (page - 1) * limit
        end = start + limit
        paginated_users = users[start:end]

        serializer = UserSerializer(paginated_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        logger.info("Creating new user")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User created successfully: %s", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("User creation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Handle GET, PUT, DELETE operations on a specific user by ID (pk).
    """
    try:
        user = User.objects.get(pk=pk)
        logger.debug("User fetched: ID=%s", pk)
    except User.DoesNotExist:
        logger.error("User not found: ID=%s", pk)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("User updated: ID=%s", pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("Failed to update user: ID=%s, Errors=%s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        logger.info("User deleted: ID=%s", pk)
        return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)
