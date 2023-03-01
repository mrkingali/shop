from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, fullname, password):

        if not phone_number:
            raise ValueError("user must have phone number ")
        if not email:
            raise ValueError("user must have email field")
        if not fullname:
            raise ValueError("user must have fullname field")

        user = self.model(phone_number=phone_number, email=self.normalize_email(email)
                          , fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, fullname, password):
        user = self.create_user(phone_number, email, fullname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user