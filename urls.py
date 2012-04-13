from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
  url(r'^items/(\d+)$','TagItems.Items.views.barcode',name='items'),
  url(r'^items/(\d+)/rating/(\d+)','TagItems.Items.views.rated',name='rating'),                      
  url(r'items/search/','TagItems.Items.views.search',name='search'),
  url(r'^items/(\d+)/tagpost/$','TagItems.Items.views.tagpost',name='tagpost')
)
