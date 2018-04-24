from djongo import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    screen_name = models.TextField()
    location = models.TextField()
    description = models.TextField()
    utc_offset = models.IntegerField()
    time_zone = models.TextField()
    lang = models.TextField()
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'screen_name': self.screen_name
        }


class Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    text = models.TextField()
    entities = models.ListField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    retweet_count = models.IntegerField()
    favorite_count = models.IntegerField()
    geo = models.ListField()
    country = models.TextField()
    predicted_country = models.BooleanField(default=False)
    sentiment = models.TextField(default='')
    promotion = models.TextField(default='')
    feedback=models.TextField(default='')
    
    
    def as_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'text': self.text,
            'user': self.user.as_dict(),
            'country': self.country,
            'sentiment': self.sentiment,
            'promotion': self.promotion,
            'issue': self.issue
        }


class Option(models.Model):
    option_name = models.TextField(primary_key=True)
    option_value = models.TextField()
