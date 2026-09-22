import random

# Kumpulan kata yang digunakan untuk membangun nama brand
PREFIXES = [
    "Neo", "Zen", "Lumi", "Nova", "Prime", "Aero", "Bright",
    "Quantum", "Pulse", "Vivid", "Echo", "Cloud", "Swift", "Terra"
]

SUFFIXES = [
    "ify", "ly", "hub", "wave", "nest", "spark", "works",
    "labs", "verse", "flow", "core", "loop", "grove", "sync"
]

CONNECTORS = ["", "-", ""]  # sesekali menambahkan tanda hubung agar bervariasi

def clean_keyword(keyword: str) -> str:
    return keyword.strip().capitalize()


def generate_names(keyword: str, count: int = 10) -> list:
    keyword = clean_keyword(keyword)
    names = set()

    attempts = 0
    max_attempts = count * 10  # menghindari perulangan tak terbatas

    while len(names) < count and attempts < max_attempts:
        attempts += 1
        pattern = random.choice([1, 2, 3, 4])

        if pattern == 1:
            # Prefix + Keyword
            name = f"{random.choice(PREFIXES)}{keyword}"
        elif pattern == 2:
            # Keyword + Suffix
            name = f"{keyword}{random.choice(SUFFIXES)}"
        elif pattern == 3:
            # Prefix + Keyword + Suffix
            name = f"{random.choice(PREFIXES)}{keyword}{random.choice(SUFFIXES)}"
        else:
            # Keyword dengan tanda hubung + Suffix
            connector = random.choice(CONNECTORS)
            name = f"{keyword}{connector}{random.choice(SUFFIXES)}"

        names.add(name)

    return list(names)


def main():
    print("=" * 22)
    print(" PEMBUAT NAMA BRAND")
    print("=" * 22)

    keyword = input("\nMasukkan kata kunci terkait bisnis/produk Anda: ")
    while not keyword.strip():
        keyword = input("Mohon masukkan kata kunci yang valid: ")

    try:
        count = int(input("Berapa banyak ide nama yang Anda inginkan? (default 10): ") or 10)
    except ValueError:
        count = 10

    results = generate_names(keyword, count)

    print(f"\nBerikut {len(results)} ide nama brand untuk '{keyword.strip()}':\n")
    for i, name in enumerate(results, start=1):
        print(f"{i}. {name}")

    print("\nSemoga sukses membangun brand Anda!")


if __name__ == "__main__":
    main()
