from enum import Enum
from typing import List, Optional
from models.token import Token, TokenType

class LexicalState(Enum):
    """Lexical analyzer için durumlar"""
    START = "START"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    CHAR = "CHAR"
    COMMENT_SINGLE = "COMMENT_SINGLE"
    COMMENT_MULTI = "COMMENT_MULTI"
    OPERATOR = "OPERATOR"
    PREPROCESSOR = "PREPROCESSOR"
    ERROR = "ERROR"

class LexicalAnalyzer:
    """State Diagram & Program Implementation yaklaşımı ile Lexical Analyzer"""
    
    def __init__(self):
        # C Dili anahtar kelimeleri
        self.keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }
        
        # Operatörler
        self.operators = {
            '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
            '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
            '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>='
        }
        
        # Ayırıcılar
        self.separators = {'(', ')', '{', '}', '[', ']', ';', ',', '.', ':', '?'}
        
        self.reset()
    
    def reset(self):
        """Analyzer'ı sıfırla"""
        self.input_text = ""
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = None
        self.state = LexicalState.START
        self.tokens = []
    
    def analyze(self, text: str) -> List[Token]:
        """Metni analiz et ve token listesi döndür"""
        self.reset()
        self.input_text = text
        self.position = 0
        self.line = 1
        self.column = 1
        
        if len(text) > 0:
            self.current_char = text[0]
        
        while self.position < len(self.input_text):
            self.process_current_state()
        
        # EOF token ekle
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.position))
        return self.tokens
    
    def process_current_state(self):
        """Mevcut duruma göre işlem yap"""
        if self.state == LexicalState.START:
            self.handle_start_state()
        elif self.state == LexicalState.IDENTIFIER:
            self.handle_identifier_state()
        elif self.state == LexicalState.NUMBER:
            self.handle_number_state()
        elif self.state == LexicalState.STRING:
            self.handle_string_state()
        elif self.state == LexicalState.CHAR:
            self.handle_char_state()
        elif self.state == LexicalState.COMMENT_SINGLE:
            self.handle_single_comment_state()
        elif self.state == LexicalState.COMMENT_MULTI:
            self.handle_multi_comment_state()
        elif self.state == LexicalState.PREPROCESSOR:
            self.handle_preprocessor_state()
        elif self.state == LexicalState.OPERATOR:
            self.handle_operator_state()
    
    def handle_start_state(self):
        """Başlangıç durumu işleyicisi"""
        if self.current_char is None:
            return
        
        if self.current_char.isspace():
            self.skip_whitespace()
        elif self.current_char.isalpha() or self.current_char == '_':
            self.state = LexicalState.IDENTIFIER
        elif self.current_char.isdigit():
            self.state = LexicalState.NUMBER
        elif self.current_char == '"':
            self.state = LexicalState.STRING
        elif self.current_char == "'":
            self.state = LexicalState.CHAR
        elif self.current_char == '#':
            self.state = LexicalState.PREPROCESSOR
        elif self.current_char == '/' and self.peek() == '/':
            self.state = LexicalState.COMMENT_SINGLE
        elif self.current_char == '/' and self.peek() == '*':
            self.state = LexicalState.COMMENT_MULTI
        elif self.current_char in self.separators:
            self.create_token(TokenType.SEPARATOR, self.current_char)
            self.advance()
        else:
            self.state = LexicalState.OPERATOR
    
    def handle_identifier_state(self):
        """Tanımlayıcı durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        identifier = ""
        
        while (self.current_char and 
               (self.current_char.isalnum() or self.current_char == '_')):
            identifier += self.current_char
            self.advance()
        
        # Anahtar kelime kontrolü
        token_type = TokenType.KEYWORD if identifier in self.keywords else TokenType.IDENTIFIER
        self.tokens.append(Token(token_type, identifier, start_line, start_col, start_pos))
        self.state = LexicalState.START
    
    def handle_number_state(self):
        """Sayı durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        number = ""
        has_dot = False
        
        while self.current_char and (self.current_char.isdigit() or 
                                   (self.current_char == '.' and not has_dot)):
            if self.current_char == '.':
                has_dot = True
            number += self.current_char
            self.advance()
        
        self.tokens.append(Token(TokenType.NUMBER, number, start_line, start_col, start_pos))
        self.state = LexicalState.START
    
    def handle_string_state(self):
        """String durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        string_val = '"'
        self.advance()  # İlk " karakterini atla
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\' and self.peek():
                string_val += self.current_char
                self.advance()
                if self.current_char:
                    string_val += self.current_char
                    self.advance()
            else:
                string_val += self.current_char
                self.advance()
        
        if self.current_char == '"':
            string_val += self.current_char
            self.advance()
            self.tokens.append(Token(TokenType.STRING, string_val, start_line, start_col, start_pos))
        else:
            # Hata: String kapatılmamış
            self.tokens.append(Token(TokenType.ERROR, string_val, start_line, start_col, start_pos))
        
        self.state = LexicalState.START
    
    def handle_char_state(self):
        """Karakter durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        char_val = "'"
        self.advance()  # İlk ' karakterini atla
        
        char_count = 0
        while self.current_char and self.current_char != "'" and char_count < 2:
            if self.current_char == '\\' and self.peek():
                char_val += self.current_char
                self.advance()
                if self.current_char:
                    char_val += self.current_char
                    self.advance()
            else:
                char_val += self.current_char
                self.advance()
            char_count += 1
        
        if self.current_char == "'":
            char_val += self.current_char
            self.advance()
            self.tokens.append(Token(TokenType.CHAR, char_val, start_line, start_col, start_pos))
        else:
            self.tokens.append(Token(TokenType.ERROR, char_val, start_line, start_col, start_pos))
        
        self.state = LexicalState.START
    
    def handle_single_comment_state(self):
        """Tek satır yorum durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        comment = ""
        
        while self.current_char and self.current_char != '\n':
            comment += self.current_char
            self.advance()
        
        self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col, start_pos))
        self.state = LexicalState.START
    
    def handle_multi_comment_state(self):
        """Çok satır yorum durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        comment = ""
        
        # /* başlangıcını ekle
        comment += self.current_char  # /
        self.advance()
        comment += self.current_char  # *
        self.advance()
        
        while self.current_char:
            if self.current_char == '*' and self.peek() == '/':
                comment += self.current_char
                self.advance()
                comment += self.current_char
                self.advance()
                break
            else:
                comment += self.current_char
                self.advance()
        
        self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col, start_pos))
        self.state = LexicalState.START
    
    def handle_preprocessor_state(self):
        """Preprocessor durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        preprocessor = ""
        
        while self.current_char and self.current_char != '\n':
            preprocessor += self.current_char
            self.advance()
        
        self.tokens.append(Token(TokenType.PREPROCESSOR, preprocessor, start_line, start_col, start_pos))
        self.state = LexicalState.START
    
    def handle_operator_state(self):
        """Operatör durumu işleyicisi"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        
        # İki karakterli operatörleri kontrol et
        two_char = self.current_char + (self.peek() or '')
        if two_char in self.operators:
            self.tokens.append(Token(TokenType.OPERATOR, two_char, start_line, start_col, start_pos))
            self.advance()
            self.advance()
        elif self.current_char in self.operators or self.current_char in "+-*/%=<>!&|^~":
            self.tokens.append(Token(TokenType.OPERATOR, self.current_char, start_line, start_col, start_pos))
            self.advance()
        else:
            # Bilinmeyen karakter - hata
            self.tokens.append(Token(TokenType.ERROR, self.current_char, start_line, start_col, start_pos))
            self.advance()
        
        self.state = LexicalState.START
    
    def advance(self):
        """Bir sonraki karaktere geç"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.position += 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
        else:
            self.current_char = None
    
    def peek(self) -> Optional[str]:
        """Bir sonraki karakteri döndür (position'ı değiştirmeden)"""
        peek_pos = self.position + 1
        if peek_pos < len(self.input_text):
            return self.input_text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """Boşlukları atla"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def create_token(self, token_type: TokenType, value: str):
        """Token oluştur"""
        self.tokens.append(Token(token_type, value, self.line, self.column, self.position))