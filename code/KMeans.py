import pandas as pd
import numpy as np
from dist import dist, search
import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
import scipy

embeddings_path = os.path.join(os.pardir, "data", "embeddings.pkl")
out_path = os.path.join(os.pardir, "data", "sentences.pkl")


class KMeans(BaseEstimator, ClusterMixin, TransformerMixin):
    '''
        Custom implementation of KMeans that fits to sklearn's pipeline
    '''

    def __init__(self, K, max_iter = 100, distance = 'cosine', tol = 1e-3):
        '''
            constructor for KMeans class

            arguments:
                - K: number of clusters
                - max_iter: max number of iterations
                - distance: distance measure to use - 'cosine' or 'euclid'
                - tol: tolerance for convergence
        '''

        assert K >= 1, ('invalid K , must be +ve')
        assert max_iter >= 1, ('invalid max_iter, must be +ve')
        assert tol > 0 and tol < 1, ('tol must be in rangd (0, 1)')

        self.K = K
        self.max_iters = max_iter
        self.dist = distance
        self.centroids = None
        self.labels = None
        self.tolerance = tol


    def init_centroids(self, X):
        '''
            this method returns the initial centroids
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - centroids: centroids matrix (k * d dims)
        '''

        n, d = X.shape
        centroids = np.zeros((self.K, d))

        ## INSTRUCTION: randomly choose self.K rows from X
        ## and assign them as centroids and return centroids
        ## Hint: look at np.random.choice function
        #for k in range(self.K):
        #centroids[k] = X[np.random.choice(n)]
        k = 0
        for i in np.random.choice(n, self.K, replace=False):
            centroids[k] = X[i]
            k += 1
        return centroids


    def cost(self, X):
        '''
            this method returns the sum of distance between centroid and points for each cluster
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - dists: vector of length k where dists[i] is sum of distance
                            between centroid[i] and points that lie in cluster i
        '''
        costs = np.zeros(self.K)
        for k in range(self.K):
            ## instructions: compute the sum of the distances between documents belonging to cluster k and its centroid
            ## hint: you might want to use dist function from dist.py here
            temp = np.compress(self.labels==k, X, axis=0)
            costs[k] = dist(temp, self.centroids[k], self.dist).sum()
        return costs

    def reassign(self, X):
        '''
            this method returns the new labels for each data point in X
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - labels: vector of length n where labels[i] is the
                    cluster label for ith point
        '''
        n, d = X.shape
        new_assign = np.zeros(n)
        ## instructions: compute the new assignments for each row in X
        ## hint: you might want to use dist function from dist.py here

        #new_assign = [np.argmin(dist(self.centroids, X[i], self.dist)) for i in range(n)]
        for i in range(n):
            new_assign[i] = np.argmin(dist(self.centroids, X[i], self.dist))

        return new_assign

    def recompute(self, X):
        '''
            this method returns new centroids
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - centroids: new centroids computed from labels
        '''
        n, d = X.shape
        centroids = np.zeros((self.K, d))
        ## instructions: compute the new centroids
        for k in range(self.K):
            temp = np.compress(self.labels==k, X, axis=0)
            centroids[k] = np.mean(temp, axis = 0)

        return centroids

    def fit(self, X, y = None):
        '''
            this method is the body of the KMeans algorithm. It regroups the data X into k clusters
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - self
        '''
        if type(X) == scipy.sparse.csr.csr_matrix:
            X = X.toarray()

        n_iter = 0
        converged = False
        ## Step 1: initialize centroids and labels
        self.centroids = self.init_centroids(X)
        self.labels = self.reassign(X)


        ## iterate
        while n_iter < self.max_iters and not converged:
            ## Step 2: recompute centroids, recompute new document assignation, check stopping criteria
            self.centroids = self.recompute(X)
            self.labels = self.reassign(X)
            if n_iter > 0:
                if  obj - self.cost(X).sum() < self.tolerance:
                    converged = True

            obj = self.cost(X).sum()
            print('iter = {}, objective = {}'.format(n_iter, obj))
            n_iter += 1

        return self

    def get_n_documents(self, X, n = 5):
        '''
            this method returns the index of top n documents from each cluster
            input =>
                - X input data matrix (n * d dims)
                - n: number of top documents to return
            output: =>
                - results: list of tuple (k, index) which means doc at index belongs to cluster k
        '''
        if type(X) == scipy.sparse.csr.csr_matrix:
            X = X.toarray()
        labels = self.transform(X)
        results = []
        for k in range(self.K):
            ## Hint: look inside dist.py for help on this
            i = 0
            j = 0
            idxs = np.argsort(dist(X, self.centroids[k], self.dist))
            while i < n:
                index = idxs[j]
                if self.labels[index] == k:
                    results.append((k, index))
                    i += 1
                j += 1

        return results

    ## all the methods below are required for the integration with scikit-learn.
    ## DO NOT EDIT ANY METHOD BELOW HERE
    def transform(self, X, y = None):
        '''
            this method returns the labels by inferencing on fitted model
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - labels: inferred models
        '''
        if type(X) == scipy.sparse.csr.csr_matrix:
            X = X.toarray()
        return self.reassign(X)

    def fit_transform(self, X, y = None):
        '''
            this method returns the labels by fitting X to the model
            input =>
                - X : data matrix (n * d dims)
            output: =>
                - labels: inferred models
        '''
        self.fit(X)
        return self.labels

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder

## encoding dataset labels (refer classifier tutorial)
le = LabelEncoder()
y = le.fit_transform(dataset.category)

## bag of words vectorizer (refer classifier tutorial)
bow_vectorizer = CountVectorizer(lowercase = False,
                                     tokenizer = lambda x: x, # because we already have tokens available
                                     stop_words = None, ## stop words removal already done from NLTK
                                     max_features = 5000, ## pick top 5K words by frequency
                                     ngram_range = (1, 1), ## we want unigrams now
                                     binary = False) ## Now it's Bag of Words

## build a pipeline
pipeline_cosine = Pipeline([
    ('bow',  bow_vectorizer),
    ('tfidf',  TfidfTransformer()),
    ('k-means',  KMeans(K = len(list(le.classes_)), distance = 'cosine', tol = 1e-4) ) ])

pipeline_cosine.fit(dataset.tokens)
preds_cosine = pipeline_cosine.transform(dataset.tokens)
