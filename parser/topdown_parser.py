from typing import List, Optional
from parser.parse_tree import ParseNode
from lexer.lexical_analyzer import Token, TokenType

class TopDownParser:
    """Yukarıdan-Aşağı (Özyinelemeli İniş) Parser"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.WHITESPACE]
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        self.errors = []
    
    def parse(self) -> ParseNode:
        """Ana parse fonksiyonu"""
        try:
            return self.parse_program()
        except Exception as e:
            self.errors.append(f"Parse hatası: {str(e)}")
            return ParseNode("ERROR")
    
    def parse_program(self) -> ParseNode:
        """program -> statement_list"""
        node = ParseNode("program")
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                node.add_child(stmt)
        
        return node
    
    def parse_statement(self) -> Optional[ParseNode]:
        """statement -> declaration | function_definition | assignment | if_stmt | while_stmt | for_stmt | expression_stmt"""
        if not self.current_token:
            return None

        # Önişlemci direktifi
        if self.current_token.type == TokenType.PREPROCESSOR:
            return self.parse_preprocessor()

        # Değişken veya fonksiyon tanımlama/bildirimi
        if (self.current_token.type == TokenType.KEYWORD and 
            self.current_token.value in ['int', 'char', 'float', 'double', 'void']):
            # İleriye bak: IDENTIFIER + '(' ise fonksiyon tanımı/bildirimi
            if (self.current_token_index + 2 < len(self.tokens) and
                self.tokens[self.current_token_index + 1].type == TokenType.IDENTIFIER and
                self.tokens[self.current_token_index + 2].type == TokenType.SEPARATOR and
                self.tokens[self.current_token_index + 2].value == '('):
                return self.parse_function_definition()
            else:
                return self.parse_declaration()

        # Kontrol yapıları
        if self.current_token.type == TokenType.KEYWORD:
            if self.current_token.value == 'if':
                return self.parse_if_statement()
            elif self.current_token.value == 'while':
                return self.parse_while_statement()
            elif self.current_token.value == 'for':
                return self.parse_for_statement()
            elif self.current_token.value == 'return':
                return self.parse_return_statement()
        
        # Atama veya ifade
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_assignment_or_expression()
        
        # Blok ifadesi
        if (self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == '{'):
            return self.parse_block()
        
        # Bilinmeyen ifadeleri atla
        self.advance()
        return None
    
    def parse_preprocessor(self) -> ParseNode:
        """preprocessor -> PREPROCESSOR"""
        node = ParseNode("preprocessor")
        if self.current_token.type == TokenType.PREPROCESSOR:
            child = ParseNode(self.current_token.value)
            child.token = self.current_token
            node.add_child(child)
            self.advance()
        return node
    
    def parse_declaration(self) -> ParseNode:
        """declaration -> type IDENTIFIER [= expression] ;"""
        node = ParseNode("declaration")
        
        # Tip
        if (self.current_token.type == TokenType.KEYWORD and 
            self.current_token.value in ['int', 'char', 'float', 'double', 'void']):
            type_node = ParseNode(self.current_token.value)
            type_node.token = self.current_token
            node.add_child(type_node)
            self.advance()
        
        # Tanımlayıcı
        if self.current_token.type == TokenType.IDENTIFIER:
            id_node = ParseNode(self.current_token.value)
            id_node.token = self.current_token
            node.add_child(id_node)
            self.advance()
        
        # İsteğe bağlı başlangıç değeri
        if (self.current_token and self.current_token.type == TokenType.OPERATOR and 
            self.current_token.value == '='):
            self.advance()  # =
            expr = self.parse_expression()
            if expr:
                node.add_child(expr)
        
        # Noktalı virgül
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == ';'):
            self.advance()
        else:
            # Hata mesajı ve bir sonraki token'a geç
            self.errors.append(f"Beklenen ';' satır {self.current_token.line if self.current_token else 'EOF'}")
            if self.current_token:
                self.advance()
        return node
    
    def parse_function_definition(self) -> ParseNode:
        """function_definition -> type IDENTIFIER ( [params] ) block"""
        node = ParseNode("function_definition")
        # Tip
        if (self.current_token.type == TokenType.KEYWORD and 
            self.current_token.value in ['int', 'char', 'float', 'double', 'void']):
            type_node = ParseNode(self.current_token.value)
            type_node.token = self.current_token
            node.add_child(type_node)
            self.advance()
        # Tanımlayıcı
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            id_node = ParseNode(self.current_token.value)
            id_node.token = self.current_token
            node.add_child(id_node)
            self.advance()
        # (
        if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == '(':
            self.advance()
            # Parametreleri parse et (basit: ')' ye kadar atla)
            params_node = ParseNode("params")
            while self.current_token and not (self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ')'):
                # İsteğe bağlı olarak, burada parametre bildirimlerini parse et
                param_token = self.current_token
                param_node = ParseNode(param_token.value)
                param_node.token = param_token
                params_node.add_child(param_node)
                self.advance()
            node.add_child(params_node)
            if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ')':
                self.advance()
        # Blok
        if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == '{':
            block = self.parse_block()
            if block:
                node.add_child(block)
        else:
            self.errors.append(f"Beklenen '{{' satır {self.current_token.line if self.current_token else 'EOF'}")
        return node
    
    def parse_assignment_or_expression(self) -> ParseNode:
        """assignment -> IDENTIFIER = expression ; | expression ;"""
        # Atama olup olmadığını görmek için ileriye bak
        if (self.current_token_index + 1 < len(self.tokens) and
            self.tokens[self.current_token_index + 1].type == TokenType.OPERATOR and
            self.tokens[self.current_token_index + 1].value == '='):
            return self.parse_assignment()
        else:
            return self.parse_expression_statement()
    
    def parse_assignment(self) -> ParseNode:
        """assignment -> IDENTIFIER = expression ;"""
        node = ParseNode("assignment")
        
        # Tanımlayıcı
        if self.current_token.type == TokenType.IDENTIFIER:
            id_node = ParseNode(self.current_token.value)
            id_node.token = self.current_token
            node.add_child(id_node)
            self.advance()
        
        # =
        if (self.current_token and self.current_token.type == TokenType.OPERATOR and 
            self.current_token.value == '='):
            self.advance()
        
        # İfade
        expr = self.parse_expression()
        if expr:
            node.add_child(expr)
        
        # Noktalı virgül
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == ';'):
            self.advance()
        else:
            self.errors.append(f"Beklenen ';' satır {self.current_token.line if self.current_token else 'EOF'}")
            if self.current_token:
                self.advance()
        return node
    
    def parse_expression_statement(self) -> ParseNode:
        """expression_statement -> expression ;"""
        node = ParseNode("expression_statement")
        expr = self.parse_expression()
        if expr:
            node.add_child(expr)
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == ';'):
            self.advance()
        else:
            self.errors.append(f"Beklenen ';' satır {self.current_token.line if self.current_token else 'EOF'}")
            if self.current_token:
                self.advance()
        return node
    
    def parse_expression(self) -> ParseNode:
        """expression -> simple_expression ([comparison_op] simple_expression)*"""
        node = self.parse_simple_expression()
        
        # Karşılaştırma operatörleri desteği
        comparison_ops = ['>', '<', '>=', '<=', '==', '!=']
        while (self.current_token and self.current_token.type == TokenType.OPERATOR and 
               self.current_token.value in comparison_ops):
            op_node = ParseNode("comparison_op")
            op_node.add_child(node)
            
            op_token = ParseNode(self.current_token.value)
            op_token.token = self.current_token
            op_node.add_child(op_token)
            self.advance()
            
            right = self.parse_simple_expression()
            if right:
                op_node.add_child(right)
            
            node = op_node
        
        return node
    
    def parse_simple_expression(self) -> ParseNode:
        """simple_expression -> term ((+|-) term)*"""
        node = self.parse_term()
        
        while (self.current_token and self.current_token.type == TokenType.OPERATOR and 
               self.current_token.value in ['+', '-']):
            op_node = ParseNode("binary_op")
            op_node.add_child(node)
            
            op_token = ParseNode(self.current_token.value)
            op_token.token = self.current_token
            op_node.add_child(op_token)
            self.advance()
            
            right = self.parse_term()
            if right:
                op_node.add_child(right)
            
            node = op_node
        
        return node
    
    def parse_term(self) -> ParseNode:
        """term -> factor ((*|/) factor)*"""
        node = self.parse_factor()
        
        while (self.current_token and self.current_token.type == TokenType.OPERATOR and 
               self.current_token.value in ['*', '/']):
            op_node = ParseNode("binary_op")
            op_node.add_child(node)
            
            op_token = ParseNode(self.current_token.value)
            op_token.token = self.current_token
            op_node.add_child(op_token)
            self.advance()
            
            right = self.parse_factor()
            if right:
                op_node.add_child(right)
            
            node = op_node
        
        return node
    
    def parse_factor(self) -> ParseNode:
        """factor -> NUMBER | IDENTIFIER | STRING | CHAR | function_call | ( expression )"""
        if self.current_token.type == TokenType.NUMBER:
            node = ParseNode(self.current_token.value)
            node.token = self.current_token
            self.advance()
            return node
        elif self.current_token.type == TokenType.STRING:
            node = ParseNode(self.current_token.value)
            node.token = self.current_token
            self.advance()
            return node
        elif self.current_token.type == TokenType.CHAR:
            node = ParseNode(self.current_token.value)
            node.token = self.current_token
            self.advance()
            return node
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Fonksiyon çağrısı kontrolü: IDENTIFIER '(' ... ')'
            if (self.current_token_index + 1 < len(self.tokens) and
                self.tokens[self.current_token_index + 1].type == TokenType.SEPARATOR and
                self.tokens[self.current_token_index + 1].value == '('):
                return self.parse_function_call()
            else:
                node = ParseNode(self.current_token.value)
                node.token = self.current_token
                self.advance()
                # Tanımlayıcı sonrası hata kontrolü
                if (self.current_token and
                    self.current_token.type not in [
                        TokenType.OPERATOR, TokenType.SEPARATOR, TokenType.EOF
                    ]):
                    self.errors.append(
                        f"Beklenmeyen/tanımsız tanımlayıcı kullanımı '{node.name}' satır {node.token.line}"
                    )
                return node
        elif (self.current_token.type == TokenType.SEPARATOR and 
              self.current_token.value == '('):
            self.advance()  # (
            node = self.parse_expression()
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == ')'):
                self.advance()  # )
            else:
                self.errors.append(f"Beklenen ')' satır {self.current_token.line if self.current_token else 'EOF'}")
                if self.current_token:
                    self.advance()
            return node

        # Hata durumu: Tanımsız/geçersiz token
        if self.current_token:
            self.errors.append(
                f"Beklenmeyen veya tanımsız token '{self.current_token.value}' satır {self.current_token.line}"
            )
            self.advance()
        return None

    def parse_function_call(self) -> ParseNode:
        """function_call -> IDENTIFIER ( [args] )"""
        node = ParseNode("function_call")
        # Fonksiyon adı
        if self.current_token.type == TokenType.IDENTIFIER:
            func_node = ParseNode(self.current_token.value)
            func_node.token = self.current_token
            node.add_child(func_node)
            self.advance()
        # (
        if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == '(':
            self.advance()
            # Argümanları parse et (virgülle ayrılmış ifadeler)
            args_node = ParseNode("args")
            while self.current_token and not (self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ')'):
                arg = self.parse_expression()
                if arg:
                    args_node.add_child(arg)
                if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ',':
                    self.advance()
                else:
                    break
            node.add_child(args_node)
            if self.current_token and self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ')':
                self.advance()
            else:
                self.errors.append(f"Beklenen ')' satır {self.current_token.line if self.current_token else 'EOF'}")
                if self.current_token:
                    self.advance()
        return node
    
    def parse_if_statement(self) -> ParseNode:
        """if_stmt -> if ( expression ) statement [else statement]"""
        node = ParseNode("if_statement")
        
        self.advance()  # if
        
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == '('):
            self.advance()  # (
            
            condition = self.parse_expression()
            if condition:
                node.add_child(condition)
            
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == ')'):
                self.advance()  # )
        
        # Then ifadesi
        then_stmt = self.parse_statement()
        if then_stmt:
            node.add_child(then_stmt)
        
        # İsteğe bağlı else
        if (self.current_token and self.current_token.type == TokenType.KEYWORD and 
            self.current_token.value == 'else'):
            self.advance()  # else
            else_stmt = self.parse_statement()
            if else_stmt:
                node.add_child(else_stmt)
        
        return node
    
    def parse_while_statement(self) -> ParseNode:
        """while_stmt -> while ( expression ) statement"""
        node = ParseNode("while_statement")
        
        self.advance()  # while
        
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == '('):
            self.advance()  # (
            
            condition = self.parse_expression()
            if condition:
                node.add_child(condition)
            
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == ')'):
                self.advance()  # )
        
        # Gövde ifadesi
        body = self.parse_statement()
        if body:
            node.add_child(body)
        
        return node
    
    def parse_for_statement(self) -> ParseNode:
        """for_stmt -> for ( statement ; expression ; statement ) statement"""
        node = ParseNode("for_statement")
        
        self.advance()  # for
        
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == '('):
            self.advance()  # (
            
            # Başlangıç
            init = self.parse_statement()
            if init:
                node.add_child(init)
            
            # Koşul
            condition = self.parse_expression()
            if condition:
                node.add_child(condition)
            
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == ';'):
                self.advance()  # ;
            
            # Güncelleme
            update = self.parse_expression()
            if update:
                node.add_child(update)
            
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == ')'):
                self.advance()  # )
        
        # Gövde
        body = self.parse_statement()
        if body:
            node.add_child(body)
        
        return node
    
    def parse_return_statement(self) -> ParseNode:
        """return_stmt -> return [expression] ;"""
        node = ParseNode("return_statement")
        
        self.advance()  # return
        
        # İsteğe bağlı ifade
        if (self.current_token and 
            not (self.current_token.type == TokenType.SEPARATOR and self.current_token.value == ';')):
            expr = self.parse_expression()
            if expr:
                node.add_child(expr)
        
        # Noktalı virgül
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == ';'):
            self.advance()
        
        return node
    
    def parse_block(self) -> ParseNode:
        """block -> { statement_list }"""
        node = ParseNode("block")
        
        if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
            self.current_token.value == '{'):
            self.advance()  # {
            
            while (self.current_token and 
                   not (self.current_token.type == TokenType.SEPARATOR and self.current_token.value == '}')):
                stmt = self.parse_statement()
                if stmt:
                    node.add_child(stmt)
            
            if (self.current_token and self.current_token.type == TokenType.SEPARATOR and 
                self.current_token.value == '}'):
                self.advance()  # }
        
        return node
    
    def advance(self):
        """Bir sonraki token'a geç"""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None