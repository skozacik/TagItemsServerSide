from django.db import models
# Create your mo
class ReviewManager(models.Manager):
    def get_by_natural_key(self, tag,votes):
        return self.get(tag,votes)
class Reviews(models.Model):
  objects=ReviewManager()
  votes=models.IntegerField()
  tag=models.CharField(max_length=255)
  def natural_key(self):
      return (self.tag,self.votes)
class Item(models.Model):
  bc=models.BigIntegerField()
  name=models.CharField(max_length=100)
  maker=models.CharField(max_length=50)
  review=models.ManyToManyField('Reviews')
  imageurl=models.URLField()
  rating=models.FloatField()
  raters=models.IntegerField()
  def natural_key(self):
      return (self.name,) + self.review.natural_key()
  natural_key.dependencies=['Items.app.review']
