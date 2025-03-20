import time
import numpy as np
import heapq
import gc

from .choclo_backend import choclo_backend

class ChocloOptimizer():

    def __init__(self,
                 loss_calculation_fcn,
                 prior_sampler_fcn=None,
                 posterior_sampler_fcn=None,
                 intermediate_sampler_fcn=None,
                 mini_batch_sampler_fcn=None,
                 parameter_transform_fcn=None,
                 batch_size=None):

        self.loss_calculation_fcn = loss_calculation_fcn
        self.prior_sampler_fcn = prior_sampler_fcn
        self.posterior_sampler_fcn = posterior_sampler_fcn
        self.intermediate_sampler_fcn = self.intermediate_sampler_uniform_distribution
        if intermediate_sampler_fcn is not None:
            self.intermediate_sampler_fcn = intermediate_sampler_fcn
        self.mini_batch_sampler_fcn = self.mini_batch_random_choice
        if mini_batch_sampler_fcn is not None:
            self.mini_batch_sampler_fcn = mini_batch_sampler_fcn
        self.parameter_transform_fcn = parameter_transform_fcn
        self.w = []
        self.batch_size=batch_size
        self.ipyparallel=False
        self.choclo_data=None

    class ChocloData():

        def __init__(self,prior_random_samples,posterior_random_samples,number_of_parameters,args):
            self.current_weights = np.array([])
            self.best_weight_vector = np.array([])
            self.loss_history = []
            self.update_history = []
            self.update_by_cycle = []
            self.loss_by_cycle = []
            self.loss_by_realization = []
            self.update_by_realization = []
            self.realization_number = 1
            self.cycle_number = 1
            self.number_of_updates = 1
            self.args = args
            self.prior_random_samples = prior_random_samples
            self.posterior_random_samples = posterior_random_samples
            self.number_of_parameters = number_of_parameters

        def increment_realization_number(self):
            self.realization_number = self.realization_number+1

        def increment_cycle_number(self):
            self.cycle_number = self.cycle_number+1

        def increment_number_of_updates(self):
            self.number_of_updates = self.number_of_updates+1

        def reset_histories(self):
            self.loss_history = []
            self.update_history = []
            self.cycle_number = 1


    def load_choclo_data(self,choclo_data):
        self.choclo_data = choclo_data

    def intermediate_sampler_uniform_distribution(self, choclo_data):

        random_samples = choclo_data.prior_random_samples
        variances = np.var(choclo_data.update_history[:,:],axis=1).flatten()
        means = choclo_data.update_history[:,-1].flatten()

        return np.vstack([np.random.uniform(mu-np.sqrt(sigma*12)/4,mu+np.sqrt(sigma*12)/4,(random_samples)) for sigma,mu in zip(variances,means)])

    def mini_batch_random_choice(self,X,y,batch_size):
        all_samples = np.arange(0,X.shape[0])
        rand_sample = np.random.choice(all_samples,size=batch_size,replace=False)
        X_batch = X[rand_sample]
        y_batch = y[rand_sample]
        return X_batch,y_batch

    def optimize(self,X,y,number_of_parameters,args=[],
            number_of_realizations=1,
            number_of_cycles=20,
            update_volume=10,
            number_of_random_simulations = 1000,
            update_volatility = 1,
            min_loss_per_change=0,
            convergence_z_score=1,
            analyze_n_parameters=None,
            update_magnitude=None,
            prior_random_samples=None,
            posterior_random_samples=None,
            prior_uniform_low=-1,
            prior_uniform_high=1,
            print_feedback=True):

        fresh_start = False
        if self.choclo_data is None:
            fresh_start = True
            self.choclo_data = self.ChocloData(prior_random_samples,posterior_random_samples,number_of_parameters,args)

        parameters = np.zeros((number_of_realizations,number_of_parameters))
        losses = np.zeros((number_of_realizations,1))
        for run in range(number_of_realizations):

            start_time = time.time()
            if self.batch_size is None:
                X_batch = X
                y_batch = y
            else:
                X_batch,y_batch = self.mini_batch_sampler_fcn(X,y,self.batch_size)

            self.model = choclo_backend(X_batch,y_batch,self.loss_calculation_fcn,
                                      number_of_parameters=number_of_parameters,
                                      args=args,model=self.choclo_data)


            #random simulation parameters
            self.model.default_random_simulation_params(prior_uniform_low=prior_uniform_low
                                                   ,prior_uniform_high=prior_uniform_high
                                                   ,prior_random_samples=prior_random_samples
                                                   ,random_sample_num=posterior_random_samples)


            self.model.adjust_optimizer(number_of_cycles=number_of_cycles,
                                            number_of_random_simulations=number_of_random_simulations,
                                                update_volatility=update_volatility,
                                                analyze_n_parameters=analyze_n_parameters,
                                                update_volume=update_volume)


            if self.prior_sampler_fcn is not None:
                self.model.change_prior_sampler(self.prior_sampler_fcn)
            if self.posterior_sampler_fcn is not None:
                self.model.change_random_sampler(self.posterior_sampler_fcn)
            if self.parameter_transform_fcn is not None:
                self.model.change_parameter_transform(self.parameter_transform_fcn)

            self.model.adjust_convergence_z_score(convergence_z_score)
            self.model.adjust_min_loss_per_change(min_loss_per_change)

            if run==0 and fresh_start==False:
                self.model.change_prior_sampler(self.intermediate_sampler_fcn)

            if run>0:
                #this overrides the default simulation function
                #we will use the best parameter set from the previous run as the priors for the current
                self.choclo_data = self.model.choclo_data
                self.model.change_prior_sampler(self.intermediate_sampler_fcn)

            #fix plot_feedback
            self.model.optimize(print_feedback=print_feedback)

            params = self.model.get_param_by_iter()
            errors = self.model.get_loss_by_iter()
            best_w_arr = errors.argsort()[0]
            loss = errors[best_w_arr]
            w = params[best_w_arr].T

            self.w = w
            parameters[run] = w
            losses[run] = loss
            self.choclo_data.increment_realization_number()
            end_time = time.time()

            if print_feedback:
                print('realization',run,'loss',loss,'time',end_time-start_time)

        if isinstance(self.choclo_data.update_by_realization, np.ndarray):
            self.choclo_data.loss_by_realization = np.vstack([self.choclo_data.loss_by_realization, losses])
            self.choclo_data.update_by_realization = np.vstack([self.choclo_data.update_by_realization, parameters])
        else:
            self.choclo_data.loss_by_realization = losses
            self.choclo_data.update_by_realization = parameters
        return self
