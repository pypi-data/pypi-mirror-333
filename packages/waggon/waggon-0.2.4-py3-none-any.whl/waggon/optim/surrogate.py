import time
import pickle
import numpy as np
from scipy.optimize import minimize

from .base import Optimiser
from .utils import create_dir

class SurrogateOptimiser(Optimiser):
    '''
    Surrogate based black-box optimiser.

    Parameter
    ----------
    func : Callable, waggon.functions.Function
        Black-box function to be optimised.
    
    surr : waggon.surrogates.Surrogate or waggon.surrogate.GenSurrogate
        Surrogate model for the black-box function.
    
    acqf : waggon.acquisitions.Acquisition
        Acquisition function defining the optimisation strategy.
    
    max_iter : int, default = 100
        Maximum number of optimisation loop iterations.
    
    eps : float, default = 1e-1
        Epsilon-solution criterion value.
    
    error_type : {'x', 'f'}, default = 'x'
        Optimisation error type - either in argument, 'x', or function, 'f'.
    
    num_opt : bool, default = False
        Whether the acquisition function is optimised numerically or not. If False,
        the search of the next best parameters is done via direct search.
    
    eq_cons : dict, default = None
        Equality-type constraints for numerical optimisation.
    
    ineq_cons : dict, default = None
        Ineqaulity-type constraints for numerical optimisation.

    fix_candidates : bool, default = False if num_opt else True
        Whether the candidate points should be fixed or not.
    
    n_candidates : int, default = 1 if num_opt else 101**2
        Number of candidates points.
    
    olhs : bool, default = True
        Whether orthogonal Latin hypercube sampling (LHS) is used for choosing candidate points.
        If False, simple LHS is used.

    lhs_seed : int, default = None
        Controls the randomness of candidates sampled via (orthogonal) LHS.
    
    verbose : int, default = 1
        Controls verbosity when fitting and predicting. By default only a progress bar over the
        optimisation loop is displayed.
    
    save_results : bool, default = True
        Whether results are saved or not.
    '''
    def __init__(self, func, surr, acqf, **kwargs):
        super(SurrogateOptimiser, self).__init__(**kwargs)
        
        self.func           = func
        self.surr           = surr
        self.acqf           = acqf
        self.num_opt        = kwargs['num_opt'] if 'num_opt' in kwargs else True
        self.num_opt_disp   = kwargs['num_opt_disp'] if 'num_opt_disp' in kwargs else False
        self.tol            = kwargs['tol'] if 'tol' in kwargs else 1e-8
        self.eq_cons        = kwargs['eq_cons'] if 'eq_cons' in kwargs else None
        self.ineq_cons      = kwargs['ineq_cons'] if 'ineq_cons' in kwargs else None
        self.surr.verbose   = self.verbose
        self.candidates     = None

    def numerical_search(self, x0=None):
        '''
        Numerical optimisation of the acquisition function.

        Returns
        -------
        best_x : np.array of shape (func.dim,)
            Predicted optimum of the acquisition function.
        '''
        best_x = None
        best_acqf = np.inf

        if x0 is None:
            candidates = self.create_candidates()
        else:
            candidates = np.array(self.n_candidates * [x0])
            candidates += np.random.normal(0, self.eps, candidates.shape)

        for x0 in candidates:

            if (self.eq_cons is None) and (self.ineq_cons is None):
                opt_res = minimize(method='L-BFGS-B', fun=self.acqf, x0=x0, bounds=self.func.domain, tol=self.tol, options={'disp': self.num_opt_disp})
            else:
                opt_res = minimize(method='SLSQP', fun=self.acqf, x0=x0, bounds=self.func.domain, constraints=[self.eq_cons, self.ineq_cons])
            
            if opt_res.fun < best_acqf:
                best_acqf = opt_res.fun
                best_x = opt_res.x
        
        return best_x
    
    def direct_search(self):
        '''
        Direct search for the optimum of the acquisition function.

        Returns
        -------
        best_x : np.array of shape (func.dim,)
            Predicted optimum of the acquisition function
        '''
        
        if self.fix_candidates:
            if self.candidates is None:
                self.candidates = self.create_candidates()
        else:
            self.candidates = self.create_candidates()
        
        if self.eq_cons is not None:
            self.candidates = self.candidates[np.where(np.all(self.eq_cons(self.candidates) == 0, axis=0))[0]]
        if self.ineq_cons is not None:
            self.candidates = self.candidates[np.where(np.all(self.eq_cons(self.candidates) <= 0, axis=0))[0]]
        
        acqf_values = self.acqf(self.candidates)
        best_x = self.candidates[np.argmin(acqf_values)]
        
        return best_x

    def predict(self, X, y, n_pred=1):
        '''
        Predicts the next best set of parameter values by optimising the acquisition function.
        
        Parameters
        ----------
        X : np.array of shape (n_samples * func.n_obs, func.dim)
            Training input points.

        y : np.array of shape (n_samples * func.n_obs, func.dim)
            Target values of the black-box function.
        
        n_pred : int, defult = 1
            Number of predictions to make.
        
        Returns
        -------
        next_x : np.array of shape (func.dim, n_pred)
        '''

        self.surr.fit(X, y)
            
        self.acqf.y = y.reshape(y.shape[0]//self.func.n_obs, self.func.n_obs)
        self.acqf.conds = X[::self.func.n_obs]
        self.acqf.surr = self.surr

        next_xs = []

        while len(next_xs) < n_pred:
            if self.num_opt:
                next_x = self.numerical_search(X[np.argmin(y)])
            else:
                next_x = self.direct_search()
            
            if next_x not in X:
                next_xs.append(next_x)

        return np.array(next_xs)
    
    def _save(self, base_dir='test_results'):
        res_path = create_dir(self.func, self.acqf.name, self.surr.name, base_dir=base_dir)

        with open(f'{res_path}/{time.strftime("%d_%m_%H_%M_%S")}.pkl', 'wb') as f:
            pickle.dump(self.res, f)
