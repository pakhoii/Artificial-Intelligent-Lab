import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, weights=None, n_iters=100):
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.activation_func = self._unit_step_function
        self.weights = weights

        
    def _unit_step_function(self, x):
        return np.where(x > 0, 1, 0)
        
        
    def fit(self, X, y):
        x_samples, n_features = X.shape
        
        X = np.c_[np.ones(x_samples), X]
        
        if self.weights is None:
            self.weights = np.zeros(n_features + 1)
            
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights)
                y_predicted = self.activation_func(linear_output)
                
                update = self.learning_rate * (y[idx] - y_predicted)
                self.weights += update * x_i

                
                
    def predict(self, X):
        X = np.c_[np.ones(X.shape[0]), X]
        linear_output = np.dot(X, self.weights)
        y_predicted = self.activation_func(linear_output)
        return y_predicted
    
    
class MultiClassPerceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.classifiers = {}
        
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        
        for cls in self.classes:
            binary_y = np.where(y == cls, 1, 0)
            clf = Perceptron(learning_rate=self.learning_rate, n_iters=self.n_iters)
            clf.fit(X, binary_y)
            self.classifiers[cls] = clf
            
    
    def predict(self, X):
        class_scores = np.zeros((X.shape[0], len(self.classes)))
        
        for idx, cls in enumerate(self.classes):
            clf = self.classifiers[cls]
            class_scores[:, idx] = np.dot(np.c_[np.ones(X.shape[0]), X], clf.weights)
        
        predicted_classes = np.argmax(class_scores, axis=1)
        return self.classes[predicted_classes]
