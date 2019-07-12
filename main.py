from sklearn import manifold

import pandas
from flask import Flask
from flask import render_template
import random
import json
import os
from flask import send_from_directory
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import numpy as np
import sys
import matplotlib.pyplot as plt
from pymongo import MongoClient



app = Flask(__name__)

labels = []  # clustering
random_samples = []
adaptive_samples = []
samplesize = 400
imp_ftrs = []

data_csv = pandas.read_csv('credit_card_data.csv', low_memory=False)
data_csv_original = pandas.read_csv('credit_card_data.csv', low_memory=False)
data_csv = data_csv.fillna(0)
data_csv_original = data_csv_original.fillna(0)


ftrs = ['BALANCE','PURCHASES','ONEOFF_PURCHASES', 'INSTALLMENTS_PURCHASES','CASH_ADVANCE','CASH_ADVANCE_TRX','PURCHASES_TRX', 'CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS']
scaler = StandardScaler()
data_csv[ftrs] = scaler.fit_transform(data_csv[ftrs])

client = MongoClient('mongodb://localhost:27017')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def d3():
    return render_template('index.html')

# TASK 1b - find K in k-means.
def plot_kmeans_elbow():
    global data_csv_original
    cols = ['BALANCE',
            'PURCHASES',
            'ONEOFF_PURCHASES',
            'INSTALLMENTS_PURCHASES',
            'CASH_ADVANCE',
            'CASH_ADVANCE_TRX',
            'PURCHASES_TRX',
            'CREDIT_LIMIT',
            'PAYMENTS',
            'MINIMUM_PAYMENTS',
            ]
    features=data_csv_original[cols]
    features[cols] = np.log(1 + features[cols])

    print("Inside Plot elbow");

    ##features = data_csv_original[ftrs]

    k = range(1, 30)

    clusters = [KMeans(n_clusters=c, init='k-means++').fit(features) for c in k]
    centr_lst = [cc.cluster_centers_ for cc in clusters]

    k_distance = [cdist(features, cent, 'euclidean') for cent in centr_lst]
    distances = [np.min(kd, axis=1) for kd in k_distance]
    avg_within = [np.sum(dist) / features.shape[0] for dist in distances]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(k, avg_within, 'g*-')

    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.title('Elbow plot')
    plt.show()

def clustering():
    plot_kmeans_elbow()
    features = data_csv[ftrs]
    k = 10
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(features)
    kmeans_centres = kmeans.cluster_centers_
    labels = kmeans.labels_
    data_csv['kcluster'] = pandas.Series(labels)

# Task 1a
def random_sampling():

    global data
    global data_csv
    global random_samples
    global samplesize
    features = data_csv[ftrs]
    data = np.array(features)
    rnd = random.sample(range(len(data_csv)), samplesize)
    for j in rnd:
        random_samples.append(data[j])
    print(random_samples)

