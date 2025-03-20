import time
import numpy as np
import heapq
import gc

from .helpers.heapsort import heapsort

from .choclo_parameter_search import choclo_search
import tensorflow as tf

tf.config.set_visible_devices([], 'GPU')
visible_devices = tf.config.get_visible_devices()

class CustomException(Exception):
    pass

def gradient_effect_size(inp, model):
    inp = list(map(lambda x:tf.Variable(x,dtype=tf.float32),inp))
    with tf.GradientTape() as tape:
        predictions = model(inp)
        grads = tape.gradient(predictions, inp)
    return grads


def create_default_tf_model(input_size, output_size=1):
    inp = tf.keras.Input(shape=input_size)

    x_0 = tf.keras.layers.Dense(100, activation="linear",use_bias=True)(inp)
    x_1 = tf.keras.layers.Dense(output_size, activation="linear",use_bias=True)(x_0)

    model = tf.keras.Model(inp, x_1)
    
    model.compile(
              optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss=tf.keras.losses.MeanSquaredError()
    )
                  
    return model

class choclo_backend():

    def __init__(self,X ,y ,loss_function ,number_of_parameters ,args=[] ,model=None, tf_meta_model=None):
        self.X = X
        self.y = y
        self.loss_calculation = loss_function
        self.choclo_data = model
        self.number_of_parameters = number_of_parameters
        self.args = np.array(args, dtype=object)
        self.loss_by_cycle = []
        self.update_by_cycle = []
        self.default_random_simulation_params()
        self.adjust_optimizer()
        self.prior_sampler = self.prior_sampler_uniform_distribution
        self.random_sampler = self.posterior_sampler_uniform_distribution
        self.parameter_transform = self.default_parameter_transform
        self.convergence_z_score = 2
        self.min_loss_per_change = 0
        self.has_args = False
        
        if tf_meta_model == None:
            self.tf_model = create_default_tf_model(input_size=number_of_parameters, output_size=1)


        if len(self.args)>0:
            self.has_args = True


    def set_weights(self, w):
        self.choclo_data.current_weights = w

    def heapsort(self,iterable):
        h = []
        for value in iterable:
            heapq.heappush(h, value)
        return [heapq.heappop(h) for i in range(len(h))]

    def adjust_convergence_z_score(self,z):
        self.convergence_z_score = z

    def adjust_min_loss_per_change(self,mlpc):
        self.min_loss_per_change = mlpc

    def default_parameter_transform(self,w,*args):
        return w

    def default_random_simulation_params(self,prior_random_samples=None,random_sample_num=None,prior_uniform_low=-1,prior_uniform_high=1):
        self.choclo_data.prior_random_samples = prior_random_samples
        self.choclo_data.posterior_random_samples = random_sample_num
        self.low = prior_uniform_low
        self.high = prior_uniform_high

    def adjust_optimizer(self,number_of_random_simulations=100,update_volatility=1,number_of_cycles=10,
                                   update_volume=2,
                                   analyze_n_parameters=None
                                   ):

        self.number_of_random_simulations = number_of_random_simulations
        self.update_volatility = update_volatility
        self.number_of_cycles = number_of_cycles
        self.update_volume = update_volume
        self.strokes = np.minimum(update_volume,100)

        self.analyze_n_parameters = analyze_n_parameters
        if self.analyze_n_parameters is None:
            self.analyze_n_parameters =  int(0.25*self.number_of_random_simulations)

        if self.choclo_data.prior_random_samples is None:
            self.choclo_data.prior_random_samples = int(self.number_of_random_simulations)

        if self.choclo_data.posterior_random_samples is None:
            self.choclo_data.posterior_random_samples = int(self.number_of_random_simulations)


        self.P = 0.9
        self.I = 0.9
        self.D = 0

    def _update_parameter_history(self):

        if len(self.choclo_data.update_history) == 0:
            self.choclo_data.update_history = self.choclo_data.current_weights
            self.choclo_data.loss_history = self.loss
            return
        try:
            self.choclo_data.update_history = np.column_stack((self.choclo_data.update_history,self.choclo_data.current_weights))
        except Exception as e:
                raise CustomException("Not enough samples, try increasing the number of simulations or volatility")

        self.choclo_data.loss_history =  np.hstack((self.choclo_data.loss_history,self.loss))

        try:
            self.choclo_data.update_history.shape[1]
            self.choclo_data.update_history.shape[0]
        except Exception as e:
            raise CustomException('parameter input must be 2-D, please check sample size or number of parameters.')


    def _sort_parameters_on_loss(self):
        self.choclo_data.current_weights = self.parameter_transform(
            self.choclo_data.current_weights.copy(), *self.args
        )

        tmp_loss = self.loss_calculation(
            self.X,
            self.y,
            self.choclo_data.current_weights.copy(),
            *self.args
        )
    
        ar_indx = np.arange(tmp_loss.shape[0])

        heap = []    
        for loss, i in zip(tmp_loss, ar_indx):
            if np.abs(loss)<float('inf') and ~np.isnan(loss):
                heap.append((loss, i))  
        

        sorted_heap = self.heapsort(heap)
        
        
        current_weights = []
        current_loss = []
        for loss, i in reversed(sorted_heap[:self.analyze_n_parameters]):

            update = self.choclo_data.current_weights[:,i]

            # Remove duplicates
            if len(current_weights)>0:
                if np.any(np.all(update == current_weights, axis=1)):
                    continue

            current_weights.append(update)
            current_loss.append(loss)
        
        self.choclo_data.current_weights = np.array(current_weights).T
        self.loss = np.array(current_loss)
        # self.choclo_data.current_weights = np.array(
        #     [self.choclo_data.current_weights[:,i]
        #                         for loss, i in reversed(sorted_heap[:self.analyze_n_parameters])]
        # ).T
        
        # self.loss = np.array([loss
        #                         for loss, i in reversed(sorted_heap[:self.analyze_n_parameters])])
        
        self._update_parameter_history()


    def prior_sampler_uniform_distribution(self,choclo_data):
        random_samples = choclo_data.prior_random_samples
        number_of_parameterss = choclo_data.number_of_parameters
        return np.random.uniform(low=self.low,high=self.high,size=(number_of_parameterss,
                                                                   random_samples))

    def posterior_sampler_uniform_distribution(self,choclo_data):

        random_samples = choclo_data.prior_random_samples
        variances = np.var(choclo_data.update_history[:,:],axis=1).flatten()
        means = choclo_data.best_weight_vector.flatten()

        return np.vstack([np.random.uniform(mu-np.sqrt(sigma*12)/2,mu+np.sqrt(sigma*12)/2,(random_samples)) for sigma,mu in zip(variances,means)])



    def _cycle(self, wh, lh, P=0.1, I=0.1, D=0):


        w = self.choclo_data.update_history[:,-1:]

        _y_ = self.choclo_data.loss_history.reshape(-1,1)
        _x_ = self.choclo_data.update_history.T

        with tf.GradientTape() as tape0:
            #train model and get next state q_value
            _y_p_ = self.tf_model(_x_)
            
            loss = self.tf_model.loss(_y_p_, _y_)
            
            grads = tape0.gradient(loss, self.tf_model.trainable_variables)
            self.tf_model.optimizer.apply_gradients(zip(grads, self.tf_model.trainable_variables))
            
        coefs = np.squeeze(gradient_effect_size([_x_], self.tf_model))
        coefs = np.mean(coefs, axis=0)
        effect_size = np.abs(coefs)
