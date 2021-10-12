from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
        
class User(AbstractUser):
    created          = models.DateTimeField(default=timezone.now)
    
    has_changed_pw   = models.BooleanField('Has changed password', default=None, null=True)
    pwd_update_time  = models.DateTimeField(editable=False, null=True, default=None)     
    
    def set_password(self, raw_password):
        if self.has_changed_pw is None:
            self.has_changed_pw = False
        elif not self.has_changed_pw:
            self.has_changed_pw = True
            self.pwd_update_time = timezone.now()
        else:
            self.pwd_update_time = timezone.now()
        super().set_password(raw_password)