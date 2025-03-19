import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class LogisticPCA(nn.Module):
    """
    Logistic PCA implementation for binary data following the R package methodology.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
    """
    def __init__(self, n_features, n_components, m=5):
        super(LogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  # Large value to approximate the natural parameters from the saturated model

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  # Mean vector (mu)
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  # Projection matrix (d × k)

    def forward(self, X):
        """
        Compute the natural parameters and projected probabilities.
        """
        theta_tilde = self.m * (2 * X - 1)  # Approximate Bernoulli natural parameter
        Z = torch.matmul(theta_tilde - self.mu, self.U)  # Projected principal component scores (n × k)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  # Reconstruct natural parameters (n × d)

        # Compute probability matrix P using sigmoid (logistic function)
        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01):
        """
        Train the Logistic PCA model using Binary Cross-Entropy Loss.
        """
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)
            loss.backward()
            optimizer.step()

            if epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}")

    def transform(self, X):
        """
        Transform input binary data into lower-dimensional representation (PC scores).
        """
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        """
        Reconstruct original binary data from lower-dimensional representation.
        """
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()
