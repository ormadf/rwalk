from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Algorithm, Comment
from .forms import AlgorithmForm, CommentForm

from .forms import RandWalkForm
from .forms import SelfAvoidForm
import pygal
from .my_nr_random_walk import MyNRRandomWalk
from .my_saw import SAW
# Create your views here.

def index(request):
    ''' homepage for walk'''
   
    return render(request, "walk/index.html")
           	
    
def rand_walk_image(request,steps):
    '''
    make radnom walk and render the trajectory x[] , y[]    	
    '''  
    steps_error = False
    #print("randwalk image steps_error: ",steps_error)	
    print("randwalk image num of steps: "+steps) 
    steps=int(steps)
    if steps== -100:
        steps_error = True
        steps = 100		
    #Non-Return Random Walk simulation
    rw=MyNRRandomWalk(steps)
    rw.fill_walk()	
    x_walk=rw.x_val
    y_walk=rw.y_val	
    chart = pygal.XY(show_x_guides=True)
    chart.add('NR random walk', [(x_walk[i],y_walk[i]) for i in range(0,steps)])
    chart.add('start',[(0,0)],foreground='#1aef07',dots_size=10)	
    chart.add('end',[(x_walk[-1],y_walk[-1])],foreground='#1aef07',dots_size=10)
    if steps_error == False:	
        chart.title='Non-Returning Random Walk. BLUE dot: Start, GREEN dot: Finish '
    else:
        chart.title='Non-Returning Random Walk. BLUE dot: Start, GREEN dot: Finish \n steps error: default steps = 100'
    	
    return chart.render_django_response( show_legend=False)
    
def self_avoid_walk_image(request,samples,steps):
    '''  make self avoiding walk on pygal.
         if steps and numbers are not integers then deafault values are used     
    ''' 
    samples_error = False	
    steps_error = False	
    samples=int(samples)
    steps = int(steps)	
    if samples == -10: 
        samples = 10
        samples_error = True		
    if steps == -10:
        steps = 10
        steps_error = True		
                    		
    print("samples: ",samples,"steps: ",steps )
    mysaw = SAW(samples,steps)
    mysaw.fill_walk()
    x_walk, y_walk = mysaw.walk()

    
    chart = pygal.XY(show_x_guides=True)
    length=len(x_walk)
    if length < steps:
        print('collison: not enough samples')
        chart.add('SAW' , [(x_walk[i],y_walk[i]) for i in range(0,length)])
        chart.add('start',[(0,0)],foreground='#1aef07', dots_size=10)
        chart.add('end',[(x_walk[-1],y_walk[-1])],foreground='#1aef07',dots_size=10)		
        if (samples_error or steps_error):
            chart.title='Self Awoiding walk: BLUE dot: start GREEN dot: finish \n COllision: not enough trials \n incorrect entry, default steps = 10 samples = 10'
        else:
            chart.title='Self Awoiding walk: BLUE dot: start, GREEN dot: finish \n Collision (not enough trials)'            		
    else:		
        chart.add('SAW', [(x_walk[i],y_walk[i]) for i in range(0,length)])
        chart.add('start',[(0,0)],foreground='#1aef07', dots_size=10)
        chart.add('end',[(x_walk[-1],y_walk[-1])],foreground='#1aef07',dots_size=10)	
        if (steps_error or samples_error):
            chart.title='Self Avoiding Walk: BLUE dot: start GREEN dot: finish \n incorrect entry, default steps = 10 samples = 10'		
        else:
            chart.title='Self Avoiding Walk: Success BLUE dot: start GREEN dot: finish '		
    #chart.add('bla',[(-steps,-steps),(5,5)])
    return chart.render_django_response(show_legend=False)	
	
