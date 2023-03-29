from django.db import models
from django.contrib.auth.models import User

# 1.Model DB (name, phn , address , image , join at)
class Clients(models.Model):
    user = models.OneToOneField(User,verbose_name=('client'),on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name = ('Full Name'),max_length=200)
    address = models.CharField(verbose_name = ('Address'),max_length=200)
    image = models.ImageField(verbose_name = ('Image'),upload_to='clients-profiles/')
    phone = models.CharField(verbose_name = ('Phone Number'),max_length=20)
    join_on = models.DateTimeField(verbose_name=('Join On'),auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Clients'
    def __str__(self):
        return self.full_name
    
# 2. Form Model 


# 3. HTML 
# 4. View
# 5. Path 