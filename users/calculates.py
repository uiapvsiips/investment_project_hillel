# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geef.settings')
#
# import django
#
# django.setup()

from users.models import User
from django.core.handlers.wsgi import WSGIRequest

def earn_money_for_referrals(contract_user_id, offered_rate):
    user = User.objects.get(id=contract_user_id)
    # Если пользователя №4, открывающего контракт, привел пользователь №3, то ему (№3) начисляется 5% от суммы контракта
    # (первая линия)
    if user.userprofile.referred_by is not None:
        first_ref_user = User.objects.get(id=user.userprofile.referred_by.id)
        first_user_ref_reward = offered_rate * 0.05
        first_ref_user.userprofile.account_balance += first_user_ref_reward
        first_ref_user.save()
        # Если пользователя №3, который привел пользователя №4, открывающего контракт,
        # привел человек №2, то ему (№2) начисляется 3% от суммы контракта (вторая линия)
        if first_ref_user.userprofile.referred_by is not None:
            second_ref_user = User.objects.get(id=first_ref_user.userprofile.referred_by.id)
            second_user_ref_reward = offered_rate * 0.03
            second_ref_user.userprofile.account_balance += second_user_ref_reward
            second_ref_user.save()
            # Если пользователя №2, который привел пользователя №3, который привел пользователя (№4)
            # открывающего контракт, привел человек №1, то ему (№1) начисляется 1.5% от суммы контракта (третья линия)
            if second_ref_user.userprofile.referred_by is not None:
                third_ref_user = User.objects.get(id=second_ref_user.userprofile.referred_by.id)
                third_user_ref_reward = offered_rate * 0.015
                third_ref_user.userprofile.account_balance += third_user_ref_reward
                third_ref_user.save()


def calc_balance():
    # Сначала выбираются все пользователи, у которых открыты контракты
    users_with_contracts = [user for user in User.objects.all() if len(user.usercontracts_set.all()) > 0]
    for user in users_with_contracts:
        user_contracts = user.usercontracts_set.all()
        # После этого у выбранных пользователей выбираются активные контракты
        active_contracts = [user_contract for user_contract in user_contracts if user_contract.status == 0]
        for user_contract in active_contracts:
            # Если на момент вызова контракт должен был закончиться (контракт рассчитан на 365 дней, а пользователь
            # просматривает его на 366, то контракт закрывается, а тело контракта возвращается пользователю на баланс)
            if user_contract.days_from_start >= user_contract.contract.term and user_contract.status == 0:
                user_contract.status = 1
                user.userprofile.account_balance += user_contract.deposit_amount
            # Вычисляется сумма, которую недополучил пользователь на момент выполнения просчета и кладется ему на баланс
            # а так же записывается как выплаченная в контракт
            unpaid_money = user_contract.current_profit - user_contract.paid_money
            user.userprofile.account_balance += unpaid_money
            user_contract.paid_money += unpaid_money
            user.save()
            user_contract.save()


# if __name__ == '__main__':
#     calc_balance()