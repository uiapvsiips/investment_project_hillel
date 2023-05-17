from rest_framework import serializers

from users.calculates import earn_money_for_referrals
from .models import *


class ContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = ['name']


class UserContractsSerializer(serializers.ModelSerializer):
    contract = ContractsSerializer()

    class Meta:
        model = UserContracts
        fields = ['contract', 'current_profit', 'days_from_start', 'complete_percent', 'deposit_amount',
                  'creation_date']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['registration_uuid', 'account_balance', 'showing_contracts']



class CheckNewContractSerializer(serializers.ModelSerializer):
    selected_contract_id = serializers.IntegerField(write_only=True)
    offered_rate = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    contract = ContractsSerializer(read_only=True)

    class Meta:
        model = UserContracts
        fields = ['contract', 'current_profit', 'days_from_start', 'complete_percent', 'deposit_amount',
                  'creation_date', 'selected_contract_id', 'offered_rate', 'user_id']

    def validate(self, attrs):
        selected_contract_id = attrs.get('selected_contract_id')
        offered_rate = attrs.get('offered_rate')
        user_id = attrs.get('user_id')
        # Проверяем, что выбранный контракт существует и пользователь может его подключить ("видит" данный контракт)
        try:
            selected_contract = Contracts.objects.get(id=selected_contract_id)
            if not [showing_contract for showing_contract in
                    User.objects.get(id=user_id).userprofile.showing_contracts.values('id') if
                    showing_contract['id'] == selected_contract_id]:
                raise Contracts.DoesNotExist
        except Contracts.DoesNotExist:
            raise serializers.ValidationError('Выбранный контракт не существует')

        # Проверяем, что offered_rate является целым числом
        if not isinstance(offered_rate, int):
            raise serializers.ValidationError('Значение offered_rate должно быть целым числом')

        # Проверяем достаточность средств на счету пользователя
        user_balance = User.objects.get(id=user_id).userprofile.account_balance
        if user_balance < selected_contract.min_money:
            raise serializers.ValidationError('Недостаточно средств на счету для открытия контракта')
        elif offered_rate > selected_contract.max_money:
            raise serializers.ValidationError('Предложенная ставка слишком высока для открытия контракта')
        elif offered_rate < selected_contract.min_money:
            raise serializers.ValidationError('Предложенная ставка слишком низкая для открытия контракта')

        return attrs

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        # Создается новый контракт
        new_contract = UserContracts(deposit_amount=validated_data['offered_rate'],
                                     contract=Contracts.objects.get(
                                         id=validated_data['selected_contract_id']),
                                     user_id=validated_data['user_id'])
        new_contract.save()
        # Списание денег с баланса пользователя
        user.userprofile.account_balance -= validated_data['offered_rate']
        user.userprofile.save()

        # Начисление денег по реферальной программе
        earn_money_for_referrals(validated_data['user_id'], validated_data['offered_rate'])
        return new_contract

class ShortUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class NewWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallets
        fields = '__all__'

        def validate(self, attrs):
            type = attrs.get('type')
            wallet_number = attrs('wallet_number')

            if not isinstance(int, type):
                raise serializers.ValidationError('Значение type должно быть целым числом')

        def create(self, validated_data):
            new_wallet = Wallets.objects.create(type=validated_data['type'],
                                                wallet_number=validated_data['wallet_number'])
            return new_wallet


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    wallets = NewWalletSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'userprofile', 'wallets']
