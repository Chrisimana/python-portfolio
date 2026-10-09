from utils.constants import COLORS

def apply_styles():
    return f"""
        QMainWindow {{
            background-color: {COLORS['bg']};
        }}
        
        QPushButton {{
            background-color: {COLORS['button']};
            color: white;
            border: none;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS['button_hover']};
        }}
        
        QLabel {{
            color: {COLORS['text']};
            font-size: 16px;
        }}
        
        QLabel#title {{
            font-size: 24px;
            font-weight: bold;
            margin: 20px;
        }}
        
        QPushButton#cell {{
            background-color: {COLORS['board']};
            color: {COLORS['text']};
            font-size: 32px;
            font-weight: bold;
            border: 2px solid {COLORS['line']};
            border-radius: 10px;
            padding: 20px;
        }}
        
        QPushButton#cell:hover {{
            background-color: {COLORS['line']};
        }}
        
        QPushButton#reset {{
            background-color: {COLORS['button']};
            font-size: 16px;
            padding: 12px;
            min-width: 150px;
        }}
        
        QComboBox {{
            background-color: white;
            border: 2px solid {COLORS['line']};
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            min-width: 150px;
        }}
    """