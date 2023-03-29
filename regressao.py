import numpy as np
import pandas as pd

class LinearRegression:
    
    def fit(self, x, y):
        x = np.array(x)
        y = np.array(y)
        
        # Número de observações e de variáveis
        n, p = x.shape
        
        # Adicionar coluna de 1's para intercepto
        x = np.concatenate([np.ones((n, 1)), x], axis=1)
        
        # Calcular estimadores dos coeficientes
        beta = np.linalg.inv(x.T.dot(x)).dot(x.T).dot(y)
        
        # Separar coeficiente linear e coeficientes angulares
        self.intercept_ = beta[0]
        self.coef_ = beta[1:]
        
        return self
        
    def predict(self, x):
        x = np.array(x)
        
        # Adicionar coluna de 1's para intercepto
        x = np.concatenate([np.ones((x.shape[0], 1)), x], axis=1)
        
        # Multiplicar matrizes de coeficientes e variáveis
        y_pred = x.dot(np.concatenate([[self.intercept_], self.coef_]))
        
        return y_pred
