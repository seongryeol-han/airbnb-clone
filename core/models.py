from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)  # model 만들때 시간을 넣어주고
    updated = models.DateTimeField(auto_now=True)  # model를 변경할 때마다 시간을 업데이트해줌

    # 데이터베이스에 저장되지 않도록 할때 abstract = True를 쓴다.
    class Meta:
        abstract = True
