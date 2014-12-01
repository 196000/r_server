from django.conf.urls import patterns, url
from server import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^run/$', views.run_rscript, name='run'),
		url(r'^results/$', views.results, name='results'),
		url(r'^add_data/$', views.add_data, name='add_data'),
		url(r'^add_targets/$', views.add_targets, name='add_targets'),
		url(r'^create_study/$', views.create_study, name='create_study'),
		url(r'^choose_target/$', views.choose_target, name='choose_target'),
		url(r'^manage_studies/$', views.manage_studies, name='manage_studies'),
		url(r'^choose_target/(?P<target>\w+)/$', views.set_target, name='set_target'),
		url(r'^choose_study/(?P<study>\w+)/$', views.choose_study, name='choose_study'),
		url(r'^remove_study/(?P<study>\w+)/$', views.remove_study, name='remove_study'),)