from django.contrib.auth.models import BaseUserManager


class Manager(BaseUserManager):
    
    def create_user(self, phone, first_name, last_name,email, password):
        
        if not phone:
            raise ValueError('user must have an phone')
        
        if not first_name:
            raise ValueError('user must have an fist name')
        
        if not last_name:
            raise ValueError('user must have an last name')
        
        if not email:
            raise ValueError('user must have an email address')
        
        user = self.model(phone=phone, first_name=first_name,last_name=last_name, email=self.normalize_email(email))
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name,email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(phone=phone, first_name=first_name,last_name=last_name, email=email, password=password)

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

        

