import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

SAMPLE_SIZE = 100
RANDOM_SEED = 42


# Membuat data contoh (dummy) yang merepresentasikan jam belajar vs nilai ujian
def generate_sample_data(sample_size, seed):
    rng = np.random.default_rng(seed)

    hours_studied = rng.uniform(0, 10, sample_size)
    noise = rng.normal(0, 7, sample_size)
    exam_score = 40 + (hours_studied * 5.5) + noise
    exam_score = np.clip(exam_score, 0, 100)

    return pd.DataFrame({
        "hours_studied": hours_studied,
        "exam_score": exam_score,
    })


# Menampilkan scatter plot beserta garis regresi linear menggunakan Seaborn
def plot_regression(data: pd.DataFrame):
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 6))
    sns.regplot(
        data=data,
        x="hours_studied",
        y="exam_score",
        scatter_kws={"alpha": 0.6, "color": "#3a6ea5"},
        line_kws={"color": "#e63946"},
    )

    plt.title("Hubungan Jam Belajar terhadap Nilai Ujian")
    plt.xlabel("Jam Belajar per Hari")
    plt.ylabel("Nilai Ujian")
    plt.tight_layout()
    plt.show()


def main():
    data = generate_sample_data(SAMPLE_SIZE, RANDOM_SEED)
    print(data.describe())
    plot_regression(data)


if __name__ == "__main__":
    main()