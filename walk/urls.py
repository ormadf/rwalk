from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),	
    url(r'^nr_rand_walk/$',views.nr_rand_walk, name='nr_rand_walk'),
    url(r'^self_avoid_walk/$',views.self_avoid_walk,name='self_avoid_walk'),	
	url(r'^self_avoid_walk_image/(?P<samples>-?\d+)\/(?P<steps>-?\d+)/$', views.self_avoid_walk_image, name='self_avoid_walk_image'),
    url(r'^rand_walk_image/(?P<steps>-?\d+)/$', views.rand_walk_image, name='rand_walk_image'), 
    
    url(r'^algorithms/$', views.algorithms, name='algorithms'),
    # details of a single algorithm	
    url(r'^algorithms/(?P<algorithm_id>\d+)/$',views.algorithm, name='algorithm'),
    url(r'^new_algorithm/$',views.new_algorithm,name='new_algorithm'),

  	#template for new comment
    url(r'^new_comment/(?P<algorithm_id>\d+)/$',views.new_comment, name='new_comment'),
    # template to edit new comment	
    url(r'^edit_comment/(?P<comment_id>\d+)/$',views.edit_comment, name='edit_comment')	
]
