# CountNClear

## 🇬🇧 CountNClear - Terminal Cleaner Utility

**CountNClear** is a small Python package that counts how many times a script has been executed in the terminal and clears it when a specified limit is reached.

### 🛠 Installation
```bash
pip install countnclear
```

### 🚀 Usage
```python
from countnclear import CountFlushTerm

# Set script to clear terminal after 5 executions
CountFlushTerm(5)
```

### 📜 Example script (`example.py`)
Save the following code as **`example.py`** and run it:
```python
from countnclear import CountFlushTerm
import time

for i in range(10):
    print(f"Running test: {i + 1}")
    CountFlushTerm(5)  # Clears the terminal after 5 executions
    time.sleep(1)
```

---


## 🇺🇿 CountNClear - Terminal tozalovchi vosita

**CountNClear** - bu terminalda skript necha marta ishga tushirilganini hisoblaydigan va belgilangan limitga yetganda terminalni tozalaydigan kichik kutubxona.

### 🛠 O'rnatish
```bash
pip install countnclear
```

### 🚀 Foydalanish
```python
from countnclear import CountFlushTerm

# Skriptni 5 martadan keyin terminalni tozalash uchun sozlash
CountFlushTerm(5)
```

### 📜 Namuna skript (`example.py`)
Quyidagi kodni **`example.py`** nomi bilan saqlang va ishga tushiring:
```python
from countnclear import CountFlushTerm
import time

for i in range(10):
    print(f"Test ishlamoqda: {i + 1}")
    CountFlushTerm(5)  # 5 martadan keyin terminalni tozalaydi
    time.sleep(1)
```

---

## 🇷🇺 CountNClear - Утилита очистки терминала

**CountNClear** - это небольшой Python-пакет, который считает, сколько раз скрипт был запущен в терминале, и очищает его при достижении заданного лимита.

### 🛠 Установка
```bash
pip install countnclear
```

### 🚀 Использование
```python
from countnclear import CountFlushTerm

# Очистка терминала после 5 запусков
CountFlushTerm(5)
```

### 📜 Пример скрипта (`example.py`)
Сохраните следующий код в файл **`example.py`** и запустите:
```python
from countnclear import CountFlushTerm
import time

for i in range(10):
    print(f"Тест выполняется: {i + 1}")
    CountFlushTerm(5)  # Очищает терминал после 5 запусков
    time.sleep(1)
```

🔗 **Site**: [click](https://www.raxmatullox.me)  
