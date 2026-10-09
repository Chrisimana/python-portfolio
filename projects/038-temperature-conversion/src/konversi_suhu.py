class KonversiSuhu:
    @staticmethod
    def celsius_ke_fahrenheit(celsius):
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_ke_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_ke_reamur(celsius):
        return celsius * 4/5
    
    @staticmethod
    def reamur_ke_celsius(reamur):
        return reamur * 5/4
    
    @staticmethod
    def celsius_ke_kelvin(celsius):
        return celsius + 273.15
    
    @staticmethod
    def kelvin_ke_celsius(kelvin):
        return kelvin - 273.15
    
    @staticmethod
    def fahrenheit_ke_reamur(fahrenheit):
        celsius = KonversiSuhu.fahrenheit_ke_celsius(fahrenheit)
        return KonversiSuhu.celsius_ke_reamur(celsius)
    
    @staticmethod
    def reamur_ke_fahrenheit(reamur):
        celsius = KonversiSuhu.reamur_ke_celsius(reamur)
        return KonversiSuhu.celsius_ke_fahrenheit(celsius)
    
    @staticmethod
    def fahrenheit_ke_kelvin(fahrenheit):
        celsius = KonversiSuhu.fahrenheit_ke_celsius(fahrenheit)
        return KonversiSuhu.celsius_ke_kelvin(celsius)
    
    @staticmethod
    def kelvin_ke_fahrenheit(kelvin):
        celsius = KonversiSuhu.kelvin_ke_celsius(kelvin)
        return KonversiSuhu.celsius_ke_fahrenheit(celsius)
    
    @staticmethod
    def reamur_ke_kelvin(reamur):
        celsius = KonversiSuhu.reamur_ke_celsius(reamur)
        return KonversiSuhu.celsius_ke_kelvin(celsius)
    
    @staticmethod
    def kelvin_ke_reamur(kelvin):
        celsius = KonversiSuhu.kelvin_ke_celsius(kelvin)
        return KonversiSuhu.celsius_ke_reamur(celsius)
    
    @staticmethod
    def konversi_suhu(nilai, dari, ke):
        # Dictionary untuk menyimpan semua fungsi konversi
        konversi_fungsi = {
            ('C', 'F'): KonversiSuhu.celsius_ke_fahrenheit,
            ('C', 'R'): KonversiSuhu.celsius_ke_reamur,
            ('C', 'K'): KonversiSuhu.celsius_ke_kelvin,
            ('F', 'C'): KonversiSuhu.fahrenheit_ke_celsius,
            ('F', 'R'): KonversiSuhu.fahrenheit_ke_reamur,
            ('F', 'K'): KonversiSuhu.fahrenheit_ke_kelvin,
            ('R', 'C'): KonversiSuhu.reamur_ke_celsius,
            ('R', 'F'): KonversiSuhu.reamur_ke_fahrenheit,
            ('R', 'K'): KonversiSuhu.reamur_ke_kelvin,
            ('K', 'C'): KonversiSuhu.kelvin_ke_celsius,
            ('K', 'F'): KonversiSuhu.kelvin_ke_fahrenheit,
            ('K', 'R'): KonversiSuhu.kelvin_ke_reamur,
        }
        
        # Jika dari dan ke sama, kembalikan nilai asli
        if dari == ke:
            return nilai
        
        # Cari fungsi konversi yang sesuai
        fungsi_konversi = konversi_fungsi.get((dari, ke))
        if fungsi_konversi:
            return fungsi_konversi(nilai)
        else:
            raise ValueError(f"Konversi dari {dari} ke {ke} tidak didukung")