def nr_rand_walk(request):
    ''' the form for non-returning random walk'''
    steps_error = False   
    if request.method == 'POST':
        form = RandWalkForm(request.POST)
        if form.is_valid():
            steps=form.cleaned_data['steps']
            			
            if steps.isdigit():
                steps = int(steps)
                
                print("nr_rand_walk steps_error = False")				
            else:
                steps = -100 # default
                
                print("nr_rand_walk steps+error is True")				
                  		
            return HttpResponseRedirect('/rand_walk_image/%d/' % steps)
       
    else:
        form = RandWalkForm()
             
    return render(request, 'walk/nr_rand_walk.html',{'form':form})
	
def self_avoid_walk(request):
    ''' the form for self-avoiding walk '''  
    if request.method == 'POST':
        form = SelfAvoidForm(request.POST)
        if form.is_valid():
            samples=form.cleaned_data['samples']
            if samples.isdigit():
                samples = int(samples)
            else:
                samples = -10 # default value			
             				
            steps=form.cleaned_data['steps']
            if steps.isdigit():
                steps = int(steps)
            else:
                steps = -10 # default value			
                      			
            return HttpResponseRedirect('/self_avoid_walk_image/%d/%d/' %(samples,steps) )
       
    else:
        form = SelfAvoidForm()
             
    return render(request, 'walk/self_avoid_walk.html',{'form':form})

@login_required	
def algorithms(request):
    ''' Show the list of algorithms'''   	
    #algorithms=Algorithm.objects.filter(owner=request.user).order_by('date_added')	
    #### Filtering is commented ALWAYS: since we need to see all Algos Comments for ALL users	
    algorithms=Algorithm.objects.order_by('date_added')
    context = {'algorithms': algorithms}
    return render(request,'walk/algorithms.html', context)
    	
@login_required
def algorithm(request,algorithm_id):
    ''' Show a single algorithm with all comments ''' 
    algorithm = Algorithm.objects.get(id=algorithm_id)
    # make sure the algorithm belongs to the current user
    #if algorithm.owner != request.user:
    #    raise Http404
    # ##### this should be commented out ALWAYS - this allows see all algos and comments	
    comments = algorithm.comment_set.order_by('-date_added')
    context={'algorithm':algorithm, 'comments': comments}
    return render(request,'walk/algorithm.html',context)

# REMOVE/ HIDE THIS FUNCTION???: ONLY ADMIN WILL BE ABLE TO MAKE NEW ALGO	
@login_required   
def new_algorithm(request):
    """ Add a new algorithm"""	
    if request.method != 'POST':
        # no data submitted : create an epty form
        form=AlgorithmForm()
    else:
        # POST data submitted: process data
        form=AlgorithmForm(request.POST)
        if form.is_valid():
            new_algorithm = form.save(commit=False)
            new_algorithm.owner = request.user	  		
            new_algorithm.save()
            return HttpResponseRedirect(reverse('walk:algorithms'))	
          
    context={'form': form}
    return render(request, 'walk/new_algorithm.html',context)

@login_required	
def new_comment(request,algorithm_id):
    """ new comment for a particular algorithm"""
    algorithm = Algorithm.objects.get(id=algorithm_id)
    
    if request.method != 'POST':
        # no data submitted: create blank form
        form = CommentForm()
    else:
        # POST data submitted: process data
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.algorithm =algorithm
            new_comment.save()
            return HttpResponseRedirect(reverse('walk:algorithm',args=[algorithm_id]))
    context = {'algorithm': algorithm,'form': form}	
    return render(request,'walk/new_comment.html', context)

@login_required
def edit_comment(request,comment_id):
    """ edit existing comment """
    comment = Comment.objects.get(id=comment_id)
    algorithm = comment.algorithm
    if algorithm.owner != request.user:
        #raise Http404
        return render(request,'walk/edit_error.html')		
    # ###### it is possible make comment owner = foreign key(user) compare with request.user 	models.py
    if request.method !='POST':
        #initial request; prefill form with current comment
        form = CommentForm(instance=comment)
    else:
        # POST data submitted: process data	
        form=CommentForm(instance=comment,data=request.POST)   		
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('walk:algorithm',args=[algorithm.id]))	

    context={'comment': comment, 'algorithm': algorithm, 'form': form}			
    return render(request,'walk/edit_comment.html',context)

	