class BMICalculator:
    def __init__(self):
        pass
    
    # Menghitung BMI berdasarkan berat dan tinggi
    def calculate_bmi(self, berat, tinggi):
        if tinggi <= 0:
            raise ValueError("Tinggi badan harus lebih dari 0")
        
        bmi = berat / (tinggi ** 2)
        return round(bmi, 2)
    
    # Mendapatkan kategori BMI
    def get_kategori(self, bmi):
        if bmi < 18.5:
            return "Kekurangan berat badan", "underweight"
        elif 18.5 <= bmi < 25:
            return "Berat badan normal", "normal"
        elif 25 <= bmi < 30:
            return "Kelebihan berat badan", "overweight"
        else:
            return "Obesitas", "obese"
    
    # Menghitung rentang berat badan ideal
    def get_berat_ideal_range(self, tinggi):
        if tinggi <= 0:
            raise ValueError("Tinggi badan harus lebih dari 0")
        
        bawah = 18.5 * (tinggi ** 2)
        atas = 25 * (tinggi ** 2)
        return round(bawah, 2), round(atas, 2)