# Task 1a
def adaptive_sampling():
    # Adaptive samples
    global data_csv
    global adaptive_samples

    kcluster0 = data_csv[data_csv['kcluster'] == 0]
    kcluster1 = data_csv[data_csv['kcluster'] == 1]
    kcluster2 = data_csv[data_csv['kcluster'] == 2]
    kcluster3 = data_csv[data_csv['kcluster'] == 3]
    kcluster4 = data_csv[data_csv['kcluster'] == 4]
    kcluster5 = data_csv[data_csv['kcluster'] == 5]
    kcluster6 = data_csv[data_csv['kcluster'] == 6]
    kcluster7 = data_csv[data_csv['kcluster'] == 7]
    kcluster8 = data_csv[data_csv['kcluster'] == 8]
    kcluster9 = data_csv[data_csv['kcluster'] == 9]


    size_kcluster0 = len(kcluster0) * samplesize / len(data_csv)
    size_kcluster1 = len(kcluster1) * samplesize / len(data_csv)
    size_kcluster2 = len(kcluster2) * samplesize / len(data_csv)
    size_kcluster3 = len(kcluster3) * samplesize / len(data_csv)
    size_kcluster4 = len(kcluster4) * samplesize / len(data_csv)
    size_kcluster5 = len(kcluster5) * samplesize / len(data_csv)
    size_kcluster6 = len(kcluster6) * samplesize / len(data_csv)
    size_kcluster7 = len(kcluster7) * samplesize / len(data_csv)
    size_kcluster8 = len(kcluster8) * samplesize / len(data_csv)
    size_kcluster9 = len(kcluster9) * samplesize / len(data_csv)


    sample_cluster0 = kcluster0.ix[random.sample(list(kcluster0.index), int(size_kcluster0))]
    sample_cluster1 = kcluster1.ix[random.sample(list(kcluster1.index), int(size_kcluster1))]
    sample_cluster2 = kcluster2.ix[random.sample(list(kcluster2.index), int(size_kcluster2))]
    sample_cluster3 = kcluster3.ix[random.sample(list(kcluster3.index), int(size_kcluster3))]
    sample_cluster4 = kcluster4.ix[random.sample(list(kcluster4.index), int(size_kcluster4))]
    sample_cluster5 = kcluster5.ix[random.sample(list(kcluster5.index), int(size_kcluster5))]
    sample_cluster6 = kcluster6.ix[random.sample(list(kcluster6.index), int(size_kcluster6))]
    sample_cluster7 = kcluster7.ix[random.sample(list(kcluster7.index), int(size_kcluster7))]
    sample_cluster8 = kcluster8.ix[random.sample(list(kcluster8.index), int(size_kcluster8))]
    sample_cluster9 = kcluster9.ix[random.sample(list(kcluster9.index), int(size_kcluster9))]


    adaptive_samples = pandas.concat([sample_cluster0, sample_cluster1, sample_cluster2, sample_cluster3, sample_cluster4, sample_cluster5, sample_cluster6, sample_cluster7, sample_cluster8, sample_cluster9])
    print(adaptive_samples)

def generate_eigenValues(data):

    cov_mat = np.cov(data.T)
    eig_values, eig_vectors = np.linalg.eig(cov_mat)
    idx = eig_values.argsort()[::-1]
    eig_values = eig_values[idx]
    eig_vectors = eig_vectors[:, idx]
    return eig_values, eig_vectors

@app.route("/pca_scree")
def scree_adaptive():
    print("Inside scree")
    try:
        global adaptive_samples
        [eigenValues, eigenVectors] = generate_eigenValues(adaptive_samples[ftrs])
    except:
        e = sys.exc_info()[0]
        print(e)
    print('eigen values adaptive pca scree')
    print(eigenValues.tolist())
    return json.dumps(eigenValues.tolist())


def plot_intrinsic_dimensionality_pca(data, k):
    [eigenValues, eigenVectors] = generate_eigenValues(data)
    print (eigenValues)
    squaredLoadings = []
    ftrCount = len(eigenVectors)
    for ftrId in range(0, ftrCount):
        loadings = 0
        for compId in range(0, k):
            loadings = loadings + eigenVectors[compId][ftrId] * eigenVectors[compId][ftrId]
        squaredLoadings.append(loadings)

    print ('squaredLoadings', squaredLoadings)
    return squaredLoadings

@app.route('/pca_random')
def pca_random():
    print('in pca_random')
    data_columns = []
    try:
        global random_samples
        global imp_ftrs
        pca_data = PCA(n_components=2)
        X = random_samples
        pca_data.fit(X)
        X = pca_data.transform(X)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 9):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]

        data_columns['clusterid'] = data_csv['kcluster'][:samplesize]

    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr

@app.route('/pca_adaptive')
def pca_adaptive():
    print("pca adaptive");
    data_columns = []
    try:
        global adaptive_samples
        global imp_ftrs
        X = adaptive_samples[ftrs]
        pca_data = PCA(n_components=2)
        pca_data.fit(X)
        X = pca_data.transform(X)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 9):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]
        data_columns['clusterid'] = np.nan
        x = 0
        for index, row in adaptive_samples.iterrows():
            data_columns['clusterid'][x] = row['kcluster']
            x = x + 1


    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr


