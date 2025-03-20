# Choclo Optimizer 

Project Status: Beta

Current Version: 3.37

Examples script will be updated soon.

## About 

ChocloOptimizer is brute force optimizer that can be used to train machine learning models. The package uses a combination of a neuroevolution algorithms, heuristics, and monte carlo simulations to optimize a parameter vector with a user-defined loss function.

The field of high performance computing is always change, and parallelization is very important for simulation based optimizers. This is why parallelization is left to the developer to implement. Chocloton supports Numba compiled functions for parallelization across CPUs and GPU acceleration. 

Due to the recent changes to threading and MKL in Anaconda distributions additional steps it has become difficult to incoporate the original parallelization engine, ipyparallel. 


## Table of contents
1. [Installation](#installation)
2. [Examples](#examples)
3. [Methods](#methods)
    1. [KmlData](#choclo_data)
    2. [Passing Static Data](#staticdata)
    2. [Parallel Processing with Numba](#parallelnumba)
	2. [Parallel Processing with Ray](#parallelray)
    2. [Convergence](#convergence)
    3. [Override Random Sampling Functions](#simulationdefaults)
    4. [Parameter Transforms](#transforms)
4. [Extensions](#ext)
    1. [Density Factorization](#hdr)

## Installation <a name="installation"></a>

```
pip install chocloton --upgrade
```

## The Algorithm ##

![](https://user-images.githubusercontent.com/21232362/122313182-bf75d280-cee3-11eb-8dc6-16158181cec2.PNG)

## Examples <a name="examples"></a>

### Density Factorization
1. Blog Post: https://rohankotwani.medium.com/hierarchical-density-factorization-with-kernelml-f2c98ce0eb1f
2. Project Link: https://github.com/freedomtowin/chocloton/tree/main/examples/density-factorization
3. Description:  Multi-Objective Optimization using IID Uniform Kernels

* Outline the goals of approximating any multi-variate distribution and building a parameterized density estimator.
* Discuss the approach using Particle Swarm/Genetic Optimizer, Multi-Agent Approximation, and Reinforcement Learning.
* Mention the applications like outlier detection and dataset noise reduction.

### Nearest Correlation Matrices
1. Blog Post: https://medium.com/towards-data-science/a-few-properties-of-random-correlation-matrices-and-their-nearest-correlation-matrices-7e0d7e1a29bb
2. Project Link: https://github.com/freedomtowin/chocloton/tree/main/examples/nearest-correlation-matrices
3. Description:  Finding Nearest (Positive Semi-Definite) Correlation Matrices

* Explain the relevance of finding the nearest positive semi-definite correlation matrix.
* Compare classical methods with the brute force approach using Chocloton.
* Discuss the significance in understanding the correlation matrix and improving correlation estimates.

### Chaotic Attractor Simulations
1. Blog Post: https://medium.com/@rohankotwani/interesting-properties-of-chaotic-attractors-1eb33e4bea99
2. Project Link: https://github.com/freedomtowin/chocloton/tree/main/examples/chaotic-attractor
3. Description:  Simulating Chaotic Attractors

* Introduce chaotic attractors and their properties.
* Discuss the hypothesis about the distribution of parameters leading to similar chaotic attractors.
* Present the results obtained using Chocloton.

### Circuit Solving
1. Blog Post: https://medium.com/vacatronics/brute-force-circuit-solving-with-kernelml-and-ray-b6fc3ff4fe14
2. Project Link: https://github.com/freedomtowin/chocloton/tree/main/examples/circuit-solving
3. Description:  Solving Simple Resistor/Transistor Circuits

* Explain the representation of circuits and the potential benefits of a brute-force solver.
* Emphasize the flexibility in changing variable representations without recomputing the algebraic solution.

### SVM Optimization
1. Blog Post: https://towardsdatascience.com/svm-optimization-on-a-gpu-with-kernelml-acb3d17856cd
2. Project Link: https://colab.research.google.com/drive/1Zkk7Q9guyP5cokn1_LSuK9s-UDQDzhrD?usp=sharing

* Provide an overview of the optimization of a multi-class, linear support vector machine.
* Discuss the use of Chocloton for SVM optimization and the benefits of using a simulation-based optimizer.

## Methods <a name="methods"></a>


### Chocloton <a name="intialization"></a>

```python
kml = chocloton.ChocloOptimizer(
                 loss_calculation_fcn,
                 prior_sampler_fcn=None,
                 posterior_sampler_fcn=None,
                 intermediate_sampler_fcn=None,
                 parameter_transform_fcn=None,
                 batch_size=None)
```

* **loss_calculation_fcn:** this function defines how the loss function is calculated 
* **prior_sampler_fcn:** this function defines how the initial parameter set is sampled 
* **posterior_sampler_fcn:** this function defines how the parameters are sampled between interations
* **intermediate_sampler_fcn:** this function defines how the priors are set between runs
* **parameter_transform_fcn:** this function transforms the parameter vector before processing
* **batch_size:** defines the random sample size before each run (default is all samples)

`loss_calculation_fcn=map_losses` should be structured as follows:

```python
def least_sq_loss_function(X,y,w):
   intercept,w = w[0],w[1:]
   hyp = X.dot(w)+intercept
   error = (hyp-y)
   return np.sum(error**2)

def map_losses(X,y,w_list):
    N = w_list.shape[1]
    out = np.zeros(N)
    for i in range(N):
        loss = least_sq_loss_function(X,y,w_list[:,i:i+1])
        out[i] = loss
    return out
```

The `loss_calculation_fcn` should map a list of input parameters to a list of loss function outputs. The `map_losses` function above calls the `least_sq_loss_function` and then stores the output for each parameter set in w_list.

```python
# Begins the optimization process, returns (list of parameters by run),(list of losses by run)
kml.optimize(   X,
                                                y,
                                                number_of_parameters,
                                                args=[],
                                                number_of_realizations=1,
                                                number_of_cycles=20,
                                                update_volume=10,
                                                number_of_random_simulations = 1000,
                                                update_volatility = 1,
                                                convergence_z_score=1,
                                                analyze_n_parameters=None,
                                                update_magnitude=None,
                                                prior_random_samples=None,
                                                posterior_random_samples=None,
                                                prior_uniform_low=-1,
                                                prior_uniform_high=1,
                                                print_feedback=True)
```
* **X:** input matrix
* **y:** output vector
* **loss_function:** f(x,y,w), outputs loss
* **number_of_parameters:** number of parameters in the loss function
* **args:** list of extra data to be passed to the loss function

### Iteration Parameters
* **number_of_realizations:** number of runs
* **number_of_cycles:** number of iterations (+bias)
* **update_volume:** the volume of attempted parameter updates (+bias)

### Learning Rate Parameters
The optimizer's parameters can be automatically adjusted by adjusting the following parameters:
* **number_of_random_simulations:** The number of random simulations per cycle
* **update_volatility:** increases the amount of coefficient augmentation, increases the search magnitude

### Automatically adjusted parameters
* **analyze_n_parameters:** the number of parameters analyzed (+variance)
* **update_magnitude:** the magnitude of the updates - corresponds to magnitude of loss function (+variance)
* **prior_random_sample_num:** the number of prior simulated parameters (+bias)
* **posterior_random_sample_num:** the number of posterior simulated parameters (+bias)

### Optinal Parameters
* **convergence_z_score:** an optional stopping threshold, stops a realization (see Convergence below)
* **min_loss_per_change:** an optional stopping threshold, stops a realization when the change in loss is below threshold
* **prior_uniform_low:** default pior random sampler - uniform distribution - low
* **prior_uniform_high:** default pior random sampler - uniform distribution - high
* **print_feedback:** real-time feedback of parameters,losses, and convergence


### choclo_data <a name="choclo_data"></a>

A KmlData class is primarily used to pass relevant information to the sampler functions.

### Data
* **ChocloOptimizer().choclo_data.best_weight_vector:** numpy array of the best weights for the current cycle 
* **ChocloOptimizer().choclo_data.current_weights:** numpy array of simulated weights for the current cycle
* **ChocloOptimizer().choclo_data.update_history:** numpy array of parameter updates for the current realization - (weight set, update #)
* **ChocloOptimizer().choclo_data.loss_history:** numpy array of losses for the current realization
* **ChocloOptimizer().choclo_data.realization_number:** current number of realizations
* **ChocloOptimizer().choclo_data.cycle_number:** current number of cycles
* **ChocloOptimizer().choclo_data.number_of_parameters:** number of parameters passed to the loss function
* **ChocloOptimizer().choclo_data.prior_random_samples:** the number of prior simulated parameters
* **ChocloOptimizer().choclo_data.posterior_random_samples:** the number of posterior simulated parameters
* **ChocloOptimizer().choclo_data.number_of_updates:** number of successful parameter updates

### Load choclo_data

An optimization model can continue where the previous model left off by loading the choclo_data.

```
#optimize
save_choclo_data = ChocloOptimizer().choclo_data
#load choclo_data
ChocloOptimizer().load_choclo_data(save_choclo_data)
```

### Passing Static Data <a name="staticdata"></a>

The args parameter can be set in the chocloton.ChocloOptimizer().optimize to pass extra data

```python
# For example, if args = [arg1,arg2]

def loss_function(X,y,w,arg1,arg2):
   return loss

def map_losses(X,y,w_list,arg1,arg2):
    N = w_list.shape[1]
    out = np.zeros(N)
    for i in range(N):
        loss = loss_function(X,y,w_list[:,i:i+1],arg1,arg2)
        out[i] = loss
    return out
```

### Parallel Processing with Numba <a name="parallelnumba"></a>

Starting with Chocloton 3.0, parallelization can be defined with nuba for GPU or CPU parallelization.

```python

from numba import jit,njit, prange

@jit('float64(float64[:,:], float64[:,:], float64[:,:])',nopython=True)
def least_sq_loss_function(X,y,w):
   intercept,w = w[0],w[1:]
   hyp = X.dot(w)+intercept
   error = (hyp-y)
   return np.sum(error**2)


@njit('float64[:](float64[:,:], float64[:,:], float64[:,:])',parallel=True)
def map_losses(X,y,w_list,alpha):
    N = w_list.shape[1]
    out = np.zeros(N)
    for i in prange(N):
        loss = least_sq_loss_function(X,y,w_list[:,i:i+1])
        out[i] = loss
    return out
```

### Parallel Processing with Ray <a name="parallelray"></a>

```python
@ray.remote
def map_losses(X,y,w_list,w_indx,args):
    N = w_indx.shape[0]
    resX = np.zeros(N)
    iter_ = 0
    for i in w_indx:
        loss = spiking_function(X,y,w_list[:,i:i+1],args)
        resX[iter_] = loss
        iter_+=1
    return resX
    

def ray_parallel_mapper(X,y,w_list,args):
    
    num_cores = 4
    
    weights_index = np.arange(0,w_list.shape[1])
    weights_index_split = np.array_split(weights_index,num_cores)
    
    w_list_id = ray.put(w_list)
    
    result_ids = [map_losses.remote(X_id,y_id,w_list_id,weights_index_split[i],args_id) for i in range(4)]
    result = ray.get(result_ids)
    
    loss = []
    indx = []
    for l in result:
        loss.extend(l)
    loss = np.hstack(loss)
    return loss
```

### Convergence <a name="convergence"></a>

The model saves the best parameter and user-defined loss after each iteration. The model also record a history of all parameter updates. The question is how to use this data to define convergence. One possible solution is:


```python
#Convergence algorithm
convergence = (best_parameter-np.mean(param_by_iter[-10:,:],axis=0))/(np.std(param_by_iter[-10:,:],axis=0))

if np.all(np.abs(convergence)<1):
    print('converged')
    break
 ```
 
The formula creates a Z-score using the last 10 parameters and the best parameter. If the Z-score for all the parameters is less than 1, then the algorithm can be said to have converged. This convergence solution works well when there is a theoretical best parameter set.

Another possible solution is to stop the realization when the the % change between cycles is less than a threshold. See `min_loss_per_change`.

### Override Random Sampling Functions <a name="simulationdefaults"></a>

The default random sampling functions for the prior and posterior distributions can be overrided. User defined random sampling function must have the same parameters as the default. Please see the default random sampling functions below. 

```python
    #prior sampler (default)
    def prior_sampler_uniform_distribution(choclo_data):
        random_samples = choclo_data.prior_random_samples
        num_params = choclo_data.number_of_parameters
        # (self.high and self.low) correspond to (prior_uniform_low, prior_uniform_high)
        return np.random.uniform(low=self.low,high=self.high,size=(num_params,
                                                                   random_samples))

    #posterior sampler (default)
    def posterior_sampler_uniform_distribution(choclo_data):
    
        random_samples = choclo_data.prior_random_samples
        variances = np.var(choclo_data.update_history[:,:],axis=1).flatten()
        means = choclo_data.best_weight_vector.flatten()

        return np.vstack([np.random.uniform(mu-np.sqrt(sigma*12)/2,mu+np.sqrt(sigma*12)/2,(random_samples)) for sigma,mu in zip(variances,means)])
            
            
    #intermediate sampler (default)
    def intermediate_sampler_uniform_distribution(choclo_data):

            random_samples = choclo_data.prior_random_samples
            variances = np.var(choclo_data.update_history[:,:],axis=1).flatten()
            means = choclo_data.update_history[:,-1].flatten()

            return np.vstack([np.random.uniform(mu-np.sqrt(sigma*12)/4,mu+np.sqrt(sigma*12)/4,(random_samples)) for sigma,mu in zip(variances,means)])
        
    from math import gamma
    #http://downloads.hindawi.com/journals/cin/2019/4243853.pdf
    def sampler_direction_based_stochastic_search(choclo_data):

        X = choclo_data.update_history[:,::-1]

        X = X[:,:X.shape[1] - X.shape[1]%2]

        X_N = X[:,:X.shape[1]//2] 
        X_M = X[:,X.shape[1]//2:]

        MUT = np.zeros((X.shape[0],X.shape[1]//2))

        BEST = X[:,0:1] 

        TOP_N_AVG = np.mean(X_N,axis=1)[:,np.newaxis]

        PAIR_DIFF = X_N - X_M

        DIRECTION_AVG = 1./3. * (TOP_N_AVG+BEST+X_N)

        DIRECTION_DEV = ((PAIR_DIFF)/12)**2 + 1e-9

        BEST_DEV = ((BEST-TOP_N_AVG)/12)**2 + 1e-9

        size = X.shape[1]//2

        Y_N = np.vstack([np.random.normal(DIRECTION_AVG[j],DIRECTION_DEV[j],size=(1,size)) for j in range(X.shape[0])])

        Y_M = np.vstack([np.random.normal(BEST[j],BEST_DEV[j],size=(1,size)) for j in range(X.shape[0])])

        Y_K = BEST + np.random.uniform(0,1,size=(X.shape[0],size))*PAIR_DIFF

        Y_L = DIRECTION_AVG + np.random.uniform(0,1,size=(X.shape[0],size))*(BEST-DIRECTION_AVG)

        iters = np.arange(X.shape[1]//2)
        Z_CAUCHY = X_N[:,iters % 3 == 0]+ X_N[:,iters % 3 == 0]*np.random.standard_cauchy(size=(np.sum(iters % 3 == 0)))
        MUT[:,iters % 3 == 0] = Z_CAUCHY

        NORM_MUT_DEV = ((BEST-X_N[:,iters % 3 == 1])/12)**2 + 1e-9
        Z_NORM = np.random.normal(BEST,NORM_MUT_DEV,size=(np.sum(iters % 3 == 1)))
        MUT[:,iters % 3 == 1] = Z_NORM

        lmbda = 1
        LEVY_DEV = (gamma(1+lmbda)*np.sin(np.pi*lmbda/2)/(gamma((1+lmbda)/2)*lmbda*2**((lmbda-1)/2)))**(1/lmbda)
        LEVY_U = np.random.normal(0,LEVY_DEV,size=(np.sum(iters % 3 == 0)))
        LEVY_V = np.random.normal(0,1,size=(np.sum(iters % 3 == 0)))
        Z_LEVY = X_N[:,iters % 3 == 0]+ 0.01*LEVY_U/(LEVY_V**(1/lmbda))
        MUT[:,iters % 3 == 0] = Z_LEVY


        X = np.hstack([X_N,Y_N,Y_M,Y_K,Y_L,MUT])

        #drop duplicates (substitution and substitute with random)

        NUM = X.shape[1]

        X = np.unique(X, axis=1)

        if NUM-X.shape[1]>0:
            sample_size = NUM-X.shape[1]
            RAND = [np.random.uniform(-0.1,0.1,size=(1,sample_size)) for _ in range(X.shape[0])]
            RAND = np.vstack(RAND)
            X = np.hstack([X,RAND])

        print(X.shape)

        return X
        
```

```python
    #mini batch random choice sampler
    def mini_batch_random_choice(X,y,batch_size):
        all_samples = np.arange(0,X.shape[0])
        rand_sample = np.random.choice(all_samples,size=batch_size,replace=False)
        X_batch = X[rand_sample]
        y_batch = y[rand_sample]
        return X_batch,y_batch
```   

### Parameter Transforms <a name="transform"></a>

The default parameter tranform function can be overrided. The parameters can be transformed before the loss calculations and parameter updates. For example, the parameters can be transformed if some parameters must be integers, positive, or within a certain range. The argument list in the Chocloton().optimize function are passed as parameters.

```python
# The default parameter transform return the parameter set unchanged 
def default_parameter_transform(w,*args):
    # w[rows,columns] = (parameter set,iteration)
    return w
```

## Extensions <a name="ext"></a>

### Hierarchical Density Factorization

```python
hdf = HierarchicalDensityFactorization(num_clusters=16,
                                                                 bins_per_dimension=61,
                                                                 smoothing_parameter=1.,
                                                                 min_leaf_samples=50,
                                                                 alpha=0.5)
```

* **number_of_clusters:** The number of clusters     
* **bins_per_dimension:** The number of histogram bins across each dimensions. This is used for estimating the kernel density function  
* **smoothing_parameter:** Increases the bandwidth of the kernel density estimation 
* **min_leaf_samples:** Prunes clusters than have less than the minimum number of samples
* **alpha:** Discount factor, 0<alpha<1

```python
hdf.optimize(X,maxiter=12,realizations=10,number_of_random_simulations=100,verbose=True)
```

* **X:** Input data -> (rows, columns)
* **maxiter:** maximum number of iterations
* **number_of_realizations:** number of runs                                    
* **number_of_random_simulations:** The number of random simulations per cycle  

```python
assignments = hdf.assign(X)
```
Returns an assignment matrix (observations, clusters) that represents whether a data point is within a hypercube cluster.

* **X:** Input data -> (rows, columns)


### Density Factorization <a name="hdr"></a>

```python
model = chocloton.region_estimator.DensityFactorization(number_of_clusters,bins_per_dimension=41,smoothing_parameter=2.0)
```                                    
                                    
* **number_of_clusters:** The number of clusters     
* **bins_per_dimension:** The number of histogram bins across each dimensions. This is used for estimating the kernel density function  
* **smoothing_parameter:** Increases the bandwidth of the kernel density estimation 

```python
model.optimize(X,y=None,agg_func='mean',
                        ,
                        number_of_random_simulations=500,
                        number_of_realizations=10,
                        )
```

This method runs the density factorization algorithm.

* **X:** Input data -> (rows, columns)
* **y:** target data -> (rows, columns)
* **agg_func:** The aggregate function for the target variable y: 'mean', 'variance', 'max', 'false-positive-cost', 'false-negative-cost', 'count'
* **number_of_realizations:** number of runs                                    
* **number_of_random_simulations:** The number of random simulations per cycle  


```python
assignments = model.get_assignments(X,pad=1.0)
```
Returns an assignment matrix (observations, clusters) that represents whether a data point is within a hypercube cluster.

* **X:** Input data -> (rows, columns)
* **pad:** This pads the variance of each density cluster.

```python
distance = model.get_distances(X,distance='chebyshev',pad=1.0)
```

Computes the distances between the data points and the hypercube centroids.

* **X:** Input data -> (rows, columns)
* **distance:** the distance metric used to assign data to clusters: 'chebyshev', 'euclidian','mae'
* **pad:** This pads the variance of each density cluster.

```python
model.prune_clusters(X,pad=pad,limit=10)
```

Prunes the clusters that have a lower number of data points than the limit. The model can be optimized after pruning.

* **X:** Input data -> (rows, columns)
* **pad:** This pads the variance of each density cluster.
* **limit:** the distance metric used to assign data to clusters: 'chebyshev', 'euclidian','mae'

