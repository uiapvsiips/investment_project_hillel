from celery import shared_task
from users.calculates import calc_balance


@shared_task
def my_hourly_task():
    calc_balance()


# @shared_task
# def print_to_console():
#     print('Текст, который будет выводиться в консоль каждые 5 секунд')
#     time.sleep(5)
#     print('Прошло 5 секунд')