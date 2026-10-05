import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

SAMPLE_SIZE = 300
RANDOM_SEED = 42


# Membuat data contoh (dummy) rumah beserta fitur-fitur yang memengaruhi harganya
def generate_sample_data(sample_size, seed):
    rng = np.random.default_rng(seed)

    sqft = rng.normal(1800, 500, sample_size).clip(500, 4000)
    bedrooms = rng.integers(1, 6, sample_size)
    bathrooms = rng.integers(1, 4, sample_size)
    age_years = rng.integers(0, 50, sample_size)
    distance_to_city_km = rng.uniform(1, 30, sample_size)

    noise = rng.normal(0, 25000, sample_size)
    price = (
        50000
        + (sqft * 120)
        + (bedrooms * 8000)
        + (bathrooms * 6000)
        - (age_years * 500)
        - (distance_to_city_km * 1500)
        + noise
    )
    price = price.clip(50000, None)

    return pd.DataFrame({
        "sqft": sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age_years,
        "distance_to_city_km": distance_to_city_km,
        "price": price,
    })


# Menampilkan heatmap korelasi antar seluruh fitur numerik dalam dataset
def plot_correlation_heatmap(data: pd.DataFrame):
    sns.set_theme(style="white")

    plt.figure(figsize=(8, 6))
    correlation = data.corr()
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm", center=0)

    plt.title("Korelasi Antar Fitur Rumah")
    plt.tight_layout()
    plt.show()


# Menampilkan scatter plot harga rumah terhadap luas bangunan beserta garis regresi
def plot_price_vs_sqft(data: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    sns.regplot(
        data=data, x="sqft", y="price",
        scatter_kws={"alpha": 0.5, "color": "#3a6ea5"},
        line_kws={"color": "#e63946"},
    )

    plt.title("Harga Rumah terhadap Luas Bangunan")
    plt.xlabel("Luas Bangunan (sqft)")
    plt.ylabel("Harga Rumah")
    plt.tight_layout()
    plt.show()


# Menampilkan boxplot distribusi harga rumah berdasarkan jumlah kamar tidur
def plot_price_by_bedrooms(data: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, x="bedrooms", y="price", hue="bedrooms", palette="viridis", legend=False)

    plt.title("Distribusi Harga Rumah Berdasarkan Jumlah Kamar Tidur")
    plt.xlabel("Jumlah Kamar Tidur")
    plt.ylabel("Harga Rumah")
    plt.tight_layout()
    plt.show()


def main():
    data = generate_sample_data(SAMPLE_SIZE, RANDOM_SEED)
    print(data.describe())

    plot_correlation_heatmap(data)
    plot_price_vs_sqft(data)
    plot_price_by_bedrooms(data)


if __name__ == "__main__":
    main()