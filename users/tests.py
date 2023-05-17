import datetime

from django.test import TestCase

from .calculates import *
from .models import UserContracts
from contracts.models import Contracts


class calc_tests(TestCase):
    def setUp(self):
        # Создаем пользователей для тестирования
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')
        self.user4 = User.objects.create_user(username='user4', password='password4')

        self.user2.userprofile.referred_by = self.user1.userprofile
        self.user2.save()
        self.user3.userprofile.referred_by = self.user2.userprofile
        self.user3.save()
        self.user4.userprofile.referred_by = self.user3.userprofile
        self.user4.save()

        # Создаем контракты для тестирования
        self.contract1 = Contracts.objects.create(name='Contract1', en_name='Contract1', min_money=100, max_money=1000,
                                                  percent_for_day=0.01, term=365, show_to_all=True)
        self.contract2 = Contracts.objects.create(name='Contract2', en_name='Contract2', min_money=500, max_money=2000,
                                                  percent_for_day=0.02, term=365, show_to_all=True)

        self.user_contract1 = UserContracts.objects.create(user=self.user1, contract=self.contract1, status=0,
                                                           deposit_amount=100)
        self.user_contract2 = UserContracts.objects.create(user=self.user2, contract=self.contract2, status=0,
                                                           deposit_amount=200)
        self.user_contract3 = UserContracts.objects.create(user=self.user3, contract=self.contract2, status=0,
                                                           deposit_amount=300)
        self.user_contract4 = UserContracts.objects.create(user=self.user4, contract=self.contract1, status=0,
                                                           deposit_amount=400)

    def test_earn_money_for_referrals(self):
        # Вызываем функцию earn_money_for_referrals для пользователя user4 с предложенной ставкой 100
        earn_money_for_referrals(self.user4.id, 100)

        # Проверяем, что начисления выполнились правильно
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.userprofile.account_balance, 100 * 0.015)

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.userprofile.account_balance, 100 * 0.03)

        self.user3.refresh_from_db()
        self.assertEqual(self.user3.userprofile.account_balance, 100 * 0.05)

        self.user4.refresh_from_db()
        self.assertEqual(self.user4.userprofile.account_balance, 0)

    def test_calc_balance(self):
        # Задаем условия для выполнения теста
        self.user_contract1.creation_date = datetime.datetime(2022,5,10)
        self.user_contract1.contract.term = 365
        self.user_contract1.status = 0
        self.user_contract1.paid_money = 0
        self.user_contract1.save()

        self.user_contract2.paid_money = 0
        self.user_contract2.save()

        # Вызываем функцию calc_balance
        calc_balance()

        # Проверяем, что балансы и статусы контрактов обновились правильно
        self.user_contract1.refresh_from_db()
        self.assertEqual(self.user_contract1.status, 1)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.userprofile.account_balance, 100 + 3.65)

        self.user_contract3.refresh_from_db()
        self.assertEqual(self.user_contract3.status, 0)
        self.user3.refresh_from_db()
        self.assertEqual(self.user3.userprofile.account_balance, 0)

        self.user_contract4.refresh_from_db()
        self.assertEqual(self.user_contract4.status, 0)
        self.user4.refresh_from_db()
        self.assertEqual(self.user4.userprofile.account_balance, 0)
