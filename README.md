# C Syntax Highlighter - Gerçek Zamanlı Lexical & Syntax Analyzer
Bu proje, C programlama dili için **gerçek zamanlı syntax highlighting** sunan kapsamlı bir araçtır. Dönem ödevi olup, programlama dilleri dersindeki **lexical analyzer** ve **top-down parser** kavramlarını pratik olarak geliştriilmiş bir uygulamadır.

Projeyi indirmek için lütfen linke tıklayınız: [Download exe](https://github.com/ahmetymtkn/c-highlighter/releases/download/v1.0.0/ahmetymtkn.exe)

Projenin demo videosu için tıklayınız [Video Link]()

Proje Raporu için Tıklayınız [Rapor.docx](https://github.com/ahmetymtkn/c-highlighter/blob/main/Rapor.docx)

Projenin detaylı incelemek için Medium makale linkim [Medium Link](https://medium.com/@yumutkanahmet19/c-syntax-highlighter-gerçek-zamanlı-lexical-syntax-analyzer-9ff701ca70df)




![Görsel1](https://github.com/ahmetymtkn/c-highlighter/blob/main/src/program_gorsel1.png)




## Özellikler

### Lexical Analyzer (Sözcüksel Çözümleyici)
- **State Diagram yaklaşımı** ile token tanıma
- **12+ farklı token türü** desteği:
  - Anahtar kelimeler (int, if, for, while...)
  - Tanımlayıcılar (değişken/fonksiyon adları)
  - Sayılar (integer/float)
  - String ve karakter literalleri
  - Operatörler (+, -, ==, &&...)
  - Ayırıcılar (parantezler, noktalı virgül...)
  - Yorumlar (tek satır // ve çok satır /* */)
  - Ön işlemci direktifleri (#include, #define...)
  - Hata token'ları
    
![Görsel2](https://github.com/ahmetymtkn/c-highlighter/blob/main/src/program_gorsel2.png)

### Top-Down Parser (Yukarıdan-Aşağı Ayrıştırıcı)
- **Recursive Descent** parsing tekniği
- **Parse tree** oluşturma
- C dili temel yapılarını destekler:
  - Değişken tanımlamaları
  - Fonksiyon tanımları
  - Kontrol yapıları (if-else, while, for)
  - İfadeler ve atamalar
  - Blok yapıları

### Grafik Arayüz (GUI)
- **Tkinter** tabanlı modern arayüz
- **Gerçek zamanlı syntax highlighting** (300ms gecikme ile)
- **Çok sekmeli görünüm**:
  - Token analizi sonuçları
  - Parse tree görselleştirmesi
  - Syntax hatalarının listesi
- **Parantez dengeleme kontrolü**
- **Renkli token vurgulama** (8 farklı renk)
- **Örnek kod yükleme** özelliği

## Teknolojiler

- **Python**
- **Tkinter** (GUI framework)

## Proje Yapısı

```
c-syntax-highlighter/
├── main.py                    # Ana çalıştırma dosyası
├── gui/
│   └── highlighter_gui.py     # Grafik arayüz
├── lexer/
│   └── lexical_analyzer.py    # Lexical analyzer
├── parser/
│   ├── topdown_parser.py      # Top-down parser
│   └── parse_tree.py          # Parse tree düğümleri
├── models/
│   └── token.py               # Token sınıfları
└── README.md
```

## Kurulum ve Çalıştırma

### Gereksinimler
```bash
# Python gereklidir
python --version
```

### Kurulum
```bash
# Projeyi klonlayın
git clone https://github.com/ahmetymtkn/c-highlighter.git
cd c-highlighter

# Bağımlılıklar (sadece standart kütüphaneler kullanılmıştır)
# Ekstra kurulum gerekmez
```

### Çalıştırma
```bash
python main.py
```

## Kullanım

1. **Uygulama açıldığında** örnek C kodu otomatik yüklenir
2. **Sol panelde** C kodunuzu yazın veya düzenleyin
3. **Sağ panelde** 3 sekme görürsünüz:
   - **Token Analizi**: Tüm token'ların listesi
   - **Parse Tree**: Syntax tree görselleştirmesi
   - **Hatalar**: Syntax hatalarının listesi
4. **Gerçek zamanlı vurgulama** yazdığınız anda aktif olur
5. **Alt kısımda** token renklerinin açıklaması bulunur

## 🎨 Token Renkleri

| Token Türü | Renk | Örnek |
|------------|------|-------|
| Anahtar Kelime | Mavi | `int`, `if`, `for` |
| String | Yeşil | `"Hello World"` |
| Sayı | Turuncu | `42`, `3.14` |
| Yorum | Gri | `// yorum` |
| Operatör | Pembe | `+`, `==`, `&&` |
| Ayırıcı | Mor | `(`, `)`, `{`, `}` |
| Ön işlemci | Kahverengi | `#include` |
| Karakter | Deniz Mavisi | `'A'` |

## Teknik Detaylar

### Lexical Analyzer
- **State Diagram & Program Implementation yaklaşımı ile lexical analyzer
- **12 farklı durum** (START, IDENTIFIER, NUMBER, STRING...)
- **Hata yönetimi** ve **geri kurtarma**
- **Satır/sütun takibi** token konumları için

### Parser
- **Top-Down** parser implementasyonu
- **AST benzeri** parse tree oluşturma

### GUI
- **Event-driven** gerçek zamanlı analiz
- **Responsive** arayüz tasarımı

## Desteklenen C Yapıları

### Temel Yapılar
```c
// Değişken tanımlamaları
int x = 10;
float pi = 3.14;
char ch = 'A';

// Fonksiyon tanımları
int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n-1);
}
```

### Kontrol Yapıları
```c
// if-else
if (x > 0) {
    printf("Pozitif");
} else {
    printf("Negatif veya sıfır");
}

// while döngüsü
while (i < 10) {
    i++;
}

// for döngüsü
for (int j = 0; j < 5; j++) {
    printf("%d ", j);
}
```

### İfadeler ve Operatörler
```c
// Aritmetik işlemler
int result = (a + b) * c / d;

// Karşılaştırma
if (x >= y && z != 0) {
    // işlem
}

// Fonksiyon çağrıları
printf("Sonuç: %d\n", calculate(x, y));
```



