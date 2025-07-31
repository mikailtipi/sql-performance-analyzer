# 🔮 SQL Query Optimization & Structural Analysis Tool

## Overview (English)

This interactive Streamlit-based tool is designed to analyze SQL Server queries both structurally and in terms of execution performance. It supports dynamic metadata fetching from the database or an Excel file, integrates execution plan visualization, and logs query durations for comparison.

### Key Features
- 💻 UI with light/dark theme switch
- 🧩 Metadata import (from DB or Excel)
- 🧠 Structural query analysis (SELECT *, WHERE checks, etc.)
- ⚡ Real-time performance evaluation using a custom SQL Server Stored Procedure
- 📊 Execution plan visualization (Graphviz)
- 📝 Recommendations based on size, indexing, and performance
- 🧾 Query history log with delta comparisons
- 📥 Exportable metadata and execution plans

### Included Stored Procedure (SSMS)
Located in `/stored_procedures/RunAndMeasure.sql`, this SP securely executes the query, measures run time and row count, logs it to a local table, and returns clear JSON-compatible results.

### 💻 Technologies Used
- Streamlit (UI)
- PyODBC (Database Connection)
- Pandas (Data processing)
- Graphviz (Execution plan visualization)

### 📷 Screenshots

#### 🔐 Splash Screen  
![Splash Screen](images/splashscreen.png)

#### 🔌 Database Connection  
![DB Connection](images/dbconnection.png)

#### 📦 Metadata Options  
![Metadata Options](images/metadata.png)

#### 📋 Query Analyzer  
![Query Analyzer](images/queryanalyzer.png)

#### 🔎 Metadata Details  
![Details](images/details.png)

#### 🧪 Sample Query Analysis  
![Example](images/example.png)  
![Example 2](images/example2.png)

#### ⏱ Execution Results  
![Execution](images/execution.png)  
![Execution Example](images/executionexample.png)

#### 🖥 Connect From Bash  
![Connect from Bash](images/connectfrombash.png)

### 🛠 Requirements
- Python 3.8+
- Microsoft SQL Server
- ODBC Driver 18 for SQL Server

### 🙌 Contribute
Contributions are welcome! Feel free to fork the repo, submit issues, or open pull requests.
---

## Genel Bilgi (Türkçe)

Bu interaktif Streamlit aracı, SQL Server sorgularını yapısal ve performans açısından analiz etmek için geliştirilmiştir. Metadata'yı doğrudan veritabanından veya Excel'den çekebilir, execution plan'ı görselleştirebilir ve geçmiş sorguları karşılaştırmak için log tutar.

### Temel Özellikler
- 💻 Açık/Koyu tema destekli kullanıcı arayüzü
- 🧩 Veritabanı ya da Excel'den metadata yükleme
- 🧠 Sorgular için yapısal analiz (SELECT * uyarıları, WHERE önerileri)
- ⚡ SP ile gerçek zamanlı performans ölçümü (SSMS ile entegre)
- 📊 Execution plan görselleştirme (Graphviz ile)
- 📝 Tablo büyüklüğü, indeks eksikliği ve performans sorunlarına dayalı öneriler
- 🧾 Sorgu geçmişi ve karşılaştırmalı analizler
- 📥 Metadata ve plan çıktıları indirilebilir

### Ekli Stored Procedure (SSMS)
`/stored_procedures/RunAndMeasure.sql` içerisinde bulunan bu SP, girilen sorguyu çalıştırır, çalıştırma süresi ve etkilenen satır sayısını ölçer, bir log tablosuna yazar ve okunabilir çıktılar döner.

### 💻 Kullanılan Teknolojiler
- Streamlit (Arayüz)
- PyODBC (Veritabanı Bağlantısı)
- Pandas (Veri işleme)
- Graphviz (Execution plan görselleştirme)

### 📷 Ekran Görüntüleri

#### 🔐 Açılış Ekranı 
![Açılış Ekranı](images/splashscreen.png)

#### 🔌 Database Bağlantısı  
![DB Bağlantısı](images/dbconnection.png)

#### 📦 Metadata Ayarları  
![Metadata Ayarları](images/metadata.png)

#### 📋 Sorgu Analizi  
![Sorgu Analizi](images/queryanalyzer.png)

#### 🔎 Metadata Detayları 
![Detaylar](images/details.png)

#### 🧪 Sample Sorgu Analizi  
![Örnek](images/example.png)  
![Örnek 2](images/example2.png)

#### ⏱ Execution Sonuçları  
![Execution](images/execution.png)  
![Execution Örnek](images/executionexample.png)

#### 🖥 CMD ile Bağlanma  
![CMD ile Bağlanma](images/connectfrombash.png)


### 🛠 Gereksinimler
- Python 3.8+
- Microsoft SQL Server
- ODBC Driver 18 for SQL Server

### 🙌 Katkı Sağla
Açık kaynak katkılarını memnuniyetle karşılıyorum. Fork'layabilir, issue açabilir veya pull request gönderebilirsiniz.


---

## Run Locally

```bash
git clone https://github.com/yourusername/sql-optimization-tool.git
cd sql-optimization-tool
pip install -r requirements.txt
streamlit run app/app.py
```

### Kurulum
```bash
git clone https://github.com/yourusername/sql-performance-analyzer.git
cd sql-performance-analyzer
pip install -r requirements.txt
streamlit run app.py
```
---

## Developed by

**Mikail Tipi**  
📧 [mkltipi@gmail.com](mailto:mkltipi@gmail.com)  
🔗 [LinkedIn - mikailtipi](https://www.linkedin.com/in/mikailtipi/)