#         _x_ = np.column_stack((np.ones((_x_.shape[0],1)),_x_))*np.sqrt(sw)
#         A=_x_.T.dot(_x_)
#         b=_x_.T.dot(_y_*np.sqrt(sw))
        
        choices = np.arange(0,w.shape[0])
        
#         try:
#             _z_ = np.linalg.solve(A,b)
#             coefs = _z_[1:]
#             effect_size = np.abs(coefs.flatten()*w.flatten())
#         except:
#             coefs = np.std(self.choclo_data.update_history[:,:],axis=1).flatten()
#             effect_size =  np.std(self.choclo_data.update_history[:,:],axis=1).flatten()
            
            
        norm_effect_size = effect_size/np.sum(effect_size)

        # Account for case where there is only one parameter
        if len(choices) == 1:
            norm_effect_size = [norm_effect_size]
            coefs = [coefs]

        best_n_effects = np.random.choice(choices, np.minimum(self.update_volume, w.shape[0]),
                                             p = norm_effect_size,
                                             replace = False)

        
        # Initialize a list to modify with the PID search function
        mutation_list = np.concatenate([w for _ in range(best_n_effects.shape[0])],axis=1)[:, :, np.newaxis]
        mutation_list = np.concatenate([mutation_list for _ in range(self.strokes)],axis=2)

        count=0

        for i_ in best_n_effects:

            w_tmp  = w.copy()
            pid = choclo_search(P,I,D)

            pid.SetPoint = self.choclo_data.update_history[i_][-1]
            feedback =- self.update_volatility*coefs[i_]+self.choclo_data.update_history[i_][-1]

            pid.windup_guard = np.exp(np.clip(coefs[i_]*self.choclo_data.update_history[i_][-1] /np.abs(self.choclo_data.update_history[i_][-1]),-123.1,123.1))

            updates = np.zeros(self.strokes)
            for p in range(0, self.strokes):
                updates[p] = feedback
                pid.update(feedback)
                output = pid.output
                feedback += output

            mutation_list[i_, count, :] = updates

            count+=1


        # Modify the updated parameter list
        mutation_list = self.parameter_transform(mutation_list, *self.args)

        # Iterate through potential mutations and update the loss/parameters

        successful_mutations = self._multiple_fire(mutation_list)
        self._breed(successful_mutations)

    def _multiple_fire(self, mutation_list):


        w = self.choclo_data.update_history[:,-1].reshape((self.choclo_data.update_history.shape[0],1))
        loss_1 = self.choclo_data.loss_history[-1]
        for p in range(0, self.strokes):
            misfire=True

            tmp_loss = self.loss_calculation(self.X, self.y, mutation_list[:, :, p],*self.args)
        
            ar = np.arange(tmp_loss.shape[0])

            heap = [(l,i) for l,i in zip(tmp_loss,ar) if np.abs(l)<float('inf') and ~np.isnan(l)]
        
            sorted_heap = reversed(self.heapsort(heap))
            
            reduced_heap = [(loss_2,i) for loss_2,i in sorted_heap if (loss_2<loss_1) and abs(loss_2)<float('inf')]
            n_succesful_mutations = len(reduced_heap)

            successful_mutations = np.zeros((w.shape[0], n_succesful_mutations))
            count = 0
            for loss_2, i_ in reduced_heap:

                w = mutation_list[:,i_, p:p+1]
                self.choclo_data.update_history = np.column_stack((self.choclo_data.update_history, w))
                self.choclo_data.update_history = self.choclo_data.update_history[:, 1:]

                self.choclo_data.loss_history = np.hstack((self.choclo_data.loss_history, np.array([loss_2])))
                self.choclo_data.loss_history = self.choclo_data.loss_history[1:]
                loss_1=loss_2

                # misfire = False

                successful_mutations[:,count:count+1] = w
                count += 1
                self.choclo_data.increment_number_of_updates()

            # if misfire == False:
            #     break


        return successful_mutations


    def _breed(self,successful_mutations):

        loss_1 = self.choclo_data.loss_history[-1]

        ### replace with operators.breed
        N = successful_mutations.shape[1]
        if N<=1:
            return 0
        
        n_breed_combos = (N+1)*N//2 - N
        breed_list = np.zeros((successful_mutations.shape[0], n_breed_combos))
        count = 0
        for i in range(successful_mutations.shape[1]):
            for j in range(successful_mutations.shape[1]):
                if i<=j:
                    continue
                breed_list[:,count] =0.5*successful_mutations[:,i]+0.5*successful_mutations[:,j]
                count+=1
        ### replace with operators.breed

        breed_list = self.parameter_transform(breed_list,*self.args)

        tmp_loss = self.loss_calculation(self.X, self.y, breed_list, *self.args)
                
        ar = np.arange(tmp_loss.shape[0])
        
        heap = [(l,i) for l,i in zip(tmp_loss,ar) if np.abs(l)<float('inf') and ~np.isnan(l)]

        sorted_heap = reversed(self.heapsort(heap))
        
        reduced_heap = [(loss_2,i) for loss_2,i in sorted_heap if (loss_2<loss_1) and abs(loss_2)<float('inf')]
        for loss_2,i in reduced_heap:

            w = breed_list[:,i:i+1]
            self.choclo_data.update_history = np.column_stack((self.choclo_data.update_history,w))
            self.choclo_data.update_history = self.choclo_data.update_history[:, 1:]

            self.choclo_data.loss_history = np.hstack((self.choclo_data.loss_history, np.array([loss_2])))
            self.choclo_data.loss_history = self.choclo_data.loss_history[1:]
            self.choclo_data.increment_number_of_updates()

    def optimize(self, print_feedback=False):

        self.choclo_data.current_weights = self.prior_sampler(self.choclo_data)
        self.choclo_data.reset_histories()
        convergence = np.ones(self.choclo_data.number_of_parameters)*3
        loss_per_change = 1e6
        
        for n in range(0,self.number_of_cycles):

            self._sort_parameters_on_loss()

            self._cycle(                           self.choclo_data.update_history[:,:],
                                                  self.choclo_data.loss_history[:],
                                                  self.P,
                                                  self.I,
                                                  self.D)


            self.loss_by_cycle.append(self.choclo_data.loss_history[-1])
            self.update_by_cycle.append(self.choclo_data.update_history[:,-1])

            self.choclo_data.update_by_cycle = np.array(self.update_by_cycle)
            self.choclo_data.loss_by_cycle = np.array(self.loss_by_cycle)
            self.choclo_data.best_weight_vector = self.choclo_data.update_by_cycle[np.where(self.choclo_data.loss_by_cycle==np.min(self.choclo_data.loss_by_cycle))[0]]


            if n>0:
                loss_per_change = np.abs((self.choclo_data.loss_by_cycle[-1]-self.choclo_data.loss_by_cycle[-2])/self.choclo_data.loss_by_cycle[-2])

            if loss_per_change<self.min_loss_per_change:
                return True

            #current only accepts parameter vector
            if self.choclo_data.best_weight_vector.shape[0]>1:
                self.choclo_data.best_weight_vector = self.choclo_data.best_weight_vector[0]

            if n>=10:
                convergence = (self.choclo_data.best_weight_vector-np.mean(
                                self.choclo_data.update_by_cycle[-10:,:],axis=0))/(np.std(
                                self.choclo_data.update_by_cycle[-10:,:],axis=0))
                nans = np.isnan(convergence)
                convergence[nans] = 0
                convergence = np.abs(convergence)

            if np.all(np.abs(convergence)<self.convergence_z_score):
                return True


            new_weights = self.random_sampler(self.choclo_data)

            if new_weights is not None:
                self.choclo_data.current_weights = new_weights

            self.choclo_data.increment_cycle_number()
            gc.collect()

        return False

    def change_random_sampler(self,fcn):
        self.random_sampler = fcn

    def change_prior_sampler(self,fcn):
        self.prior_sampler = fcn

    def change_parameter_transform(self,fcn):
        self.parameter_transform = fcn

    def change_loss_calculation(self,fcn):
        self.loss_calculation = fcn

    def get_param_by_iter(self):
        return np.array(self.choclo_data.update_by_cycle)

    def get_loss_by_iter(self):
        return np.array(self.choclo_data.loss_by_cycle)

    def get_best_param(self):
        params = self.get_param_by_iter()
        errors = self.get_loss_by_iter()
        best_w_arr = errors.argsort()[0]
        w = params[best_w_arr]
        return w

    def get_update_history(self):
        return self.choclo_data.update_history