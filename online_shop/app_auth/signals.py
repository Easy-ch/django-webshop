from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
import threading
import time
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Этот блок кода будет выполнен только при создании нового пользователя
        user_id = instance.id
        print(f"Пользователь создан! ID пользователя: {user_id}")
        my_thread = threading.Thread(target=delete_user, args=(user_id,  ))
        my_thread.start()

def delete_user(user_id):
    time.sleep(300)
    user = User.objects.get(id=user_id)
    if user.is_verified_email:
        print("Пользователь подтвердил свою почту. Удаление отменено.")
        return
    try:
        user.delete()
        print(f"Пользователь {user.username} успешно удален.")
    except User.DoesNotExist:
        print(f"Пользователь с id={user_id} не существует.")