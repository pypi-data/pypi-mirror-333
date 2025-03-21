# الگوریتم خوشه‌بندی بهبود یافته SONSC+ با شاخص ISI برای داده‌های MNIST و CIFAR-10

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.datasets import mnist, cifar10

# Compute Cohesion and Separation
def compute_cohesion_separation(X, labels):
    unique_labels = np.unique(labels)
    k = len(unique_labels)
    if k < 2:
        return np.nan, np.nan

    cluster_centers = np.array([X[labels == label].mean(axis=0) for label in unique_labels])

    cohesion = np.mean([
        np.mean(np.linalg.norm(X[labels == label] - cluster_centers[i], axis=1))
        for i, label in enumerate(unique_labels)
    ])

    separation = np.mean([np.linalg.norm(cluster_centers[i] - cluster_centers[j])
                          for i in range(k) for j in range(i + 1, k)])

    return cohesion, separation

# ISI computation function
def compute_isi(cohesion, separation):
    return (separation ** 2) / (cohesion + separation ** 2) if (cohesion + separation ** 2) != 0 else np.nan

# SONSC+ algorithm implementation
def sonsc_isi(X, k_values):
    results = []
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        cohesion, separation = compute_cohesion_separation(X, labels)
        isi_score = compute_isi(cohesion, separation)
        results.append({
            "k": k,
            "Cohesion": cohesion,
            "Separation": separation,
            "ISI": np.clip(isi_score, 0, 1)
        })
    return pd.DataFrame(results)

# Main execution block
if __name__ == "__main__":
    # MNIST dataset
    from tensorflow.keras.datasets import mnist, cifar10
    (X_mnist_train, _), (_, _) = mnist.load_data()
    X_mnist = X_mnist_train.reshape(-1, 784)
    X_mnist = StandardScaler().fit_transform(X_mnist)
    X_mnist_subset = X_mnist[:2000]

    # CIFAR-10 dataset
    (X_cifar_train, _), (_, _) = cifar10.load_data()
    X_cifar = X_cifar_train.reshape(X_cifar_train.shape[0], -1)
    X_cifar = StandardScaler().fit_transform(X_cifar)
    X_cifar_subset = X_cifar[:2000]

    k_values = range(2, 15)

    # MNIST results
    mnist_results_df = sonsc_isi(X_mnist_subset, k_values)
    mnist_results_df.to_csv("mnist_sonsc_isi_results.csv", index=False)
    print("MNIST Results:\n", mnist_results_df)

    # CIFAR-10 results
    cifar_results_df = sonsc_isi(X_cifar_subset, k_values)
    cifar_results_df.to_csv("cifar10_sonsc_isi_results.csv", index=False)
    print("CIFAR-10 Results:\n", cifar_results_df)

    # Plotting Cohesion and Separation for MNIST
    plt.figure(figsize=(12, 6))
    plt.plot(mnist_results_df["k"], mnist_results_df["Cohesion"], marker='o', label='Cohesion', color='red')
    plt.plot(mnist_results_df["k"], mnist_results_df["Separation"], marker='o', linestyle='--', label='Separation', color='green')
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Score")
    plt.title("Cohesion and Separation for MNIST")
    plt.legend()
    plt.grid()
    plt.show()

    # Plotting ISI for MNIST
    plt.figure(figsize=(12, 6))
    plt.plot(mnist_results_df["k"], mnist_results_df["ISI"], marker='o', color='blue')
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("ISI")
    plt.title("ISI for MNIST")
    plt.grid()
    plt.show()
