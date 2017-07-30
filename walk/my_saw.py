from random import randint
#this is django version
class SAW():
    """self-avoiding walk on two-dimensional lattice"""
    def __init__(self, num_samples=4 ,num_steps= 10 ):
        """ self-avoiding random walk"""  
        self.num_samples = num_samples	
        self.num_steps = num_steps
        self.x_val = [0]
        self.y_val=[0]
        self.lattice=[[0 for x in range(-num_steps,num_steps)] for y in range(-num_steps,num_steps)]
        #self.terminate = False  	
                      
			  
    def stepf(self):
        die = randint(1,4)
        if die == 1:
            x_step = 1
            y_step = 0
        elif die == 2:
            x_step = 0
            y_step = 1					
        elif die == 3:
            x_step = -1
            y_step = 0					
        elif die == 4:
            x_step = 0
            y_step = -1
        else:
            print("stepf error")    		
        return [x_step,y_step]	# returns vector of one step (up down left right)		
       	   
    def fill_walk(self):
        """calc the random walk points"""	
        terminate=False  # when terminate is True - the walk is successful, end the program		
        #sample is a "polymer" (a single self-avoiding walk)
        for sample in range(1,self.num_samples): 
            #print("sample: "+str(sample)  )			
            if terminate == True:
                print('Terminate: simulation success')			
                break  # SAW walk is done - end of simulation
            # start new walk from (0,0):				
            self.x_val = [0]
            self.y_val=[0]                     				            		
            # place a marker to the starting point in the center of the lattice
            x_current = 0
            y_current = 0
            x_prev = 0 # x_prev , y_prev  - trailing / previous location of the "turtle"
            y_prev = 0
            self.lattice[0][0] = sample+1 # we mark the initial site as 'backstep' to block return
			#first step: 
            x_step,y_step = self.stepf()
            x_current,y_current = x_prev +x_step, y_prev + y_step
            self.x_val.append(x_current)
            self.y_val.append(y_current)
            self.lattice[x_current][y_current] = sample+1 # labeled as a "backstep" 			
            #run steps loop    
            for step in range(2,self.num_steps+1):                     			
                print(" start step:",step)    				
                # make a step: left, right, up or down
                x_step, y_step = self.stepf()                          				                             				
                x_new = x_current + x_step
                y_new = y_current + y_step
   				                
                #ignore the stepback and try again:		
                while (self.lattice[x_new][y_new] == sample + 1):                    				
                    x_step, y_step = self.stepf()				
                    x_new = x_current + x_step
                    y_new = y_current + y_step					
                                                                  
                # check if the step is labeled as 'sample' (which means 'visited')
                if (self.lattice[x_new][y_new]==sample):
                    #break from step loop and go to new sample				
                    # append x_new y_new dot to the list and break ('head' hit the 'tail')
                    # it is for illustration:  the collision is shown in figure					
                    self.x_val.append(x_new)
                    self.y_val.append(y_new)	
                    # MAKE x_prev, y_prev =sample instead of sample+1: 
                    self.lattice[x_prev][y_prev]=sample	# sample+1 may cause error in the next sample simulation				
                    # BREAK NOW from this loop	and go to next sample
                    break
                     
                                         					
                    					
                else:
                    print("in else, step: ",step)
                    print(" we make move and label the previous site =sample")					
                    self.lattice[x_prev][y_prev] = sample			
                    x_prev, y_prev = x_current, y_current					
                    self.lattice[x_prev][y_prev]=sample+1 
                    x_current, y_current = x_new, y_new     
                    self.x_val.append(x_current)
                    self.y_val.append(y_current)
                    #print(self.x_val)
                    #print (self.y_val)
                    if step == self.num_steps:
                        print('steps ended: now terminate')					
                        terminate = True # successful walk, end the program					
                          
    def walk(self):
        """ returns the computed SAW walk as two lists"""
        return self.x_val, self.y_val
        		
					  