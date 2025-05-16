""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np

from utils import minimized_angle
from soccer_field import *


class ExtendedKalmanFilter:
    def __init__(self, mean, cov, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.reset()

    def reset(self):
        self.mu = self._init_mean
        self.sigma = self._init_cov

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        # YOUR IMPLEMENTATION HERE

        #prediction implementation

        ut = env.forward(self.mu,u) 
        Gt = env.G(self.mu,u)
        Vt = env.V(self.mu,u)
        Mt = env.noise_from_motion(u,self.alphas)
        
        # Predicted covariance

        Gt_sigma_GT = np.dot(np.dot(Gt,self.sigma),Gt.T)
        Vt_Mt_VT = np.dot(np.dot(Vt,Mt),Vt.T)
        sigma_t = Gt_sigma_GT + Vt_Mt_VT

        #Correction implementation
        qt = np.array([[ self.beta[0][0] ]])
        zt = env.observe(ut,marker_id)
        Ht = env.H(ut,marker_id)
        

        # St Covariance

        St = np.dot(np.dot(Ht,sigma_t),Ht.T) + qt
        # Kalman Gain 
        Kt = np.dot(np.dot(sigma_t,Ht.T),np.linalg.inv(St))

        # udpated state
        Zt_Zi = minimized_angle (z - zt)
        self.mu = ut + np.dot(Kt,Zt_Zi)

        # Update Covariance 
        I = np.eye(3)
        I_KtHt = I - np.dot(Kt,Ht)


        self.sigma = np.dot(I_KtHt,sigma_t)

        return self.mu, self.sigma
