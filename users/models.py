import uuid
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models

from contracts.models import Contracts

CONTRACT_STATUS_CHOICES = (
    (0, 'active'),
    (1, 'completed'),
    (2, 'stopped')
)


class UserContracts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    deposit_amount = models.FloatField(default=0.0)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, choices=CONTRACT_STATUS_CHOICES)
    paid_money = models.FloatField(default=0.0)

    @property
    def days_from_start(self):
        DaysFromStart = (pytz.utc.localize(datetime.now()) - self.creation_date).days
        if DaysFromStart > self.contract.term:
            return self.contract.term
        return DaysFromStart

    @property
    def complete_percent(self):
        CompletePercent = round((self.days_from_start / self.contract.term) * 100)
        if CompletePercent >= 100:
            return 100
        return CompletePercent

    @property
    def current_profit(self):
        CurrentProfit = round(((self.contract.percent_for_day * self.days_from_start) * self.deposit_amount) / 100, 2)
        MaxTotalProfit = round(((self.contract.percent_for_day * self.contract.term) * self.deposit_amount) / 100, 2)
        if CurrentProfit > MaxTotalProfit:
            return MaxTotalProfit
        return CurrentProfit


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_uuid = models.UUIDField(default=uuid.uuid4)
    account_balance = models.FloatField(default=0.0)
    showing_contracts = models.ManyToManyField(Contracts)
    ref_link = models.CharField(max_length=200, null=True, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Wallets(models.Model):
    WALLET_TYPE_CHOICES = (
        (0, 'bank card'),
        (1, 'usdt'),
        (2, 'BTC'),
        (3, 'ETH')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    type = models.IntegerField(default=0, choices=WALLET_TYPE_CHOICES)
    wallet_number = models.CharField(null=True, max_length=150)
