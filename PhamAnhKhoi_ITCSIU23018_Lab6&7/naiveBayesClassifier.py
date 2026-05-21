import pandas as pd
import numpy as np
import sys

class NaiveBayesFilter:
    def __init__(self):
        self.data = []
        self.vocabulary = []  # returns tuple of unique words
        
        self.p_spam = 0  # Probability of Spam
        self.p_ham = 0  # Probability of Ham
        self.n_words_spam = 0  # Total number of words in Spam messages
        self.n_words_ham = 0  # Total number of words in Ham messages
        
        # Initiate parameters
        self.parameters_spam = {}
        self.parameters_ham = {}

        
        # self.parameters_spam = {unique_word: 0 for unique_word in self.vocabulary}
        # print('parameters_spam: ', self.parameters_spam)
        # self.parameters_ham = {unique_word: 0 for unique_word in self.vocabulary}
        # print('parameters_ham: ', self.parameters_ham)


    def fit(self, X, y):
        self.vocabulary = set(word for sms in X for word in sms)
        self.parameters_ham = {word: 0 for word in self.vocabulary}
        self.parameters_spam = {word: 0 for word in self.vocabulary}

        rows = []
        sms_spam = 0
        sms_ham = 0

        for i, sms in enumerate(X):
            row = {word: 0 for word in self.vocabulary}
            
            sms_spam += 1 if y.iloc[i] == 'spam' else 0
            sms_ham += 1 if y.iloc[i] == 'ham' else 0
            
            for word in sms:
                row[word] += 1
                if y.iloc[i] == 'spam':
                    self.parameters_spam[word] += 1
                    self.n_words_spam += 1
                else:
                    self.parameters_ham[word] += 1
                    self.n_words_ham += 1

            row['Label'] = y.iloc[i]
            rows.append(row)
        
        self.data = pd.DataFrame(rows)
        self.p_spam = sms_spam / len(X)
        self.p_ham = sms_ham / len(X)
        
        # print('parameters_spam: ', self.parameters_spam)
        # print('parameters_ham: ', self.parameters_ham)

        return self.data
    
    
    def predict(self, X):
        prob = self.predict_proba(X)
        predict_labels = []
        
        for p in prob:            
            if p['P(spam|X)'] > p['P(ham|X)']:
                predict_labels.append('spam')
            else:
                predict_labels.append('ham')
        
        return predict_labels


    def predict_proba(self, X):
        proba = []
    
        for sms in X:
            p_mul_spam = self.p_spam
            p_mul_ham = self.p_ham
            
            for word in sms:
                # P(Xi|spam) and P(Xi|ham)
                p_xi_spam = (self.parameters_spam.get(word, 0) + 1) / (self.n_words_spam + len(self.vocabulary))
                p_xi_ham = (self.parameters_ham.get(word, 0) + 1) / (self.n_words_ham + len(self.vocabulary))
                
                # P(spam|Xi) and P(ham|Xi)
                p_mul_spam *= p_xi_spam
                p_mul_ham *= p_xi_ham
            
            proba.append({'P(spam|X)': p_mul_spam, 'P(ham|X)': p_mul_ham})
                
        return proba

    def score(self, true_labels, predict_labels):
        recall = 0
        tp = sum(1 for true, pred in zip(true_labels, predict_labels) if true == 'spam' and pred == 'spam')
        fn = sum(1 for true, pred in zip(true_labels, predict_labels) if true == 'spam' and pred == 'ham')
        if tp + fn > 0:
            recall = tp / (tp + fn)

        return recall