class DiskonCalculator:
    @staticmethod

    # Menghitung harga setelah diskon
    def hitung_diskon(harga_asal, diskon):
        if diskon > 100:
            raise ValueError("Diskon tidak boleh lebih dari 100%")
        if diskon < 0:
            raise ValueError("Diskon tidak boleh bernilai negatif")
        if harga_asal < 0:
            raise ValueError("Harga asal tidak boleh negatif")
        
        harga_diskon = harga_asal - (harga_asal * diskon / 100)
        return round(harga_diskon, 2)
    
    @staticmethod
    # Validasi input harga
    def validasi_input_harga(harga_str):
        if not harga_str:
            return False, "Harga tidak boleh kosong"
        
        try:
            harga = float(harga_str)
            if harga <= 0:
                return False, "Harga harus lebih besar dari 0"
            return True, harga
        except ValueError:
            return False, "Harga harus berupa angka"
    
    @staticmethod
    # Validasi input diskon
    def validasi_input_diskon(diskon_str):
        if not diskon_str:
            return False, "Diskon tidak boleh kosong"
        
        try:
            diskon = float(diskon_str)
            if diskon < 0:
                return False, "Diskon tidak boleh negatif"
            if diskon > 100:
                return False, "Diskon tidak boleh lebih dari 100%"
            return True, diskon
        except ValueError:
            return False, "Diskon harus berupa angka"