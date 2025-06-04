from lexer.lexical_analyzer import LexicalAnalyzer
from parser.topdown_parser import TopDownParser
from models.token import TokenType
from parser.parse_tree import ParseNode
import tkinter as tk
from tkinter import ttk

class CSyntaxHighlighterGUI:
    """Gerçek zamanlı C syntax highlighter GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Programlama Dilleri - C Syntax Highlighter")
        self.root.geometry("1200x800")
        
        # Bileşenler
        self.lexical_analyzer = LexicalAnalyzer()
        self.current_tokens = []
        self.parse_tree = None
        self.errors = []
        
        self.create_gui()
        self.configure_tags()
        
        # Gerçek zamanlı vurgulama
        self.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.text_widget.bind('<Button-1>', self.on_text_change)
        self.text_widget.bind('<MouseWheel>', self.on_text_change)

        # Renk açıklama paneli
        self.create_legend()
        
        # Başlangıç örnek kodu
        self.load_sample_code()
    
    def create_gui(self):
        """GUI bileşenlerini oluştur"""
        # Ana çerçeve
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Üst çerçeve - butonlar için
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Button(button_frame, text="Temizle", command=self.clear_text).pack(side='left', padx=2)
        
        # Bölünmüş pencere
        paned_window = ttk.PanedWindow(main_frame, orient='horizontal')
        paned_window.pack(fill='both', expand=True)
        
        # Sol panel - Kod editörü
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=2)
        
        ttk.Label(left_frame, text="C Kod Editörü", font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Kaydırma çubukları ile metin widget'ı
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.text_widget = tk.Text(text_frame, wrap='none', undo=True, font=('Courier New', 11))
        
        # Kaydırma çubukları
        v_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.text_widget.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient='horizontal', command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Kaydırma çubukları ve metin widget'ını yerleştir
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        self.text_widget.pack(fill='both', expand=True)
        
        # Sağ panel - Analiz sonuçları
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        # Sekmeler için notebook
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Token analizi sekmesi
        token_frame = ttk.Frame(self.notebook)
        self.notebook.add(token_frame, text="Token Analizi")
        
        ttk.Label(token_frame, text="Lexical Analyzer Sonuçları", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Kaydırma çubuklu token listesi
        token_list_frame = ttk.Frame(token_frame)
        token_list_frame.pack(fill='both', expand=True)
        
        self.token_listbox = tk.Listbox(token_list_frame, font=('Courier New', 9))
        token_scrollbar = ttk.Scrollbar(token_list_frame, orient='vertical', command=self.token_listbox.yview)
        self.token_listbox.configure(yscrollcommand=token_scrollbar.set)
        
        token_scrollbar.pack(side='right', fill='y')
        self.token_listbox.pack(fill='both', expand=True)
        
        # Parse tree sekmesi
        parse_frame = ttk.Frame(self.notebook)
        self.notebook.add(parse_frame, text="Parse Tree")
        
        ttk.Label(parse_frame, text="Top-Down Parser Sonuçları", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Parse tree görüntüsü
        tree_frame = ttk.Frame(parse_frame)
        tree_frame.pack(fill='both', expand=True)
        
        self.parse_tree_widget = ttk.Treeview(tree_frame)
        tree_scrollbar_v = ttk.Scrollbar(tree_frame, orient='vertical', command=self.parse_tree_widget.yview)
        tree_scrollbar_h = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.parse_tree_widget.xview)
        self.parse_tree_widget.configure(yscrollcommand=tree_scrollbar_v.set, xscrollcommand=tree_scrollbar_h.set)
        
        tree_scrollbar_v.pack(side='right', fill='y')
        tree_scrollbar_h.pack(side='bottom', fill='x')
        self.parse_tree_widget.pack(fill='both', expand=True)
        
        # Hatalar sekmesi
        error_frame = ttk.Frame(self.notebook)
        self.notebook.add(error_frame, text="Hatalar")
        
        ttk.Label(error_frame, text="Syntax Hataları", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Hata görüntüsü
        error_list_frame = ttk.Frame(error_frame)
        error_list_frame.pack(fill='both', expand=True)
        
        self.error_listbox = tk.Listbox(error_list_frame, font=('Courier New', 9), fg='red')
        error_scrollbar = ttk.Scrollbar(error_list_frame, orient='vertical', command=self.error_listbox.yview)
        self.error_listbox.configure(yscrollcommand=error_scrollbar.set)
        
        error_scrollbar.pack(side='right', fill='y')
        self.error_listbox.pack(fill='both', expand=True)
        
    def configure_tags(self):
        """Text widget etiketlerini yapılandır"""
        # 5+ farklı token türü için renkler
        self.text_widget.tag_configure('KEYWORD', foreground='#0000FF', font=('Courier New', 11, 'bold'))
        self.text_widget.tag_configure('IDENTIFIER', foreground='#000080')
        self.text_widget.tag_configure('NUMBER', foreground='#FF6600')
        self.text_widget.tag_configure('STRING', foreground='#008000')
        self.text_widget.tag_configure('CHAR', foreground='#008080')
        self.text_widget.tag_configure('OPERATOR', foreground='#FF0080', font=('Courier New', 11, 'bold'))
        self.text_widget.tag_configure('SEPARATOR', foreground='#800080', font=('Courier New', 11, 'bold'))
        self.text_widget.tag_configure('COMMENT', foreground='#808080', font=('Courier New', 11, 'italic'))
        self.text_widget.tag_configure('PREPROCESSOR', foreground='#804000', font=('Courier New', 11, 'bold'))
        self.text_widget.tag_configure('ERROR', background='#FFCCCC', foreground='#CC0000')
        
        # Syntax hata vurgulama
        self.text_widget.tag_configure('SYNTAX_ERROR', background='#FFE6E6')
        self.text_widget.tag_configure('PAREN_ERROR', background='#FF9999', foreground='white')
    
    def on_text_change(self, event=None):
        """Metin değiştiğinde gerçek zamanlı analiz"""
        # Kısa gecikme ile analiz et (performans için)
        self.root.after(300, self.perform_real_time_analysis)
    
    def perform_real_time_analysis(self):
        """Gerçek zamanlı analiz gerçekleştir"""
        try:
            content = self.text_widget.get('1.0', 'end-1c')
            
            # Lexical analiz
            self.current_tokens = self.lexical_analyzer.analyze(content)
            
            # Syntax vurgulama
            self.apply_syntax_highlighting()
            
            # Görüntüleri güncelle
            self.update_token_display()

            # Parse analizi (sadece çok büyük değilse)
            if len(content) < 5000:  # Performans sınırı
                try:
                    parser = TopDownParser(self.current_tokens)
                    self.parse_tree = parser.parse()
                    self.errors = parser.errors
                    self.update_parse_tree_display()
                    self.update_error_display()
                except Exception as e:
                    self.errors = [f"Parser hatası: {str(e)}"]
                    self.update_error_display()
        
        except Exception as e:
            print(f"Gerçek zamanlı analiz hatası: {e}")
    
    def apply_syntax_highlighting(self):
        """Syntax vurgulama uygula"""
        # Mevcut etiketleri temizle
        for tag in ['KEYWORD', 'IDENTIFIER', 'NUMBER', 'STRING', 'CHAR', 
                   'OPERATOR', 'SEPARATOR', 'COMMENT', 'PREPROCESSOR', 'ERROR']:
            self.text_widget.tag_remove(tag, '1.0', 'end')
        
        # Token'lara göre vurgulama uygula
        for token in self.current_tokens:
            if token.type == TokenType.EOF:
                continue
            
            start_index = f"{token.line}.{token.column - 1}"
            end_index = f"{token.line}.{token.column - 1 + len(token.value)}"
            
            try:
                self.text_widget.tag_add(token.type.value, start_index, end_index)
            except tk.TclError:
                continue  # Geçersiz indeks, atla
        
        # Parantez dengeleme kontrolü
        self.check_parentheses_balance()
    
    def check_parentheses_balance(self):
        """Parantez dengeleme kontrolü"""
        # Önce eski parantez hata etiketlerini temizle
        self.text_widget.tag_remove('PAREN_ERROR', '1.0', 'end')
        content = self.text_widget.get('1.0', 'end-1c')
        stack = []
        pairs = {'(': ')', '{': '}', '[': ']'}
        opening = set(pairs.keys())
        closing = set(pairs.values())
        reverse_pairs = {v: k for k, v in pairs.items()}
        
        line = 1
        col = 0
        
        for i, char in enumerate(content):
            if char == '\n':
                line += 1
                col = 0
            else:
                col += 1
            
            if char in opening:
                stack.append((char, line, col))
            elif char in closing:
                if stack and stack[-1][0] == reverse_pairs[char]:
                    stack.pop()
                else:
                    # Eşleşmeyen kapanış
                    index = f"{line}.{col-1}"
                    self.text_widget.tag_add('PAREN_ERROR', index, f"{index}+1c")
        
        # Eşleşmeyen açılış
        for char, line, col in stack:
            index = f"{line}.{col-1}"
            self.text_widget.tag_add('PAREN_ERROR', index, f"{index}+1c")
    
    def update_token_display(self):
        """Token listesini güncelle"""
        self.token_listbox.delete(0, tk.END)
        
        for i, token in enumerate(self.current_tokens):
            if token.type == TokenType.EOF:
                continue
            
            display_text = f"{i+1:3d}: {token.type.value:12s} | {token.value:20s} | Satır {token.line:2d}, Sütun {token.column:2d}"
            self.token_listbox.insert(tk.END, display_text)
    
    def update_parse_tree_display(self):
        """Parse tree görüntüsünü güncelle"""
        # Mevcut ağacı temizle
        for item in self.parse_tree_widget.get_children():
            self.parse_tree_widget.delete(item)
        
        if self.parse_tree:
            self.insert_tree_node(self.parse_tree, "")
    
    def insert_tree_node(self, node: ParseNode, parent: str):
        """Parse tree düğümünü ekle"""
        if not node:
            return
        
        # Düğüm metni
        display_text = node.name
        if hasattr(node, 'token') and node.token:
            display_text += f" ({node.token.value})"
        
        item_id = self.parse_tree_widget.insert(parent, 'end', text=display_text)
        
        # Alt düğümleri ekle
        for child in node.children:
            self.insert_tree_node(child, item_id)
    
    def update_error_display(self):
        """Hata listesini güncelle"""
        self.error_listbox.delete(0, tk.END)
        
        for error in self.errors:
            self.error_listbox.insert(tk.END, error)
        
        if not self.errors:
            self.error_listbox.insert(tk.END, "Syntax hatası bulunamadı!")
    
    def load_sample_code(self):
        """Örnek kod yükle"""
        sample_code = """#include <stdio.h>