@app.route('/mds_euclidean_random')
def mds_euclidean_random():
    data_columns = []
    try:
        global random_samples
        global imp_ftrs
        mds_data = manifold.MDS(n_components=2, dissimilarity='precomputed')
        similarity = pairwise_distances(random_samples, metric='euclidean')
        X = mds_data.fit_transform(similarity)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 3):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]
        data_columns['clusterid'] = data_csv['kcluster'][:samplesize]
    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr


@app.route('/mds_euclidean_adaptive')
def mds_euclidean_adaptive():
    data_columns = []
    try:
        global adaptive_samples
        global imp_ftrs
        mds_data = manifold.MDS(n_components=2, dissimilarity='precomputed')
        X = adaptive_samples[ftrs]
        similarity = pairwise_distances(X, metric='euclidean')
        X = mds_data.fit_transform(similarity)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 3):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]

        data_columns['clusterid'] = np.nan
        x = 0
        for index, row in adaptive_samples.iterrows():
            data_columns['clusterid'][x] = row['kcluster']
            x = x + 1
    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr


@app.route('/mds_correlation_random')
def mds_correlation_random():
    data_columns = []
    try:
        global random_samples
        global imp_ftrs
        mds_data = manifold.MDS(n_components=2, dissimilarity='precomputed')
        similarity = pairwise_distances(random_samples, metric='correlation')
        X = mds_data.fit_transform(similarity)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 9):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]
        data_columns['clusterid'] = data_csv['kcluster'][:samplesize]
    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr


@app.route('/mds_correlation_adaptive')
def mds_correlation_adaptive():
    data_columns = []
    try:
        global adaptive_samples
        global imp_ftrs
        mds_data = manifold.MDS(n_components=2, dissimilarity='precomputed')
        X = adaptive_samples[ftrs]
        similarity = pairwise_distances(X, metric='correlation')
        X = mds_data.fit_transform(similarity)
        data_columns = pandas.DataFrame(X)
        for i in range(0, 9):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]

        data_columns['clusterid'] = np.nan
        x = 0
        for index, row in adaptive_samples.iterrows():
            data_columns['clusterid'][x] = row['kcluster']
            x = x + 1
    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr


@app.route('/scatter_matrix_random')
def scatter_matrix_random():
    try:
        global random_samples
        global imp_ftrs
        data_columns = pandas.DataFrame()
        for i in range(0, 3):
            data_columns[ftrs[imp_ftrs[i]]] = data_csv_original[ftrs[imp_ftrs[i]]][:samplesize]

        data_columns['clusterid'] = data_csv['kcluster'][:samplesize]
    except:
        e = sys.exc_info()[0]
        print(e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr

@app.route('/scatter_matrix_adaptive')
def scatter_matrix_adaptive():
    try:
        global imp_ftrs
        data_columns = pandas.DataFrame()
        for i in range(0, 3):
            data_columns[ftrs[imp_ftrs[i]]] = adaptive_samples[ftrs[imp_ftrs[i]]][:samplesize]

        data_columns['clusterid'] = np.nan
        for index, row in adaptive_samples.iterrows():
            data_columns['clusterid'][index] = row['kcluster']
        data_columns = data_columns.reset_index(drop=True)
    except:
        e = sys.exc_info()[0]
        print (e)
    jstr = json.dumps(data_columns,
                      default=lambda df: json.loads(df.to_json()))
    newresult = json.loads(jstr)
    ##data_columns=data_columns.to_json()
    return jstr

clustering()
random_sampling()
adaptive_sampling()
squared_loadings = plot_intrinsic_dimensionality_pca(data, 10)
imp_ftrs = sorted(range(len(squared_loadings)), key=lambda k: squared_loadings[k], reverse=True)

if __name__ == "__main__":
    app.run("localhost", 6666,debug=True)