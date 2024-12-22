from django.contrib.auth.models import User
class AccountAuthBackend:
    @staticmethod
    def authenticate(username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):  # Use `user_id` instead of `id_` for consistency
        try:
            return User.objects.get(pk=user_id)  # Must retrieve by primary key
        except User.DoesNotExist:
            return None