#include <stdlib.h>

/* Bu bir örnek C programıdır */
// Gerçek zamanlı syntax vurgulama testi

int main() {
    int x = 10;
    int y = 20;
    char ch = 'A';
    float pi = 3.14159;
    
    // Kontrol yapıları
    if (x > y) {
        printf("x büyük\\n");
    } else {
        printf("y büyük veya eşit\\n");
    }
    
    // Döngü yapıları
    for (int i = 0; i < 5; i++) {
        printf("i = %d\\n", i);
    }
    
    int j = 0;
    while (j < 3) {
        printf("j = %d\\n", j);
        j = j + 1;
    }
    
    // Aritmetik işlemler
    int result = x + y * 2 - (x / 2);
    
    return 0;
}

// Fonksiyon tanımı
int factorial(int n) {
    if (n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
}"""
        
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', sample_code)
        self.perform_real_time_analysis()
    
    def clear_text(self):
        """Metni temizle"""
        self.text_widget.delete('1.0', tk.END)
        self.token_listbox.delete(0, tk.END)
        self.error_listbox.delete(0, tk.END)
        # Parse tree'yi temizle
        for item in self.parse_tree_widget.get_children():
            self.parse_tree_widget.delete(item)

    def create_legend(self):
        """Alt kısımda token renklerini gösteren açıklama paneli"""
        legend_frame = ttk.LabelFrame(self.root, text="🎨 Token Renkleri")
        legend_frame.pack(fill=tk.X, padx=10, pady=(0, 10), side=tk.BOTTOM)

        colors_info = [
            ("Anahtar Kelime", "#0000FF", "int, if, for"),
            ("String", "#008000", '"Hello"'),
            ("Sayı", "#FF6600", "42, 3.14"),
            ("Yorum", "#808080", "// yorum"),
            ("Operatör", "#FF0080", "+, ==, &&"),
            ("Ayırıcı", "#800080", "( ) { } ;"),
            ("Ön işlemci", "#804000", "#include"),
            ("Karakter", "#008080", "'A'")
        ]

        for i, (label, color, example) in enumerate(colors_info):
            frame = ttk.Frame(legend_frame)
            frame.grid(row=i//4, column=i%4, sticky='w', padx=10, pady=3)

            dot = ttk.Label(frame, text="●", foreground=color, font=("Arial", 12, "bold"))
            dot.pack(side=tk.LEFT)

            desc = ttk.Label(frame, text=f"{label}: {example}", font=("Arial", 9))
            desc.pack(side=tk.LEFT, padx=(5, 0))