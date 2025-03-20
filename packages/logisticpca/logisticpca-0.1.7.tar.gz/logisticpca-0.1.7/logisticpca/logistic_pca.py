import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class LogisticPCA(nn.Module):
    """
    Standard Logistic PCA for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
    """
    def __init__(self, n_features, n_components, m=5):
        super(LogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)
        Z = torch.matmul(theta_tilde - self.mu, self.U)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()


class SparseLogisticPCA(nn.Module):
    """
    Sparse Logistic PCA with L1 regularization for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
        lambda_L1 (float): Regularization strength for sparsity.
    """
    def __init__(self, n_features, n_components, m=5, lambda_L1=0.01):
        super(SparseLogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  
        self.lambda_L1 = lambda_L1  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)  
        Z = torch.matmul(theta_tilde - self.mu, self.U)  
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)

            # Add L1 sparsity penalty
            l1_penalty = self.lambda_L1 * torch.norm(self.U, p=1)  
            loss += l1_penalty
            
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}, L1 Penalty: {l1_penalty.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()
