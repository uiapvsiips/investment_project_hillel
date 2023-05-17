from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import *


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_contracts(request):
    if request.method == 'GET':
        serializer = UserContractsSerializer(request.user.usercontracts_set.all(), many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_short_info(request):
    if request.method == 'GET':
        serializer = ShortUserInfoSerializer(request.user)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_info(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_new_contract(request):
    if request.method == 'POST':
        data = {'selected_contract_id': request.POST.get('selected_contract'),
                'offered_rate': request.POST.get('offered_rate'),
                'user_id': request.user.id}
        serializer = CheckNewContractSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_add_wallet(request):
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'type': request.POST.get('type'),
            'wallet_number': request.POST.get('wallet_number'),
        }
        serializer = NewWalletSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
