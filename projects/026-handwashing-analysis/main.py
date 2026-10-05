import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

RANDOM_SEED = 42
HANDWASHING_START = pd.Timestamp("1847-06-01")  # bulan saat kebijakan cuci tangan diterapkan


# Membuat data bulanan contoh (dummy) yang meniru kasus historis Dr. Semmelweis
# angka kematian ibu melahirkan di Klinik 1 menurun drastis setelah kebijakan
# cuci tangan diterapkan pada pertengahan 1847
def generate_sample_data(seed):
    rng = np.random.default_rng(seed)
    date_range = pd.date_range(start="1841-01-01", end="1849-12-01", freq="MS")

    records = []
    for current_date in date_range:
        births = rng.integers(200, 400)

        if current_date < HANDWASHING_START:
            death_rate = rng.uniform(0.08, 0.16)  # sebelum cuci tangan, angka kematian tinggi
        else:
            death_rate = rng.uniform(0.01, 0.04)  # setelah cuci tangan, angka kematian menurun

        deaths = int(births * death_rate)
        records.append({"date": current_date, "births": births, "deaths": deaths})

    data = pd.DataFrame(records)
    data["death_rate_percent"] = (data["deaths"] / data["births"]) * 100

    return data


# Menampilkan grafik tren angka kematian bulanan, dengan garis penanda
def plot_death_rate_trend(data: pd.DataFrame):
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(11, 6))
    sns.lineplot(data=data, x="date", y="death_rate_percent", color="#3a6ea5")

    plt.axvline(HANDWASHING_START, color="#e63946", linestyle="--", label="Kebijakan Cuci Tangan Dimulai")

    plt.title("Tren Angka Kematian Ibu Melahirkan Sebelum dan Sesudah Kebijakan Cuci Tangan")
    plt.xlabel("Tanggal")
    plt.ylabel("Angka Kematian (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


# Menampilkan perbandingan rata-rata angka kematian sebelum vs sesudah kebijakan dalam bentuk boxplot
def plot_before_after_comparison(data: pd.DataFrame):
    data = data.copy()
    data["period"] = np.where(data["date"] < HANDWASHING_START, "Sebelum Cuci Tangan", "Sesudah Cuci Tangan")

    plt.figure(figsize=(7, 6))
    sns.boxplot(data=data, x="period", y="death_rate_percent", hue="period", palette="Set2", legend=False)

    plt.title("Perbandingan Angka Kematian: Sebelum vs Sesudah Kebijakan Cuci Tangan")
    plt.xlabel("")
    plt.ylabel("Angka Kematian (%)")
    plt.tight_layout()
    plt.show()


def main():
    data = generate_sample_data(RANDOM_SEED)

    avg_before = data[data["date"] < HANDWASHING_START]["death_rate_percent"].mean()
    avg_after = data[data["date"] >= HANDWASHING_START]["death_rate_percent"].mean()

    print(f"Rata-rata angka kematian sebelum kebijakan: {avg_before:.2f}%")
    print(f"Rata-rata angka kematian sesudah kebijakan: {avg_after:.2f}%")

    plot_death_rate_trend(data)
    plot_before_after_comparison(data)


if __name__ == "__main__":
    main()