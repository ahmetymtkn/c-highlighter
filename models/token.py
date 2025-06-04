from enum import Enum 

class TokenType(Enum):  # Token türlerini tanımlayan Enum sınıfı
    """C Dili için token türleri"""
    KEYWORD = "KEYWORD"  # Anahtar kelimeler
    IDENTIFIER = "IDENTIFIER"  # Tanımlayıcılar
    NUMBER = "NUMBER"  # Sayılar
    STRING = "STRING"  # Metin dizileri
    CHAR = "CHAR"  # Tek karakterler
    OPERATOR = "OPERATOR"  # Operatörler
    SEPARATOR = "SEPARATOR"  # Ayırıcılar
    COMMENT = "COMMENT"  # Yorumlar
    PREPROCESSOR = "PREPROCESSOR"  # Önişlemci direktifleri
    WHITESPACE = "WHITESPACE"  # Boşluklar
    ERROR = "ERROR"  # Hatalı token'lar
    EOF = "EOF"  # Dosya sonu

class Token:  # Token nesnesini temsil eden sınıf
    def __init__(self, type, value, line, column, position):  # Token oluşturucu
        self.type = type  # Token türü
        self.value = value  # Token içeriği
        self.line = line  # Satır numarası
        self.column = column  # Sütun numarası
        self.position = position  # Kod içindeki pozisyon

    def __repr__(self):  # Token'ın string temsili
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"  # Token bilgilerini döndürür