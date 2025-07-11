""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np

from utils import minimized_angle

from soccer_field import *

class ParticleFilter:
    def __init__(self, mean, cov, num_particles, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.num_particles = num_particles
        self.reset()

    def reset(self):
        self.particles = np.zeros((self.num_particles, 3))
        for i in range(self.num_particles):
            self.particles[i, :] = np.random.multivariate_normal(
                self._init_mean.ravel(), self._init_cov)
        self.weights = np.ones(self.num_particles) / self.num_particles

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        # YOUR IMPLEMENTATION HERE
        
        # xt is particales and zt is observation and w is weight
        xt = np.zeros((self.num_particles, 3))  
        zt = np.zeros(self.num_particles)     
        w = np.zeros(self.num_particles)                 
        
        for i in range(self.num_particles):
            noise = env.sample_noisy_action(u, alphas=self.alphas).ravel()
            
            xt[i, :] = env.forward(self.particles[i, :], noise).ravel()
            
            zt[i] = env.observe(xt[i, :], marker_id)
            
            rw = minimized_angle(z - zt[i])
            
            w[i] = env.likelihood(rw, self.beta)
        
        w += 1.e-100  
        
        w /= np.sum(w)

        self.particles, self.weights = self.resample(xt, w)

        mean, cov = self.mean_and_variance(self.particles)
        return mean, cov

    def resample(self, particles, weights):
        """Sample new particles and weights given current particles and weights. Be sure
        to use the low-variance sampler from class.

        particles: (n x 3) matrix of poses
        weights: (n,) array of weights
        """
        new_particles, new_weights = particles, weights
        # YOUR IMPLEMENTATION HERE
        J = self.num_particles 
        new_particles = np.zeros_like(particles)  
        
        r = np.random.uniform(0, 1.0 / J)
        c = weights[0]                          
        i = 0                   
        
        for j in range(1, J + 1):         
            U = r + (j - 1) * (1.0 / J)   
            while U > c and i < J - 1:     
                i += 1                     
                c += weights[i]                
            new_particles[j - 1] = particles[i]        
    
        return new_particles, new_weights

    def mean_and_variance(self, particles):
        """Compute the mean and covariance matrix for a set of equally-weighted
        particles.

        particles: (n x 3) matrix of poses
        """
        mean = particles.mean(axis=0)
        mean[2] = np.arctan2(
            np.cos(particles[:, 2]).sum(),
            np.sin(particles[:, 2]).sum()
        )

        zero_mean = particles - mean
        for i in range(zero_mean.shape[0]):
            zero_mean[i, 2] = minimized_angle(zero_mean[i, 2])
        cov = np.dot(zero_mean.T, zero_mean) / self.num_particles

        return mean.reshape((-1, 1)), cov
