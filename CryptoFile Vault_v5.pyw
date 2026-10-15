
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado por: 👉 Cristian M. Veliz Cano ✔
Versión del Soft: 👉 V-05
Nombre del Soft: ✨ CryptoFile Vault ✨
✨ Encriptador Universal de Archivos ✨

✨ CryptoFile Vault ✨

✅ Este Soft-Ware fue diseñado para encriptar y desencriptar
cualquier tipo de archivo de forma segura utilizando
criptografía simétrica con clave personalizada.

⚙️ El funcionamiento del Programa es Directo:

📄 El Usuario selecciona archivos individuales o múltiples,
   ingresa una clave privada, y el sistema los encripta
   convirtiéndolos en archivos seguros .dat

⭐ El Soft-Ware permite trabajar con:

✔ Archivos Individuales de Cualquier Tipo (*.*)
✔ Múltiples Archivos (auto-comprime en ZIP y encripta)
✔ Múltiples Archivos (auto-comprime en ZIP y encripta, Con Gerarquia de Arbol)
✔ Con Compreción, y Des-Compreción, Original, [osea si tiene Gerarquia de Arbol]
✔ Directorios Completos (con contenido recursivo, [Gerarquia de Arbol])
✔ Desencriptación con Recuperación de Nombres Originales, [Gerarquia de Arbol]
✔ Extracción Organizada en Carpeta "Desencriptados", [Gerarquia de Arbol]
✔ Con Visor, para Ver la Gerarquia del Arbol de 2 Formas, y poder Hacer Una Revición
✔ Con Visor, de LOG´s [EVENTOS], que hemos Hecho hasta el Momento, Herrores, o Auditoria

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Nota Importante:

➜ Este Soft-Ware trabaja completamente de forma Local.

✔ No requiere conexión a Internet.
✔ No utiliza Servicios Externos.
✔ No transmite Información.
✔ Criptografía AES-128 en modo CBC.
✔ Las claves NO se almacenan.

💯% OFF-LINE y SEGURO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️ Atajos del Teclado:

📎 F1
• Para mostrar información del software.

📎 CTRL+K
⌨️ Para mostrar los Atajos del Teclado.

📎 ESC
• Cierra inmediatamente el Soft-Ware.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Licencia:

MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software...

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 Algoritmo de Encriptación:

➜ Fernet (AES-128 en modo CBC + HMAC)
➜ ZIP (pyzipper) ↔ Con soporte password ↔ CON CONTRASEÑA AES-256
➜ Clave derivada mediante PBKDF2HMAC (100,000 iteraciones)
➜ Salt aleatorio único por cada archivo
➜ Verificación de integridad integrada
➜ Verificación de la Creación del Archivo RESUMEN-LOG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Tu Bóveda Digital Personal para Proteger Cualquier Archivo."

✨ CryptoFile Vault_v5 ✨
Alojado en Mega:
https://mega.nz/file/vpUziCAI#d3PSDPvvlxyAaqN9oe4JvPTpxu2ADXMUUc7SLFBKqm4

Source Code:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pip install pillow-jxl-plugin==1.0.1
'''
##=========================================================================================
import os
import sys
import zipfile
import base64
import secrets
import hashlib
import time
from pathlib import Path as PathLib
from datetime import datetime
import random
import string
import pyperclip

import threading
from threading import Thread

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QListWidget, QLabel, QPlainTextEdit,
    QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QSpinBox, 
    QGroupBox, QGridLayout, QDialog, QShortcut, QProgressBar, QCheckBox,
    QSplitter, QFrame)

from PyQt5.QtGui import QKeySequence, QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Importar cryptography ↔ CONTRASEÑA AES-256
try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    ##from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2  <-- Anterior, pero me actualice
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    ## <<<-- Usar PBKDF2HMAC para determinar qué categorías usar (determinístico pero aleatorio) --- 
    from cryptography.hazmat.backends import default_backend
    print("✅ Cryptography cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando cryptography: {e}")
    print(f"Python usado: {sys.executable}")
    print(f"Versión: {sys.version}")

# Con soporte ZIP password ↔ CON CONTRASEÑA AES-256
try:
    import pyzipper
except ImportError:
    print("⚠️ pyzipper no instalado. ZIP sin contraseña. pip install pyzipper")

import resources_rc
##====================================================================================
ZIP_PASSWORD_AVAILABLE = True
CRYPTO_AVAILABLE = True
##====================================================================================
# --- Clase para manejo de rutas de recursos ---
##====================================================================================
class Path():
    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # =========================
    # ✨ Devuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================

    @staticmethod
    def resource_path_app():
        try:
            path_app = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        except Exception as e:
            print(e)
        return path_app

# -------------------- Helpers ---------------------
BASE_DIR = Path.resource_path_app()
LOG_FILE = os.path.join(BASE_DIR, "Log")

# ------------------ Log Registre ------------------
def log_message(msg):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    try:
        with open(f"{LOG_FILE}.log", "a", encoding="utf-8", errors='ignore') as f:
            f.write(line + "\n")
    except Exception:
        pass

def LogFile():
    return f"{LOG_FILE}.log"

SEMANTIC_DICT_GENERAL = {
    # --- Lenguajes de Programación y Frameworks ---
    "python": ["py", "python3", "python programming", "python scripting", "python language", "python code", "python dev"],
    "javascript": ["js", "javascript language", "ecmascript", "node.js", "nodejs", "frontend scripting", "js code"],
    "java": ["java language", "jvm", "java development", "jdk", "jre", "spring boot", "maven", "gradle"],
    "c++": ["cpp", "c plus plus", "gnu c++", "g++", "stl", "c++ standard library", "c++ development"],
    "php": ["php language", "php scripting", "laravel", "symfony", "composer", "backend scripting"],
    "ruby": ["ruby on rails", "rails framework", "ruby language", "gem", "bundler", "ruby scripting"],
    "go": ["golang", "go language", "go programming", "go modules"],
    "rust": ["rust lang", "rust programming", "cargo", "rust memory safety", "systems programming"],
    "sql": ["structured query language", "sql query", "database query", "t-sql", "pl/sql", "mysql", "postgresql"],
    "html": ["hypertext markup language", "html5", "web markup", "html code", "html tags"],
    "css": ["cascading style sheets", "css3", "stylesheet", "style rules", "sass", "scss", "less"],
    
    # --- Herramientas y Tecnologías de Desarrollo ---
    "git": ["git version control", "git repo", "github", "gitlab", "bitbucket", "git commit", "git branch", "git merge"],
    "docker": ["containers", "containerization", "dockerfile", "docker compose", "docker image", "docker hub", "kubernetes", "k8s"],
    "api": ["application programming interface", "rest api", "restful", "graphql", "api endpoint", "web service", "microservice"],
    "aws": ["amazon web services", "ec2", "s3", "lambda", "rds", "cloud computing", "aws cloud"],
    "azure": ["microsoft azure", "azure cloud", "azure services", "cloud platform ms"],
    "gcp": ["google cloud platform", "gcp cloud", "google compute engine", "gke"],
    "ci/cd": ["continuous integration", "continuous deployment", "jenkins", "github actions", "gitlab ci", "devops pipeline"],
    "testing": ["unit testing", "integration testing", "pytest", "unittest", "jest", "selenium", "tdd", "test driven development"],
    "linux": ["gnu linux", "linux kernel", "ubuntu", "debian", "centos", "shell scripting", "bash", "command line"],
    "windows": ["win32", "powershell", "windows server", "active directory", "windows os"],
    "macos": ["os x", "mac os", "cocoa", "swift", "xcode", "apple os"],
    
    # --- Conceptos y Paradigmas ---
    "algoritmo": ["algorithm", "algorithm design", "complexity", "big o notation", "data structures", "sorting algorithms"],
    "base de datos": ["database", "dbms", "rdbms", "nosql", "mongodb", "cassandra", "redis", "data storage", "sql database"],
    "seguridad": ["security", "cybersecurity", "cryptography", "encryption", "hashing", "vulnerability", "penetration testing", "owasp"],
    "osint": ["open source intelligence", "open-source intelligence", "intelligence gathering", "reconnaissance", "infosec"],
    "machine learning": ["ml", "ai", "artificial intelligence", "deep learning", "neural networks", "tensorflow", "pytorch", "scikit-learn", "data science"],
    "blockchain": ["distributed ledger", "smart contracts", "ethereum", "bitcoin", "cryptocurrency", "dlt", "web3"],
    "devops": ["development operations", "infrastructure as code", "automation", "ansible", "puppet", "chef", "terraform"],
    
    # --- Recursos y Comunidades ---
    "stackoverflow": ["stack overflow", "stackexchange", "programming q&a", "so", "coding forum"],
    "github": ["git repo", "github repo", "code repository", "source control", "open source", "git hosting"],
    "documentación": ["docs", "documentation", "api docs", "readthedocs", "tech reference", "manual"],

    # --- Ingeniería de Software ---
    "arquitectura": ["software architecture", "system architecture", "microservices architecture", "design patterns", "arquitectura de sistemas"],
    "uml": ["unified modeling language", "uml diagrams", "diagrama de clases", "casos de uso", "modelado"],
    "poo": ["oop", "object oriented programming", "programación orientada a objetos", "clases y objetos", "herencia", "polimorfismo"],
    "clean code": ["código limpio", "clean architecture", "refactoring", "buenas prácticas", "principios solid", "tdd", "arquitectura limpia"],
    "debug": ["debugging", "depuración", "troubleshooting", "bug fixing", "error tracking"],

    # --- Redes e Infraestructura ---
    "redes": ["networking", "network infrastructure", "routers", "switches", "protocolos de red", "tcp/ip", "dns", "dhcp"],
    "vpn": ["virtual private network", "conexion segura", "remote access", "tunel vpn"],
    "firewall": ["security firewall", "waf", "network filter", "protection layer", "filtrado de paquetes"],
    "servidor": ["server", "dedicated server", "vps", "host", "http server", "nginx", "apache"],

    # --- Ingeniería y electrónica ---
    "microcontrolador": ["microcontroller", "embedded system", "arduino", "esp32", "stm32", "programación embebida"],
    "sensores": ["sensor", "iot sensor", "arduino sensors", "electronic measurement", "telemetría", "sensores iot"],
    "robotica": ["robotics", "autonomous systems", "servo motors", "ros", "robot control", "mecatrónica"],

    # --- Inteligencia Artificial avanzada ---
    "nlp": ["natural language processing", "procesamiento de lenguaje natural", "tokenization", "llm", "transformers"],
    "vision": ["computer vision", "visión artificial", "image processing", "ocr", "detección de objetos"],
    "dataset": ["data set", "training data", "conjunto de datos", "data labeling", "csv dataset"],
    "reinforcement learning": ["rl", "aprendizaje por refuerzo", "agent training", "reward function"],

    # --- Data Science, Big Data y Estadística ---
    "big data": ["large scale data", "hadoop", "spark", "databricks", "data lakes", "etl", "pipelines"],
    "estadística": ["statistics", "probability", "regression", "anova", "data analysis", "modelos estadísticos"],
    "visualización": ["data visualization", "plots", "dashboards", "matplotlib", "power bi", "tableau"],

    # --- Ciberseguridad avanzada ---
    "malware": ["virus", "troyano", "spyware", "malicious software", "payload"],
    "forense digital": ["digital forensics", "dfir", "análisis forense", "memory dump", "evidencia digital"],
    "exploits": ["vulnerability exploit", "rce", "lfi", "rfi", "buffer overflow", "exploit db"],

    # --- Desarrollo móvil ---
    "android": ["android dev", "apk", "kotlin", "java android", "android studio"],
    "ios": ["iphone dev", "swiftui", "xcode project", "objective-c"],

    # --- Matemáticas aplicadas a ingeniería ---
    "matrices": ["matrix", "matrix algebra", "álgebra lineal", "vectores", "numpy array"],
    "calculo": ["calculus", "derivatives", "integrals", "math analysis", "matemáticas avanzadas"],

    # --- Vida Diaria y Hogar ---
    "persona": ["person", "individual", "contact", "profile", "gente", "individuo", "sujeto"],
    "ubicacion": ["location", "place", "address", "city", "site", "lugar", "sitio", "dirección", "posición"],
    "casa": ["home", "house", "apartment", "flat", "domicilio", "vivienda", "hogar", "departamento"],
    "comida": ["food", "meal", "cuisine", "dish", "alimento", "platillo", "vianda"],
    "receta": ["recipe", "cooking recipe", "food recipe", "gastronomy", "cocina", "guía de cocina"],
    "limpieza": ["cleaning", "cleaning tips", "house cleaning", "tidying", "aseo", "orden", "higiene"],
    "compra": ["shopping", "purchase", "buying", "store", "market", "comprar", "adquisición"],
    "dinero": ["money", "cash", "currency", "funds", "payment", "pago", "capital", "finanzas"],
    "salud": ["health", "wellness", "fitness", "medicine", "well-being", "bienestar", "medicina", "forma física"],
    "trabajo": ["job", "work", "employment", "career", "profession", "oficio", "empleo", "ocupación"],
    "educación": ["education", "learning", "school", "university", "course", "study", "aprendizaje", "formación"],
    "familia": ["family", "relatives", "kin", "household", "parientes", "familiares"],
    "amigos": ["friends", "friendship", "buddies", "pals", "amistad", "compañeros"],
    
    # --- Intereses y Ocio ---
    "deporte": ["sport", "sports", "exercise", "game", "match", "competency", "ejercicio físico", "competencia"],
    "música": ["music", "song", "track", "melody", "tune", "canción", "tema musical"],
    "viaje": ["travel", "trip", "journey", "vacation", "tourism", "viajar", "excursión", "turismo"],
    "libro": ["book", "novel", "reading", "text", "publication", "lectura", "texto", "publicación"],
    "película": ["movie", "film", "cinema", "motion picture", "cine", "filme"],
    "coche": ["car", "automobile", "vehicle", "auto", "motorcar", "vehículo", "automóvil"],
    "mascota": ["pet", "animal", "companion animal", "mascota", "animal doméstico"],
    
    # --- Agricultura y Naturaleza ---
    "semillas": ["seed", "seeds", "plant seeds", "agriculture seeds", "semilla", "grano", "simiente"],
    "fertilizantes": ["fertilizer", "fertilisers", "plant feed", "nutrients", "abono", "nutrientes para plantas"],
    "planta": ["plant", "flora", "vegetation", "greenery", "vegetal", "flora local"],
    "jardín": ["garden", "yard", "orchard", "patio", "cultivo", "huerto"],
    "clima": ["weather", "climate", "temperature", "forecast", "tiempo atmosférico", "pronóstico del tiempo"],
    
    # --- Conceptos Abstractos y Comunicación ---
    "idea": ["idea", "concept", "thought", "notion", "inspiration", "brainwave", "concepto", "pensamiento", "inspiración"],
    "problema": ["problem", "issue", "challenge", "trouble", "dilemma", "obstacle", "inconveniente", "dilema", "obstáculo"],
    "solución": ["solution", "answer", "fix", "resolution", "remedy", "solve", "respuesta", "arreglo", "resolución", "remedio"],
    "tiempo": ["time", "moment", "duration", "period", "while", "ocasion", "momento", "duración", "período", "rato"],
    "amor": ["love", "affection", "romance", "passion", "devotion", "cariño", "afecto", "pasión"],
    "feliz": ["happy", "joyful", "glad", "cheerful", "delighted", "content", "alegre", "contento", "satisfecho"],
    "triste": ["sad", "unhappy", "sorrowful", "melancholy", "depressed", "deprimido", "melancólico"],
    "conversación": ["conversation", "talk", "chat", "dialogue", "discussion", "charla", "diálogo", "debate", "plática"],
    "pregunta": ["question", "query", "inquiry", "doubt", "consulta", "duda", "preguntar"],
    "respuesta": ["answer", "reply", "response", "retort", "respuesta", "réplica", "contestación"],
    "información": ["information", "info", "data", "details", "facts", "knowledge", "datos", "detalles", "conocimiento", "saber"],
    "noticia": ["news", "report", "update", "headline", "story", "reportaje", "titular", "actualidad"],
    "evento": ["event", "occasion", "happening", "incident", "affair", "acontecimiento", "suceso", "incidente"],
    "oportunidad": ["opportunity", "chance", "prospect", "opening", "oportunidad", "posibilidad", "ocasión"],

    # --- Transporte ---
    "motocicleta": ["moto", "motorcycle", "bike", "motocicleta", "vehículo de dos ruedas"],
    "autobús": ["bus", "coach", "transporte público", "camioneta pública"],
    "bicicleta": ["bicycle", "bike", "cicla", "bici"],

    # --- Oficios y trabajos técnicos civiles ---
    "electricista": ["electrician", "instalador eléctrico", "servicio eléctrico", "cables", "circuitos del hogar"],
    "plomero": ["plumber", "fontanero", "tuberías", "reparación de fugas", "drenajes"],
    "carpintero": ["carpenter", "madera", "ebanistería", "muebles"],
    "albañil": ["mason", "construction worker", "block", "cemento", "yeso"],
    "herramientas": ["tools", "hand tools", "kit de herramientas", "martillo", "llave inglesa"],

    # --- Servicios públicos ---
    "agua": ["water", "servicio de agua", "suministro", "tuberías", "plomería"],
    "electricidad": ["electricity", "power", "luz", "energía", "corriente"],
    "internet": ["wifi", "network", "router", "conexión web"],

    # --- Cocina y hogar avanzado ---
    "electrodoméstico": ["appliance", "home appliance", "cocina eléctrica", "microondas", "refrigerador"],
    "bebida": ["drink", "beverage", "refresco", "jugo", "café", "té"],

    # --- Seguridad doméstica ---
    "emergencia": ["emergency", "urgent situation", "accidente", "llamar ayuda"],
    "primeros auxilios": ["first aid", "auxilio", "curación básica"],
    "incendio": ["fire", "fuego", "accidente doméstico", "alarma"],

    # --- Clima y fenómenos naturales ---
    "lluvia": ["rain", "heavy rain", "precipitación"],
    "viento": ["wind", "breeze", "air flow"],
    "terremoto": ["earthquake", "sismo", "temblor"],

    # --- Oficina y documentos ---
    "documento": ["document", "file", "paper", "archivo"],
    "correo": ["email", "mail", "mensaje", "inbox"],
    "foto": ["photo", "image", "picture", "fotografía"],

    # --- Tecnología general para civiles ---
    "celular": ["phone", "smartphone", "móvil", "android", "iphone"],
    "computadora": ["computer", "pc", "laptop", "notebook"],

    # --- Emociones adicionales ---
    "enojado": ["angry", "mad", "furious", "molesto"],
    "relajado": ["relaxed", "calm", "tranquilo"],
    "estresado": ["stressed", "anxious", "preocupado"],

    # --- Conversación y expresión ---
    "mensaje": ["message", "text", "sms", "chat"],
    "explicación": ["explanation", "clarification", "detalle"],
    "historia": ["story", "tale", "narrative", "relato"],

    # --- Objetos cotidianos ---
    "bolsa": ["bag", "purse", "saco", "mochila"],
    "llave": ["key", "house key", "car key"],
    "mesa": ["table", "desk", "mesón"],
    "silla": ["chair", "seat"],

    # --- Anime ---
    "anime": ["japanese animation", "animación japonesa", "otaku", "anime series", "anime show"],
    "shonen": ["acción juvenil", "battle anime", "anime para jóvenes", "shounen"],
    "shojo": ["romance anime", "anime para chicas", "shoujo"],
    "isekai": ["otro mundo", "fantasy world anime", "isekai anime"],
    "opening": ["op", "intro anime", "canción inicial"],
    "ending": ["ed", "canción final", "ending theme"],

    # --- Caricaturas ---
    "caricatura": ["cartoon", "animated show", "dibujos animados"],
    "cartoon": ["serie animada", "caricatura americana", "cartoon network"],
    "animado": ["animated", "dibujado", "animación"],

    # --- Series (en general) ---
    "serie": ["tv show", "series", "episodios", "temporadas"],
    "temporada": ["season", "t", "cycle"],
    "episodio": ["episode", "capítulo", "ep", "cap"],

    # --- Películas ---
    "pelicula": ["movie", "film", "cine", "largometraje"],
    "actor": ["actor de cine", "film actor", "star"],
    "directo": ["director", "filmmaker", "realizador"],

    # --- Mangas / Manwhuas / Manhuas ---
    "manga": ["japanese comic", "comic japonés", "historieta japonesa"],
    "manhwa": ["korean comic", "comic coreano", "manwhua"],
    "manhua": ["chinese comic", "comic chino", "historieta china"],
    "scan": ["scaneo", "raw", "capítulo escaneado"],

    # --- Web Novels y Novelas ---
    "novela": ["novel", "story book", "literatura"],
    "web novel": ["novela web", "historia online", "light novel"],
    "light novel": ["ln", "novela ligera", "ficción japonesa"],
    "libro": ["book", "ebook", "lectura", "volume"],

    # --- Música ---
    "musica": ["music", "song", "audio", "melodía", "track"],
    "cancion": ["song", "tema", "single"],
    "album": ["disco", "álbum musical", "cd"],
    "artista": ["musician", "cantante", "autor musical"],

    # --- Arte ---
    "arte": ["art", "drawing", "painting", "creación artística"],
    "pintura": ["paint", "artwork", "cuadro"],
    "ilustración": ["illustration", "art digital", "dibujos"],

    # --- Televisión ---
    "television": ["tv", "tele", "canal", "programa tv"],
    "canal": ["channel", "station", "señal tv"],
    "programa": ["show", "tv program", "transmisión"],

    # --- Descargas y Servicios Gratuitos ---
    "gratis_mega": ["mega free", "link mega", "descarga mega", "mega.nz"],
    "gratis_rapidshare": ["rapidshare", "descarga rápida", "host antigua"],
    "gratis_google_drive": ["google drive", "gdrive", "link drive", "drive download"],
    "descarga": ["download", "bajar archivo", "archivo descargable"],

    # --- Libros / PDFs / Lectura ---
    "pdf": ["documento pdf", "archivo pdf", "ebook pdf"],
    "ebook": ["digital book", "libro electrónico", "lectura digital"],
    "biblioteca": ["library", "colección de libros", "book archive"],
}
# =====================================================
# MOTOR PARA GENERAR, CONTRASEÑAS, CON
# =====================================================
class PasswordGeneratorDialog(QDialog):
    """Generador de contraseñas seguras"""
    
    password_generated = QtCore.pyqtSignal(str)  # Señal para enviar contraseña al formulario principal
    
    def __init__(self, parent=None, current_password=""):
        super().__init__(parent)
        self.setWindowTitle("🔐 Generador de Contraseñas Seguras")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        log_message(f"[PasswordGeneratorDialog] 🔐 Generador de Contraseñas Seguras")
        self.setMinimumWidth(500)
        self.setStyleSheet(self.get_stylesheet())
        self.setup_ui(current_password)
    
    # =====================================================

    def get_stylesheet(self):
        """Estilo cyberpunk oscuro"""
        return """
        QDialog {
            background-color: #0d1117;
            color: #e6edf3;
        }
        QGroupBox {
            border: 2px solid #30363d;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            font-weight: bold;
            color: #58a6ff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QLabel {
            color: #8b949e;
            font-size: 12px;
        }
        QLineEdit {
            background-color: #21262d;
            border: 2px solid #30363d;
            border-radius: 6px;
            padding: 10px;
            color: #7ee787;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            font-weight: bold;
        }
        QLineEdit:focus {
            border: 2px solid #58a6ff;
        }
        QSpinBox {
            background-color: #21262d;
            border: 2px solid #30363d;
            border-radius: 4px;
            padding: 5px;
            color: #e6edf3;
            min-width: 60px;
        }
        QCheckBox {
            color: #c9d1d9;
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #30363d;
            background: #21262d;
        }
        QCheckBox::indicator:checked {
            background: #238636;
            border: 2px solid #238636;
        }
        QPushButton {
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 13px;
            border: 2px solid;
        }
        QPushButton#generate_btn {
            background: #1a1a2e;
            border-color: #00ff88;
            color: #00ff88;
        }
        QPushButton#generate_btn:hover {
            background: #00ff88;
            color: #0d1117;
        }
        QPushButton#btn_generate {
            background: #1a1a2e;
            border-color: #80ff00;
            color: #80ff00;
        }
        QPushButton#btn_generate:hover {
            background: #80ff00;
            color: #0a0a0f;
        }
        QPushButton#copy_btn {
            background: #1a1a2e;
            border-color: #58a6ff;
            color: #58a6ff;
        }
        QPushButton#copy_btn:hover {
            background: #58a6ff;
            color: #0d1117;
        }
        QPushButton#use_btn {
            background: #1a1a2e;
            border-color: #f0883e;
            color: #f0883e;
        }
        QPushButton#use_btn:hover {
            background: #f0883e;
            color: #0d1117;
        }
        QPushButton#close_btn {
            background: #21262d;
            border-color: #8b949e;
            color: #8b949e;
        }
        QPushButton#close_btn:hover {
            background: #da3633;
            border-color: #da3633;
            color: white;
        }

        QPushButton#btn_clear {
            background: #1a1a2e;
            border-color: #ff4444;
            color: #ff4444;
        }
        QPushButton#btn_clear:hover {
            background: #ff4444;
            color: white;
        }
        QProgressBar {
            border: 2px solid #30363d;
            border-radius: 5px;
            text-align: center;
            color: #e6edf3;
            font-weight: bold;
        }
        QProgressBar::chunk {
            border-radius: 3px;
        }
        """
    # =====================================================

    def setup_ui(self, current_password):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título decorativo
        title = QLabel("⚡ GENERADOR DE CONTRASEÑAS CRYPTOFILE VAULT")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #00ff88;
            padding: 10px;
            border-bottom: 2px solid #30363d;
        """)
        layout.addWidget(title)
        
        # Sección: Configuración
        config_group = QGroupBox("⚙️ Configuración")
        config_layout = QGridLayout()
        
        # Longitud
        config_layout.addWidget(QLabel("Longitud:"), 0, 0)
        self.length_spin = QSpinBox()
        self.length_spin.setRange(8, 128)
        self.length_spin.setValue(32)
        self.length_spin.setToolTip("Longitud recomendada: 32+ caracteres")
        config_layout.addWidget(self.length_spin, 0, 1)
        
        # Checkboxes para tipos de caracteres
        self.chk_upper = QCheckBox("Mayúsculas (A-Z)")
        self.chk_upper.setChecked(True)
        self.chk_lower = QCheckBox("Minúsculas (a-z)")
        self.chk_lower.setChecked(True)
        self.chk_digits = QCheckBox("Números (0-9)")
        self.chk_digits.setChecked(True)
        self.chk_special = QCheckBox("Especiales (!@#$%)")
        self.chk_special.setChecked(True)
        self.chk_extra = QCheckBox("Extra ({}[]|<>~)")
        self.chk_extra.setChecked(False)
        
        config_layout.addWidget(self.chk_upper, 0, 2)
        config_layout.addWidget(self.chk_lower, 1, 2)
        config_layout.addWidget(self.chk_digits, 2, 2)
        config_layout.addWidget(self.chk_special, 0, 3)
        config_layout.addWidget(self.chk_extra, 1, 3)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Sección: Resultado
        result_group = QGroupBox("🔑 Contraseña Generada")
        result_layout = QVBoxLayout()
        
        self.password_display = QLineEdit()
        self.password_display.setEchoMode(QLineEdit.Password)
        self.password_display.setPlaceholderText("Presiona 'Generar' para crear contraseña...")
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignCenter)
        self.password_display.setMinimumHeight(45)
        
        # Mostrar/Ocultar
        self.chk_show = QCheckBox("Mostrar contraseña")
        self.chk_show.stateChanged.connect(self.toggle_visibility)
        
        # Barra de fortaleza
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(True)
        self.strength_bar.setFormat("Fortaleza: %p%")
        
        result_layout.addWidget(self.password_display)
        result_layout.addWidget(self.chk_show)
        result_layout.addWidget(self.strength_bar)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Sección: Métricas
        self.lbl_metrics = QLabel("Entropía: 0 bits | Combinaciones: 0")
        self.lbl_metrics.setAlignment(Qt.AlignCenter)
        self.lbl_metrics.setStyleSheet("color: #58a6ff; font-family: Consolas;")
        layout.addWidget(self.lbl_metrics)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        self.btn_generate = QPushButton("🎲 GENERAR")
        self.btn_generate.setObjectName("generate_btn")
        self.btn_generate.setMinimumHeight(50)
        self.btn_generate.clicked.connect(self.generate_password)

        # Botón para frase ultra (agregar en phrase_layout)
        self.btn_ultra = QPushButton("🔐 FRASE ULTRA (4 palabras)")
        self.btn_ultra.setObjectName("btn_generate")
        self.btn_ultra.setMinimumHeight(50)
        self.btn_ultra.clicked.connect(lambda: self.generate_passphrase_ultra(4))
        
        self.btn_copy = QPushButton("📋 COPIAR")
        self.btn_copy.setObjectName("copy_btn")
        self.btn_copy.setMinimumHeight(50)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        
        self.btn_use = QPushButton("✅ USAR ESTA")
        self.btn_use.setObjectName("use_btn")
        self.btn_use.setMinimumHeight(50)
        self.btn_use.setToolTip("Enviar contraseña al campo principal")
        self.btn_use.clicked.connect(self.use_password)
        
        self.btn_clean = QPushButton("📋 Limpiar")
        self.btn_clean.setObjectName("btn_clear")
        self.btn_clean.setMinimumHeight(50)
        self.btn_clean.clicked.connect(self.cleaner_hall_P)
        
        self.btn_close = QPushButton("❌ CERRAR")
        self.btn_close.setObjectName("close_btn")
        self.btn_close.setMinimumHeight(40)
        self.btn_close.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_ultra)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_use)
        btn_layout.addWidget(self.btn_clean)
        
        layout.addLayout(btn_layout)
        layout.addWidget(self.btn_close)
        
        # Si hay contraseña actual, mostrarla
        if current_password:
            self.password_display.setText(current_password)
            self.calculate_strength(current_password)
    
    # =====================================================

    def toggle_visibility(self, state):
        if state == Qt.Checked:
            self.password_display.setEchoMode(QLineEdit.Normal)
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
    
    # =====================================================

    def generate_password(self):
        """Genera contraseña segura según configuración"""
        length = self.length_spin.value()
        
        chars = ""
        if self.chk_lower.isChecked():
            chars += string.ascii_lowercase
        if self.chk_upper.isChecked():
            chars += string.ascii_uppercase
        if self.chk_digits.isChecked():
            chars += string.digits
        if self.chk_special.isChecked():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if self.chk_extra.isChecked():
            chars += "`~^\\/"
        
        if not chars:
            QMessageBox.warning(self, "Advertencia", "Selecciona al menos un tipo de carácter")
            log_message("[PasswordGeneratorDialog-generate_password] ↔ ⚠️ Advertencia, \nSelecciona al menos un tipo de carácter")
            return
        
        # Generar con mezcla asegurada
        password = []
        
        # Asegurar al menos uno de cada tipo seleccionado
        if self.chk_lower.isChecked():
            password.append(random.choice(string.ascii_lowercase))
        if self.chk_upper.isChecked():
            password.append(random.choice(string.ascii_uppercase))
        if self.chk_digits.isChecked():
            password.append(random.choice(string.digits))
        if self.chk_special.isChecked():
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Completar el resto
        for _ in range(length - len(password)):
            password.append(random.choice(chars))
        
        # Mezclar
        random.shuffle(password)
        final_password = ''.join(password)
        
        self.password_display.setText(final_password)
        self.calculate_strength(final_password)
    
    # =====================================================

    def calculate_strength(self, password):
        """Calcula y muestra la fortaleza de la contraseña"""
        length = len(password)
        
        # Calcular tamaño del pool de caracteres
        pool = 0
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if has_lower: pool += 26
        if has_upper: pool += 26
        if has_digit: pool += 10
        if has_special: pool += 32
        
        # Entropía: L * log2(R)
        import math
        entropy = length * math.log2(pool) if pool > 0 else 0
        
        # Score visual (0-100)
        score = min(100, int((entropy / 128) * 100))
        
        self.strength_bar.setValue(score)
        
        # Color según fortaleza
        if score < 40:
            color = "#da3633"  # Rojo
            text = "DÉBIL"
        elif score < 70:
            color = "#f0883e"  # Naranja
            text = "MEDIA"
        elif score < 90:
            color = "#58a6ff"  # Azul
            text = "FUERTE"
        else:
            color = "#00ff88"  # Verde
            text = "EXCELENTE"
        
        self.strength_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        self.strength_bar.setFormat(f"Fortaleza: {text} ({score}%)")
        
        # Actualizar métricas
        combinations = pool ** length
        self.lbl_metrics.setText(
            f"Entropía: {entropy:.1f} bits | Combinaciones: {self.format_number(combinations)}"
        )
    
    # =====================================================

    def format_number(self, n):
        """Formatea números grandes legiblemente"""
        if n > 1e24:
            return f"{n:.2e}"
        elif n > 1e12:
            return f"{n/1e12:.1f} trillones"
        elif n > 1e6:
            return f"{n/1e6:.1f} millones"
        else:
            return f"{n:,}"
    
    # =====================================================

    def copy_to_clipboard(self):
        """Copia al portapapeles"""
        password = self.password_display.text()
        if password:
            try:
                pyperclip.copy(password)
                QMessageBox.information(self, "Éxito", "Contraseña copiada al portapapeles")
                log_message("[PasswordGeneratorDialog-copy_to_clipboard] ↔ 🎉 Éxito, Contraseña \ncopiada al portapapeles")
            except:
                # Fallback si pyperclip falla
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(password)
                QMessageBox.information(self, "Éxito", "Contraseña copiada al portapapeles")
                log_message("[PasswordGeneratorDialog-copy_to_clipboard] ↔ 🎉 Éxito, Contraseña \ncopiada al portapapeles")

    # =====================================================

    def use_password(self):
        """Emite la señal con la contraseña para usar en el formulario principal"""
        password = self.password_display.text()
        if password:
            self.password_generated.emit(password)
            self.accept()
        else:
            QMessageBox.warning(self, "Advertencia", "Genera una contraseña primero")
            log_message("[PasswordGeneratorDialog-use_password] ↔ ⚠️ Advertencia, Genera una contraseña primero")

    # =====================================================

    def generate_passphrase_ultra(self, num_palabras=4):
        """
        Genera frase ultra-entropía usando múltiples capas de semántica + PBKDF2HMAC.
        Útil para contraseñas maestras o seeds de recuperación.
        """
        self.cleaner_hall_P()
        
        # Usar PBKDF2HMAC para determinar qué categorías usar (determinístico pero aleatorio)
        salt = secrets.token_bytes(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=num_palabras * 2,
            salt=salt,
            iterations=480000,
            backend=default_backend()
        )
        derived = kdf.derive(secrets.token_bytes(64))
        
        todas_las_categorias = list(SEMANTIC_DICT_GENERAL.keys())
        palabras_seleccionadas = []
        
        for i in range(num_palabras):
            # Usar bytes derivados para seleccionar categoría
            categoria_idx = derived[i*2] % len(todas_las_categorias)
            categoria = todas_las_categorias[categoria_idx]
            
            # Seleccionar sinónimo de esa categoría
            sinonimos = SEMANTIC_DICT_GENERAL[categoria]
            palabra_idx = derived[i*2 + 1] % len(sinonimos)
            palabra = sinonimos[palabra_idx]
            
            # Limpiar
            palabra_limpia = palabra.replace(" ", "-").replace("_", "-")
            palabras_seleccionadas.append(palabra_limpia)
        
        # Entropía adicional para separadores y casing
        sep_opciones = ["-", "_", ".", "!", "@", "#", "$"]
        separador = sep_opciones[derived[num_palabras*2 - 1] % len(sep_opciones)]
        
        # Mezclar casing aleatoriamente
        palabras_finales = []
        for i, palabra in enumerate(palabras_seleccionadas):
            if secrets.randbelow(2) == 0:
                palabras_finales.append(palabra.upper())
            else:
                palabras_finales.append(palabra.lower())
        
        passphrase = separador.join(palabras_finales)
        
        # Añadir sufijo entropía PBKDF2HMAC
        numero = 1000 + (derived[-2] % 9000)  # 4 dígitos
        passphrase = f"{passphrase}{separador}{numero}"
        
        self.password_display.setText(passphrase)
        #self.check_input.setText(passphrase)
        
        # Entropía: log2(180 categorías * 10 sinónimos promedio ^ num_palabras)
        import math
        entropy = math.log2(len(todas_las_categorias)) + (num_palabras * math.log2(10))
        QMessageBox.information(self, "Aviso", 
            f"🔐 Ultra-Frase [{num_palabras} palabras] | Entropía: ~{entropy:.1f} bits | "
            f"PBKDF2HMAC: 480k iters"
        )

        log_message(
            f"🔐 Ultra-Frase [{num_palabras} palabras] | Entropía: ~{entropy:.1f} bits | "
            f"PBKDF2HMAC: 480k iters"
        )


    def cleaner_hall_P(self):

        self.password_display.setText("")
        self.strength_bar.setFormat(f"0%")
        self.strength_bar.setValue(0)

# =====================================================
# MOTOR DE ENCRIPTACIÓN
# =====================================================
class CryptoEngine:
    @staticmethod
    def derive_key(password, salt=None):
        """Deriva una clave Fernet desde una contraseña usando PBKDF2HMACHMAC"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    # =====================================================

    @staticmethod
    def encrypt_file(file_path, password, output_path=None):
        """
        Encripta un archivo individual
        Retorna: (éxito, ruta_salida, mensaje)
        """
        try:
            # Generar salt y derivar clave
            key, salt = CryptoEngine.derive_key(password)
            fernet = Fernet(key)
            
            # Leer archivo original
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encriptar datos
            encrypted_data = fernet.encrypt(data)
            
            # Formato: [SALT(16 bytes)][DATOS_ENCRIPTADOS]
            final_data = salt + encrypted_data
            
            # Determinar nombre de salida
            if output_path is None:
                base_name = os.path.splitext(file_path)[0]
                output_path = base_name + '.dat'
            
            # Guardar archivo encriptado
            with open(output_path, 'wb') as f:
                f.write(final_data)
            
            return True, output_path, "Encriptación exitosa"
            
        except Exception as e:
            log_message(f"[encrypt_file-Exception] [✘] Error: {str(e)}")
            return False, None, f"Error: {str(e)}"
    
    # =====================================================

    @staticmethod
    def decrypt_file(file_path, password, output_path=None, original_name=None):
        """
        Desencripta un archivo .dat
        Retorna: (éxito, ruta_salida, mensaje)
        """
        try:
            # Leer archivo encriptado
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Extraer salt (primeros 16 bytes)
            if len(data) < 16:
                return False, None, "Archivo corrupto o inválido"
            
            salt = data[:16]
            encrypted_data = data[16:]
            
            # Derivar clave y desencriptar
            key, _ = CryptoEngine.derive_key(password, salt)
            fernet = Fernet(key)
            
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Determinar nombre de salida
            if output_path is None:
                if original_name:
                    output_path = original_name
                else:
                    base_name = os.path.splitext(file_path)[0]
                    output_path = base_name + '_decrypted'
            
            # Guardar archivo desencriptado
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            return True, output_path, "Desencriptación exitosa"
            
        except InvalidToken:
            log_message(f"[decrypt_file-InvalidToken] [✘] Clave incorrecta o archivo corrupto")
            return False, None, "Clave incorrecta o archivo corrupto"
            
        except Exception as e:
            log_message(f"[decrypt_file-Exception] [✘] Error: {str(e)}")
            return False, None, f"Error: {str(e)}"

# =====================================================
# WORKER PARA OPERACIONES EN SEGUNDO PLANO
# =====================================================
class CryptoWorker(QThread):
    progress = pyqtSignal(int, int, str)  # current, total, filename
    finished = pyqtSignal(bool, str, int)  # success, message, count
    log = pyqtSignal(str)
    
    def __init__(self, operation, files, password, output_dir=None, path_dir_raiz_carpeta="", original_names=None):
        super().__init__()
        self.operation = operation  # 'encrypt_files_samples' o 'encrypt_files_directory' o 'decrypt'
        self.files = files
        self.password = password
        self.output_dir = output_dir
        self.original_names = original_names or {}
        self.path_dir_raiz_carpeta = path_dir_raiz_carpeta
    
    # =====================================================

    def run(self):
        try:
            if self.operation == 'encrypt':
                self.encrypt_files_samples()

            elif self.operation == 'encrypt_grup':
                self.encrypt_files_directory()

            elif self.operation == 'decrypt':
                self.decrypt_files()

        except Exception as e:
            self.finished.emit(False, str(e), 0)
    
    # =====================================================

    def encrypt_files_samples(self):
        total = len(self.files)
        success_count = 0
        
        # Si hay múltiples archivos, crear ZIP primero
        if total > 1:
            self.log.emit("📦 Creando archivo ZIP temporal...")
            log_message("[encrypt_files_samples] ↔ 📦 Creando archivo ZIP temporal...")
            
            # Crear ZIP temporal
            temp_zip = os.path.join(self.output_dir or os.path.dirname(self.files[0]), 
                                   "temp_vault.zip") 

            print(f'\nEste es el Directorio Temporal *.ZIP:  ---> {temp_zip}')
            print(f'Esta es laLista de Archivos:  ---> {self.files}\n')

            # Llamar el método (sin el self.path_dir_raiz_carpeta porque es para archivos, no directorios)
            msn = self.create_encrypted_zip(temp_zip)
            
            if not msn:
                self.finished.emit(False, "Error al crear ZIP", 0)
                return
            
            # Encriptar el ZIP
            self.progress.emit(1, 2, "Encriptando archivo ZIP...")
            
            output_path = os.path.join(self.output_dir or os.path.dirname(temp_zip), 
                                      "vault_encrypted.dat")
            
            success, result_path, msg = CryptoEngine.encrypt_file(
                temp_zip, self.password, output_path
            )
            
            # Eliminar ZIP temporal
            try:
                os.remove(temp_zip)
            except:
                pass
            
            if success:
                success_count = 1
                log_message(f"[encrypt_files_samples ...] ↔ 🎉 Encriptación exitosa con (Fernet")

                self.log.emit(f"✅ Encriptado: {os.path.basename(result_path)}")
                log_message(f"[encrypt_files_samples] ↔ ✅ Encriptado: {os.path.basename(result_path)}")
            else:
                self.log.emit(f"❌ Error: {msg}")
                log_message(f"[encrypt_files_samples] ↔ ❌ Error: {msg}")
                
        else:
            # Archivo individual
            for i, file_path in enumerate(self.files):
                self.progress.emit(i + 1, total, os.path.basename(file_path))
                
                output_path = None
                if self.output_dir:
                    output_path = os.path.join(self.output_dir, 
                                              os.path.splitext(os.path.basename(file_path))[0] + '.dat')
                
                success, result_path, msg = CryptoEngine.encrypt_file(
                    file_path, self.password, output_path
                )
                
                if success:
                    success_count += 1
                    log_message(f"[encrypt_files_samples ...] ↔ 🎉 Encriptación exitosa con (Fernet")
                    self.log.emit(f"✅ Encriptado: {os.path.basename(result_path)}")
                    log_message(f"[encrypt_files_samples] ↔ ✅ Encriptado: {os.path.basename(result_path)}")
                else:
                    self.log.emit(f"❌ Error en {os.path.basename(file_path)}: {msg}")
                    log_message(f"[encrypt_files_samples] ↔ ❌ Error en {os.path.basename(file_path)}: {msg}")
        
        self.finished.emit(True, f"Proceso completado", success_count)
    
    # =====================================================

    def encrypt_files_directory(self):
        global root_dir

        total = len(self.files)
        success_count = 0
        
        # Si hay múltiples archivos, crear ZIP primero
        if total > 1:
            self.log.emit("📦 Creando archivo ZIP temporal...")
            log_message(f"[encrypt_files_directory] ↔ 📦 Creando archivo ZIP temporal...")
            
            # Crear ZIP temporal
            temp_zip = os.path.join(self.output_dir or os.path.dirname(self.files[0]), 
                                   "temp_vault.zip") 

            print(f'\nEste es el Directorio Temporal *.ZIP:  ---> {temp_zip}')
            print(f'Este es el Directorio Principal:  ---> {self.path_dir_raiz_carpeta}\n')

            msn = self.compress_to_ZIP(temp_zip)
            
            if not msn:
                self.finished.emit(False, "Error al crear ZIP", 0)
                return
            
            # Encriptar el ZIP
            self.progress.emit(1, 2, "Encriptando archivo ZIP...")
            
            output_path = os.path.join(self.output_dir or os.path.dirname(temp_zip), 
                                      "vault_encrypted.dat")
            
            success, result_path, msg = CryptoEngine.encrypt_file(
                temp_zip, self.password, output_path
            )
            
            # Eliminar ZIP temporal
            try:
                os.remove(temp_zip)
            except:
                pass
            
            if success:
                success_count = 1
                log_message(f"[encrypt_files_samples ...] ↔ 🎉 Encriptación exitosa con (Fernet")
                self.log.emit(f"✅ Encriptado: {os.path.basename(result_path)}")
                log_message(f"[encrypt_files_directory] ↔ ✅ Encriptado: {os.path.basename(result_path)}")
            else:
                self.log.emit(f"❌ Error: {msg}")
                log_message(f"[encrypt_files_directory] ↔ ❌ Error: {msg}")
                
        else:
            # Archivo individual
            for i, file_path in enumerate(self.files):
                self.progress.emit(i + 1, total, os.path.basename(file_path))
                
                output_path = None
                if self.output_dir:
                    output_path = os.path.join(self.output_dir, 
                                              os.path.splitext(os.path.basename(file_path))[0] + '.dat')
                
                success, result_path, msg = CryptoEngine.encrypt_file(
                    file_path, self.password, output_path
                )
                
                if success:
                    success_count += 1
                    log_message(f"[encrypt_files_samples ...] ↔ 🎉 Encriptación exitosa con (Fernet")
                    self.log.emit(f"✅ Encriptado: {os.path.basename(result_path)}")
                    log_message(f"[encrypt_files_directory] ↔ ✅ Encriptado: {os.path.basename(result_path)}")
                else:
                    self.log.emit(f"❌ Error en {os.path.basename(file_path)}: {msg}")
                    log_message(f"[encrypt_files_directory] ↔ ❌ Error en {os.path.basename(file_path)}: {msg}")
        
        self.finished.emit(True, f"Proceso completado", success_count)
    
    # =====================================================
    # MÉTODO decrypt_files() con soporte ZIP password ↔ CON CONTRASEÑA AES-256
    # =====================================================
    def decrypt_files(self):
        """
        Desencripta archivos .dat y extrae ZIPs protegidos con contraseña
        """
        total = len(self.files)
        success_count = 0
        
        for i, file_path in enumerate(self.files):
            self.progress.emit(i + 1, total, os.path.basename(file_path))
            
            try:
                # Crear archivo temporal para el ZIP desencriptado
                temp_dir = os.path.dirname(file_path)
                temp_zip = os.path.join(temp_dir, f"temp_decrypt_{int(time.time())}.zip")
                
                # Desencriptar el .dat (capa Fernet)
                original_name = self.original_names.get(file_path)
                success, result_path, msg = CryptoEngine.decrypt_file(
                    file_path, self.password, temp_zip, original_name
                )
                
                if not success:
                    self.log.emit(f"❌ Error desencriptando {os.path.basename(file_path)}: {msg}")
                    log_message(f"[decrypt_files] ↔ ❌ Error: {msg}")
                    # Limpiar temporal si existe
                    if os.path.exists(temp_zip):
                        os.remove(temp_zip)
                    continue
                
                # Verificar si es un ZIP (por firma mágica)
                if self.is_zip_file(temp_zip):
                    self.log.emit(f"📂 Detectado archivo ZIP, extrayendo contenido...")
                    log_message(f"[decrypt_files] ↔ 📂 ZIP detectado, extrayendo...")
                    
                    # Crear carpeta de salida
                    extract_dir = os.path.join(self.output_dir or os.path.dirname(file_path), 
                                              "Desencriptados")
                    os.makedirs(extract_dir, exist_ok=True)
                    
                    # Intentar extraer con pyzipper (AES-256) primero
                    extracted = self._extract_zip_with_password(temp_zip, extract_dir, self.password)
                    
                    if extracted:
                        success_count += 1

                        ##=================================================================

                        # Construir el árbol completo de Extracción, para los LOG´s
                        folder = Path.resource_path(f"{extract_dir}")
                        log_message(f"📌 Directorio Principal: 📂 {folder}")

                        # Usar os.walk para recorrer todo el árbol
                        # Ordenamos para mantener consistencia alfabética
                        for dirpath, dirnames, filenames in os.walk(folder):
                            # Ordenar directorios y archivos alfabéticamente
                            dirnames.sort()
                            filenames.sort()
                            
                            # Calcular el nivel de profundidad (nivel 0 = raíz)
                            relative_path = os.path.relpath(dirpath, folder)
                            if relative_path == ".":
                                level = 0
                            else:
                                level = relative_path.count(os.sep) + 1
                            
                            # Indentación: 1 tabulación por nivel
                            indent = "\t" * level
                            
                            # Si no es el directorio raíz, mostrarlo como sub-directorio
                            if level > 0:
                                current_dir_name = os.path.basename(dirpath)                    
                                log_message(f"{indent}➜ Sub-Directorio: \"📂 {current_dir_name}\"  ||  👀 Y Dentro Hay:")
                            
                            # Listar archivos en este directorio (si hay)
                            if filenames:
                                file_indent = "\t" * (level + 1)
                                for filename in filenames:
                                    # Extraer extensión
                                    _, ext = os.path.splitext(filename)
                                    if ext:
                                        ext_display = ext.lower()
                                    else:
                                        ext_display = "sin_ext"
                                                            
                                    log_message(f"{file_indent}•  {filename} [⭐{ext_display}]")

                        ##=================================================================

                        self.log.emit(f"✅ Extraídos {len(extracted)} archivos en: {extract_dir}")
                        log_message(f"[decrypt_files] ↔ ✅ {len(extracted)} archivos extraídos")
                        
                        # Listar archivos extraídos
                        for name in extracted:
                            self.log.emit(f"  → {name}")
                            
                    else:
                        # Fallback: intentar sin contraseña (ZIPs antiguos)
                        try:
                            with zipfile.ZipFile(temp_zip, 'r') as zipf:
                                zipf.extractall(extract_dir)
                                extracted = zipf.namelist()
                                success_count += 1
                                self.log.emit(f"✅ Extraídos {len(extracted)} archivos (sin pass)")
                        except Exception as e2:
                            self.log.emit(f"❌ Error extrayendo ZIP: {str(e2)}")
                            log_message(f"[decrypt_files] ↔ ❌ Error ZIP: {str(e2)}")
                    
                    # Limpiar temporal
                    try:
                        os.remove(temp_zip)
                    except:
                        pass
                        
                else:
                    # Archivo individual (no es ZIP)
                    final_path = result_path
                    if self.output_dir:
                        if original_name:
                            final_name = original_name
                        else:
                            final_name = os.path.basename(file_path).replace('.dat', '')
                        final_path = os.path.join(self.output_dir, final_name)
                        if os.path.exists(final_path):
                            os.remove(final_path)
                        os.rename(result_path, final_path)
                    
                    success_count += 1
                    self.log.emit(f"✅ Desencriptado: {os.path.basename(final_path)}")
                    log_message(f"[decrypt_files] ↔ ✅ Archivo: {os.path.basename(final_path)}")
                    
            except Exception as e:
                self.log.emit(f"❌ Error inesperado: {str(e)}")
                log_message(f"[decrypt_files] ↔ ❌ Error: {str(e)}")
                # Limpiar temporal si existe
                if 'temp_zip' in locals() and os.path.exists(temp_zip):
                    try:
                        os.remove(temp_zip)
                    except:
                        pass
        
        self.finished.emit(True, f"Proceso completado", success_count)

    # =====================================================

    # Intentar extraer con pyzipper (AES-256)
    def _extract_zip_with_password(self, zip_path, extract_dir, password):
        """
        Extrae ZIP protegido con contraseña usando pyzipper o zipfile
        """
        extracted_files = []
        
        # Intentar con pyzipper (AES) primero
        if ZIP_PASSWORD_AVAILABLE:
            try:
                with pyzipper.AESZipFile(zip_path, 'r') as zipf:
                    # Establecer contraseña
                    zipf.setpassword(password.encode('utf-8'))
                    
                    # Listar y extraer
                    file_list = zipf.namelist()
                    zipf.extractall(extract_dir)
                    extracted_files = file_list
                    self.log.emit(f"🔓 Desencriptado con (AES-256)")
                    log_message(f"[decrypt_files_extract ...] ↔ 🔓 Desencriptado con (AES-256)")
                    return extracted_files
                    
            except RuntimeError as e:
                # Contraseña incorrecta o no es AES
                self.log.emit(f"⚠️ pyzipper: {str(e)}")
                log_message(f"[decrypt_files_extract ...] ↔ ⚠️ pyzipper: {str(e)}")
            except Exception as e:
                self.log.emit(f"⚠️ pyzipper falló: {str(e)}")
                log_message(f"[decrypt_files_extract ...] ↔ ⚠️ pyzipper falló: {str(e)}")
        
        # Intentar con zipfile estándar
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                if password:
                    zipf.setpassword(password.encode('utf-8'))
                
                file_list = zipf.namelist()
                zipf.extractall(extract_dir)
                extracted_files = file_list
                return extracted_files
                
        except Exception as e:
            self.log.emit(f"❌ No se pudo extraer: {str(e)}")
            log_message(f"[decrypt_files_extract ...] ↔ ❌ No se pudo extraer: {str(e)}")
            return None
    
    def is_zip_file(self, file_path):
        """Verifica si un archivo es ZIP por su firma mágica"""
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(4)
                return magic == b'PK\x03\x04'
        except:
            return False

##=========================================================================================================

##====================================================================================
# --- Metodo, que Crea un Archivo ZIP, sin Gerarquia de Arbol, pero cifrado con ↔ PYZIPPER (AES-256)
##====================================================================================
    def create_encrypted_zip(self, temp_zip):
        """
        Crea ZIP de archivos individuales con contraseña opcional
        """
        self.log.emit(f"DEBUG: password exists={bool(self.password)}, ZIP_AVAILABLE={ZIP_PASSWORD_AVAILABLE}")
        log_message(f"DEBUG: password exists={bool(self.password)}, ZIP_AVAILABLE={ZIP_PASSWORD_AVAILABLE}")
        try:
            # ========== OPCIÓN A: PYZIPPER (AES-256) ==========
            if self.password and ZIP_PASSWORD_AVAILABLE:
                with pyzipper.AESZipFile(
                    temp_zip,
                    mode="w",
                    compression=pyzipper.ZIP_DEFLATED,
                    encryption=pyzipper.WZ_AES
                ) as zipf:
                    
                    password_bytes = self.password.encode('utf-8')
                    zipf.setpassword(password_bytes)
                    
                    for file_path in self.files:
                        arcname = os.path.basename(file_path)
                        zipf.write(file_path, arcname)
                        self.log.emit(f"  → Agregado (AES-256): {arcname} ↔ [Cifrado]")
                        log_message(f"[create_encrypted_zip] ↔ → Agregado (AES-256): {arcname} ↔ [Cifrado]")
                
                self.log.emit(f"🔐 ZIP con AES-256 creado: {os.path.basename(temp_zip)}")
                log_message(f"[create_encrypted_zip] ↔ 🔐 ZIP con AES-256 creado: {os.path.basename(temp_zip)}")
                return temp_zip

            # ========== OPCIÓN B: PYMINIZIP (contraseña ZIP estándar) ==========
            elif self.password and PYMINIZIP_AVAILABLE:
                self.log.emit("🔐 Usando pyminizip (compatibilidad máxima)")
                log_message(f"[create_encrypted_zip] ↔ 🔐 Usando pyminizip (compatibilidad máxima)")
                
                # pyminizip necesita lista de nombres de archivo y prefijos
                arcnames = [os.path.basename(f) for f in self.files]
                
                pyminizip.compress_multiple(
                    self.files,                  # lista de rutas completas
                    arcnames,               # nombres dentro del ZIP
                    temp_zip,               # archivo salida
                    self.password,           # contraseña
                    5                       # nivel compresión (1-9)
                )
                
                self.log.emit(f"🔐 ZIP con contraseña creado [Estandar]: {os.path.basename(temp_zip)}")
                log_message(f"[create_encrypted_zip] ↔ 🔐 ZIP con contraseña creado [Estandar]: {os.path.basename(temp_zip)}")
                return temp_zip

            # ========== OPCIÓN C: SIN CONTRASEÑA ==========
            else:
                if self.password and not ZIP_PASSWORD_AVAILABLE and not PYMINIZIP_AVAILABLE:
                    self.log.emit("⚠️ Sin librería de cifrado. Instale: pip install pyzipper")
                    log_message(f"[create_encrypted_zip] ↔ ⚠️ Sin librería de cifrado. Instale: pip install pyzipper")
                
                with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in self.files:
                        arcname = os.path.basename(file_path)
                        zipf.write(file_path, arcname)
                        self.log.emit(f"  → Agregado [Sin-Cifrar]: {arcname}")
                        log_message(f"[create_encrypted_zip] ↔ → Agregado [Sin-Cifrar]: {arcname}")
                
                return temp_zip

        except Exception as e:
            error_msg = f"Error creando ZIP: {str(e)}"
            self.log.emit(f"❌ {error_msg}")
            log_message(f"[create_encrypted_zip] ↔ ❌ {error_msg}")
            return None

##=========================================================================================================

##====================================================================================
# --- Metodo, que Crea un Archivo ZIP, Con Gerarquia de Arbol, pero cifrado con ↔ PYZIPPER (AES-256)
##====================================================================================
    def compress_to_ZIP(self, outputPath):
        """
        Comprime directorios a ZIP con contraseña AES opcional
        """
        global root_dir

        self.log.emit(f"DEBUG: password exists={bool(self.password)}, ZIP_AVAILABLE={ZIP_PASSWORD_AVAILABLE}")
        log_message(f"DEBUG: password exists={bool(self.password)}, ZIP_AVAILABLE={ZIP_PASSWORD_AVAILABLE}")

        root_dir = self.path_dir_raiz_carpeta
        
        if not root_dir:
            return None

        Directory_P = outputPath.replace("\\", "/")

        try:
            # Usar pyzipper si hay contraseña y está disponible
            if self.password and ZIP_PASSWORD_AVAILABLE:

                with pyzipper.AESZipFile(
                    Directory_P, 
                    mode="w", 
                    compression=pyzipper.ZIP_DEFLATED,
                    encryption=pyzipper.WZ_AES
                ) as zipf:
                    
                    # Establecer contraseña
                    password_bytes = self.password.encode('utf-8')
                    zipf.setpassword(password_bytes)
                    
                    # === AÑADIR ARCHIVOS DIRECTAMENTE (sin método auxiliar) ===
                    for dirpath, dirnames, filenames in os.walk(root_dir):
                        dirnames.sort()
                        filenames.sort()

                        for filename in filenames:
                            full_path = os.path.join(dirpath, filename)
                            arcname = os.path.relpath(full_path, root_dir)

                            try:
                                zipf.write(full_path, arcname)
                                self.log.emit(f"  → Agregado (AES-256): {arcname} ↔ [Cifrado]")
                                log_message(f"[compress_to_ZIP] ↔ → Agregado (AES-256): {arcname} ↔ [Cifrado]")
                            except Exception as e:
                                self.log.emit(f"  ⚠️ Error: {arcname} - {str(e)}")
                                log_message(f"[compress_to_ZIP] ↔ ⚠️ Error: {arcname}")
                    
            elif self.password and not ZIP_PASSWORD_AVAILABLE:
                # Fallback: ZIP estándar con contraseña (ZipCrypto - débil)
                self.log.emit("⚠️ Usando ZIP estándar (instala pyzipper para AES)")
                log_message("[compress_to_ZIP] ↔ ⚠️ ZIP estándar (cifrado débil)")
                
                with zipfile.ZipFile(Directory_P, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
                    for dirpath, dirnames, filenames in os.walk(root_dir):
                        dirnames.sort()
                        filenames.sort()

                        for filename in filenames:
                            full_path = os.path.join(dirpath, filename)
                            arcname = os.path.relpath(full_path, root_dir)

                            try:
                                zipf.write(full_path, arcname)
                                self.log.emit(f"  → Agregado [Estandar CF-Debil]: {arcname}")
                                log_message(f"[compress_to_ZIP] ↔ → Agregado [Estandar CF-Debil]: {arcname}")
                            except Exception as e:
                                self.log.emit(f"  ⚠️ Error: {arcname}")
                                log_message(f"[compress_to_ZIP] ↔ ⚠️ Error: {arcname}")
                                
            else:
                # Sin contraseña (comportamiento original)
                with zipfile.ZipFile(Directory_P, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
                    for dirpath, dirnames, filenames in os.walk(root_dir):
                        dirnames.sort()
                        filenames.sort()

                        for filename in filenames:
                            full_path = os.path.join(dirpath, filename)
                            arcname = os.path.relpath(full_path, root_dir)

                            try:
                                zipf.write(full_path, arcname)
                                self.log.emit(f"  → Agregado [Sin-Cifrar]: {arcname}")
                                log_message(f"[compress_to_ZIP] ↔ → Agregado [Sin-Cifrar]: {arcname}")
                            except Exception as e:
                                self.log.emit(f"  ⚠️ Error: {arcname}")
                                log_message(f"[compress_to_ZIP] ↔ ⚠️ Error: {arcname}")

            self.log.emit(f"✅ ZIP creado: {os.path.basename(Directory_P)}")
            log_message(f"[compress_to_ZIP] ↔ ✅ ZIP creado: {os.path.basename(Directory_P)}")

            if self.password:
                self.log.emit(f"🔐 Protegido con contraseña [AES-256]")
                log_message(f"[compress_to_ZIP] ↔🔐 Protegido con contraseña [AES-256]")
            
            return Directory_P

        except Exception as e:
            error_msg = f"Error creando ZIP: {str(e)}"
            self.log.emit(f"❌ {error_msg}")
            log_message(f"[compress_to_ZIP] ↔ ❌ {error_msg}")
            return None

# =====================================================
# MAIN APPLICATION
# =====================================================
class CryptoFileVault(QWidget):
    def __init__(self):
        super().__init__()

        self.LogFile = Path.resource_path(LogFile())
        print(f"Path Log File: --->>>  {self.LogFile}")

        
        self.files = []
        self.list_files_andP = []
        self.worker = None
        self.path_dir_raiz_carpeta = ""
        self.dir_path_Resumen = ""

        self.visor_1 = True
        self.visor_2 = False
        self.added = 0
        self.invisor = False
        
        self.setWindowTitle("✨ CryptoFile Vault V-05 ✨")
        
        # Icono
        self.setWindowIcon(QtGui.QIcon(":/imagenes/Resources/1.png"))
        
        self.center_on_screen()
        self.init_ui()
        
        self.add_log("╔══════════════════════════════════════╗")
        self.add_log("║    CryptoFile Vault V-05 Iniciado    ║")
        self.add_log("║    Sistema de Encriptación Listo     ║")
        self.add_log("╚══════════════════════════════════════╝")

        log_message(f"╔══════════════════════════════════════╗")
        log_message(f"║                        CryptoFile Vault V-05 Iniciado                 ║")
        log_message(f"║                        Sistema de Encriptación Listo                  ║")
        log_message(f"╚══════════════════════════════════════╝")
        
        if not CRYPTO_AVAILABLE:
            self.add_log("⚠️ ADVERTENCIA: Instala 'cryptography'")
            self.add_log("   pip install cryptography")

            log_message(f"⚠️ ADVERTENCIA: Instala 'cryptography'")
            log_message(f"   pip install cryptography")
        
        self.show_app_info()

	# =====================================================
	# UI - COMPACT FRONT V-05
	# =====================================================
    def init_ui(self):
        self.setStyleSheet("""
            QWidget{
                background:#0a0a0f;
                color:white;
                font-size:12px;
                font-family:'Segoe UI', Arial;
            }

            QPushButton{
                background:#1a1a2e;
                color:white;
                border:1px solid #00c3ff;
                border-radius:6px;
                padding:6px 10px;
                min-height:28px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#00c3ff;
                color:black;
            }

            QPushButton:pressed{
                background:#0099cc;
            }

            QPushButton#danger{
                border:1px solid #ff4444;
            }

            QPushButton#danger:hover{
                background:#ff4444;
                color:white;
            }

            QPushButton#btnLOGs{
                background:#1a1a2e;
                color:white;
                border:1px solid #ff4444;
                border-radius:6px;
                padding:6px 10px;
                min-height:28px;
                font-weight:bold;
            }

            QPushButton#btnLOGs:hover{
                background:#ffff00;
                color:black;
            }

            QPushButton#success{
                border:1px solid #80ff00;
                color:#80ff00;
            }

            QPushButton#success:hover{
                background:#80ff00;
                color:black;
            }

            QPushButton#decrypt{
                border:1px solid #00c3ff;
                color:#00c3ff;
            }

            QPushButton#decrypt:hover{
                background:#00c3ff;
                color:black;
            }

            QListWidget,
            QTextEdit,
            QLineEdit{
                background:#111118;
                color:#b164ff;
                border:1px solid #333;
                border-radius:5px;
                padding:4px;
            }

            QLineEdit:focus{
                border:1px solid #00c3ff;
            }

            QLineEdit#password{
                color:#80ff00;
                font-family:monospace;
            }

            QListWidget{
                selection-background-color:#1a1a2e;
                selection-color:#00c3ff;
            }

            QGroupBox{
                border:1px solid #00c3ff;
                border-radius:7px;
                margin-top:8px;
                padding:7px;
                font-weight:bold;
                color:#00c3ff;
            }

            QGroupBox::title{
                subcontrol-origin:margin;
                left:10px;
                padding:0 6px;
                background:#0a0a0f;
            }

            QProgressBar{
                border:1px solid #00c3ff;
                border-radius:5px;
                text-align:center;
                color:white;
                background:#111118;
                min-height:16px;
                max-height:18px;
            }

            QProgressBar::chunk{
                background:qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:0,
                    stop:0 #00c3ff,
                    stop:1 #80ff00
                );
                border-radius:4px;
            }

            QLabel{
                color:#cccccc;
            }

            QLabel#title{
                color:#00c3ff;
                font-size:18px;
                font-weight:bold;
            }

            QLabel#subtitle{
                color:#888888;
                font-size:10px;
            }

            QCheckBox{
                color:#888888;
            }

            QCheckBox::indicator{
                width:14px;
                height:14px;
            }

            QScrollBar:vertical{
                background:#111118;
                width:10px;
                margin:0;
            }

            QScrollBar::handle:vertical{
                background:#00c3ff;
                min-height:30px;
                border-radius:5px;
            }

            QScrollBar::handle:vertical:hover{
                background:#80ff00;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical{
                height:0px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título principal
        header = QHBoxLayout()
        title = QLabel("🔐 CryptoFile Vault")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        header.addWidget(title)
        layout.addLayout(header)

        subtitle = QLabel("Encriptación Segura para Cualquier Archivo")
        subtitle.setObjectName("subtitle")
        subtitle.setStyleSheet('''
            QLabel{
                color:#00c3ff;
                font-size:10px;
                font-weight:bold;
            }
            ''')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        self.SubDirecty = QLabel("Directorio de Archivos: -> ")
        self.SubDirecty.setObjectName("subtitle")
        self.SubDirecty.setStyleSheet('''
            QLabel{
                background-color: #0a0a0a;
                color: #00ff41;
                font-size: 14px;
            }
            ''')
        self.SubDirecty.setAlignment(Qt.AlignCenter)
        self.SubDirecty.hide()
        layout.addWidget(self.SubDirecty)
        
        # ==========================================
        # SECCIÓN: Selección de Archivos
        # ==========================================
        files_group = QGroupBox("📁 Archivos a Procesar")
        files_layout = QVBoxLayout()
        
        # Botones de selección
        btns_layout = QHBoxLayout()

        self.btn_files = QPushButton("📄 Agregar Archivos")
        self.btn_folder = QPushButton("📁 Agregar Carpeta")
        self.btn_VPD = QPushButton("📁 Vista Previa Directorio?")
        self.btn_VPD.hide()

        self.btn_clear = QPushButton("🗑️ Limpiar Lista")
        self.btn_clear.setObjectName("danger")

        self.btn_LOGs = QPushButton("📁 Leer Log´s?")
        self.btn_LOGs.setObjectName("btnLOGs")

        btns_layout.addWidget(self.btn_files)
        btns_layout.addWidget(self.btn_folder)
        btns_layout.addWidget(self.btn_VPD)
        btns_layout.addStretch()
        btns_layout.addWidget(self.btn_clear)
        btns_layout.addWidget(self.btn_LOGs)

        files_layout.addLayout(btns_layout)
        
        # Lista de archivos
        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(120)
        files_layout.addWidget(self.list_widget)
        
        # Info de archivos
        self.lbl_file_info = QLabel("Archivos: 0 | Tamaño total: 0 MB")
        self.lbl_file_info.setStyleSheet("color:#888;")
        files_layout.addWidget(self.lbl_file_info)

        files_group.setLayout(files_layout)
        layout.addWidget(files_group)

        # =================================================
        # CLAVE + DIRECTORIO EN UNA SOLA FILA
        # =================================================
        security_output_layout = QHBoxLayout()
        security_output_layout.setSpacing(6)
        
        # -------------------------------------------------
        # CLAVE
        # -------------------------------------------------
        key_group = QGroupBox("🔑 Clave de Seguridad")
        key_layout = QVBoxLayout()
        key_layout.setContentsMargins(5, 5, 5, 5)
        key_layout.setSpacing(4)

        key_input_layout = QHBoxLayout()
        key_input_layout.setSpacing(5)

        key_input_layout.addWidget(QLabel("Contraseña:"))

        self.key_input = QLineEdit()
        self.key_input.setObjectName("password")
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText("Ingresa tu clave...")
        self.key_input.setMinimumHeight(28)

        key_input_layout.addWidget(self.key_input)

        self.chk_show_key = QCheckBox("Mostrar")
        self.chk_show_key.setStyleSheet(
            "color:#888888; font-size:10px;"
        )

        self.chk_show_key.stateChanged.connect(
            self.toggle_key_visibility
        )

        key_input_layout.addWidget(self.chk_show_key)

        key_layout.addLayout(key_input_layout)
        
        # Nota de seguridad
        security_note = QLabel("💡 Nota: Usa una clave segura y memorízala. Sin ella no podrás recuperar tus archivos.")
        security_note.setStyleSheet("color:#ffaa00; font-size:9px;")

        key_layout.addWidget(security_note)
        key_group.setLayout(key_layout)

        # -------------------------------------------------
        # DIRECTORIO
        # -------------------------------------------------
        output_group = QGroupBox("📂 Directorio de Salida")
        output_layout = QHBoxLayout()
        output_layout.setContentsMargins(5, 5, 5, 5)
        output_layout.setSpacing(5)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText(
            "Ingresa, un Directorio, para Guardar (*.dat)..."
        )
        self.output_path.setReadOnly(True)
        self.output_path.setMinimumHeight(28)

        self.btn_output = QPushButton("📂 Seleccionar")

        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.btn_output)

        output_group.setLayout(output_layout)

        security_output_layout.addWidget(
            key_group,
            1
        )

        security_output_layout.addWidget(
            output_group,
            1
        )

        layout.addLayout(security_output_layout)
        
        # ==========================================
        # SECCIÓN: Acciones Principales
        # ==========================================
        actions_group = QGroupBox("⚡ Acciones")
        actions_layout = QHBoxLayout()

        self.btn_encrypt = QPushButton("🔒 ENCRIPTAR")
        self.btn_encrypt.setObjectName("success")
        self.btn_encrypt.setMinimumHeight(50)
        self.btn_encrypt.setStyleSheet("""
            QPushButton{
                background:#1a1a2e;
                border:2px solid #80ff00;
                color:#80ff00;
                font-size:14px;
                font-weight:bold;
            }
            QPushButton:hover{
                background:#80ff00;
                color:black;
            }
        """)
        
        self.btn_decrypt = QPushButton("🔓 DESENCRIPTAR")
        self.btn_decrypt.setMinimumHeight(50)
        self.btn_decrypt.setStyleSheet("""
            QPushButton{
                background:#1a1a2e;
                border:2px solid #00c3ff;
                color:#00c3ff;
                font-size:14px;
                font-weight:bold;
            }
            QPushButton:hover{
                background:#00c3ff;
                color:black;
            }
        """)

        # Dentro de tu layout de clave:
        self.btn_generate_pass = QPushButton("🎲")
        self.btn_generate_pass.setToolTip("Generar contraseña segura")
        self.btn_generate_pass.setFixedWidth(40)
        self.btn_generate_pass.setStyleSheet("""
            QPushButton{
                background:#1a1a2e;
                border:2px solid #00c3ff;
                color:#00c3ff;
                font-size:14px;
                font-weight:bold;
            }
            QPushButton:hover{
                background:#00c3ff;
                color:black;
            }
        """)
        
        
        actions_layout.addWidget(self.btn_encrypt)
        actions_layout.addWidget(self.btn_decrypt)
        actions_layout.addWidget(self.btn_generate_pass)

        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # ==========================================
        # Barra de progreso
        # ==========================================
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # ==========================================
        # SECCIÓN: Log
        # ==========================================
        log_group = QGroupBox("📝 Registro de Operaciones")
        log_layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        self.log.setStyleSheet("""
            QTextEdit{
                background:#080808;
                color:#00ff80;
                border:1px solid #333;
                font-family:'Consolas', monospace;
                font-size:11px;
            }
        """)
        
        log_layout.addWidget(self.log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # ========================================== 
        # Conectar señales
        # ==========================================
        self.btn_files.clicked.connect(self.add_files)
        self.btn_folder.clicked.connect(self.add_folder)
        self.btn_VPD.clicked.connect(lambda: CryptoFileVault.ver_Estructura_ArbolRaiZ(self))
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_LOGs.clicked.connect(lambda: CryptoFileVault.log_events(self))
        self.btn_output.clicked.connect(self.select_output_dir)
        self.btn_encrypt.clicked.connect(self.encrypt_files)
        self.btn_decrypt.clicked.connect(self.decrypt_files)
        self.btn_generate_pass.clicked.connect(self.open_password_generator)
        
        # Atajos de teclado
        QShortcut(QKeySequence('F1'), self).activated.connect(self.show_app_info)
        QShortcut(QKeySequence('Ctrl+B'), self).activated.connect(self.Banner_Imge_Viewer)
        QShortcut(QKeySequence('Ctrl+K'), self).activated.connect(self.show_shortcuts)
        QShortcut(QKeySequence('Ctrl+O'), self).activated.connect(self.add_files)
        QShortcut(QKeySequence('Ctrl+I'), self).activated.connect(self.add_folder)
        QShortcut(QKeySequence('Ctrl+E'), self).activated.connect(self.encrypt_files)
        QShortcut(QKeySequence('Ctrl+D'), self).activated.connect(self.decrypt_files)
        QShortcut(QKeySequence('Ctrl+L'), self).activated.connect(self.clear_all)
        QShortcut(QKeySequence('Ctrl+1'), self).activated.connect(self.visor_on_1)

        self.update_file_info()
    
    ##=========================================================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):

        try:

            if os.path.exists(self.dir_path_Resumen):
                os.remove(self.dir_path_Resumen)
                self.dir_path_Resumen = ""

            self.btn_VPD.hide()

            message = '''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Desarrollado por: 👉 Cristian M. Veliz Cano ✔
Versión del Soft: 👉 V-05
Nombre del Soft: ✨ CryptoFile Vault ✨
✨ Encriptador Universal de Archivos ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Licencia:

MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software y de los archivos de
documentación asociados, para utilizar el Software sin
restricción, incluyendo sin limitación los derechos de uso,
copia, modificación, fusión, publicación, distribución,
sublicencia y/o venta de copias del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
            self.clear_all()
            self.add_log("App closing. Cleanup done.")
            log_message(f"App closing. Cleanup done.")

            QMessageBox.information(self, "Completado", 
                f"{message}\n\nArchivos Todos los archivo(s) procesados...")

        except Exception as e:
            self.add_log(f"Error on close: {e}")
            log_message(f"Error on close: {e}")

        finally:

            if os.path.exists(self.LogFile):
                os.remove(self.LogFile)
                self.LogFile = ""

            event.accept()
                
    ##=========================================================================================
    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 900, 650
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)
    
    ##=========================================================================================
    def show_app_info(self):
        dialog = app_info(self)
        dialog.exec_()

    # =====================================================================
    # Image Banner en LBL_Image...
    # =====================================================================
    def Banner_Imge_Viewer(self):

        path_image = str(":/imagenes/Resources/2.png")
        pixmap = QPixmap(path_image)

        scaled = pixmap
        Viewer_Image.Frame_Viewer_Image(self, scaled)
    
    def show_shortcuts(self):
        dialog_k = key_info(self)
        dialog_k.exec_()

    def visor_on_1(self):

        if os.path.exists(self.dir_path_Resumen):
            os.remove(self.dir_path_Resumen)
            self.dir_path_Resumen = ""

        if self.invisor == True:
            if self.visor_1 == True:
                self.visor_1 = False
                
                self.clear_all()            
                self.visor()

            elif self.visor_1 == False:
                self.visor_1 = True

                self.clear_all()
                self.visor()
    
    ##========================================================================================
    # Métodos de Utilidad
    ##========================================================================================
    def toggle_key_visibility(self, state):
        if state:
            self.key_input.setEchoMode(QLineEdit.Normal)
        else:
            self.key_input.setEchoMode(QLineEdit.Password)
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{timestamp}] {message}")
    
    def update_file_info(self):
        count = len(self.files)
        total_size = sum(os.path.getsize(f) for f in self.files if os.path.exists(f))
        size_mb = total_size / (1024 * 1024)
        self.lbl_file_info.setText(f"Archivos: {count} | Tamaño total: {size_mb:.2f} MB")

    ## Metodo para Acortar el Titulo si este fuera muy Largo (Alternativo)
    def acortando_title(self, text, length=60):

        name, ext = os.path.splitext(text)

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ....{ext}"
    
    ##========================================================================================
    # Selección de Archivos
    ##========================================================================================
    def add_files(self):

        self.path_dir_raiz_carpeta = ""
        self.btn_VPD.hide()
        self.clear_all()
        self.invisor = False

        if os.path.exists(self.dir_path_Resumen):
            os.remove(self.dir_path_Resumen)
            self.dir_path_Resumen = ""

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar Archivos para Encriptar",
            "",
            "Todos los archivos (*.*)"
        )
        
        if files:
            fpath, fname = os.path.split(files[0])
            dir_path_files = CryptoFileVault.acortando_title(self, fpath)

            fname1 = fpath.split("/")[-1]
            fname2 = fname1.split(" ")[0]
            print(fname2)

            self.SubDirecty.show()
            self.SubDirecty.setText(f"Directorio de Archivos: -> {dir_path_files}  {fname2}")

            for f in files:
                if f not in self.files:
                    self.files.append(f)
                    self.list_widget.addItem(os.path.basename(f))
            
            self.add_log(f"Agregados {len(files)} archivo(s)")
            log_message(f"Agregados {len(files)} archivo(s)")
            self.update_file_info()
    
    ##========================================================================================
    # Selección de Archivos por Directorio Completo
    ##========================================================================================    
    def add_folder(self):

        self.path_dir_raiz_carpeta = ""
        self.clear_all()
        self.invisor = True
        self.btn_VPD.hide()

        if os.path.exists(self.dir_path_Resumen):
            os.remove(self.dir_path_Resumen)
            self.dir_path_Resumen = ""

        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta"
        )

        self.path_dir_raiz_carpeta = folder

        if folder == "":
            pass

        else:
            print(folder)
            self.visor()
    
    ##========================================================================================
    # Muestra la Selección de Archivos de 2 Formas Distintas
    ##========================================================================================
    def visor(self):
        global folder

        path_dir_raiz = CryptoFileVault.acortando_title(self, self.path_dir_raiz_carpeta)
        fpath, fname = os.path.split(self.path_dir_raiz_carpeta)
        fname1 = fname.split()[0]
        
        try:
            fname2 = fname.split()[1]
        except:
            fname2 = ""
            pass

        dir_path_Resumen1 = self.path_dir_raiz_carpeta
        self.dir_path_Resumen = f'{dir_path_Resumen1}/Resumen-Arbol_(Directorio).txt'
        print(self.dir_path_Resumen)
        self.add_log(f"[Creado] ↔ Resumen-Arbol_(Directorio).txt ↔ En: 📌 Directorio Principal: 📂 {fname1} {fname2}")
        log_message(f"[Creado] ↔ Resumen-Arbol_(Directorio).txt ↔ En: 📌 Directorio Principal: 📂 {fname1} {fname2}")

        self.SubDirecty.show()
        self.btn_VPD.show()
        self.SubDirecty.setText(f"Directorio de Archivos: -> {path_dir_raiz}  {fname1}")

        if self.visor_1:

            # Construir el árbol completo
            self.list_files_andP.append(f"📌 Directorio Principal: 📂 {self.path_dir_raiz_carpeta}")
            folder = self.path_dir_raiz_carpeta
            dir_path = (f"📌 Directorio Principal: 📂 {self.path_dir_raiz_carpeta}\n")

            try:
                with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                    vaiable_name.write(f'{dir_path}\n')
                    vaiable_name.close()

            except Exception as e:
                print(e)

            # Recursively list directories, subdirectories, and their contents
            for dirpath, dirnames, filenames in os.walk(folder):
                self.added = 0

                # Print the current directory
                if dirpath == folder:

                    self.list_files_andP.append(f'\nEl Directorio es: {os.path.basename(dirpath)}')
                    dir_path = (f'El Directorio es: {os.path.basename(dirpath)}')

                    try:
                        with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                            vaiable_name.write(f'{dir_path}\n')
                            vaiable_name.close()

                    except Exception as e:
                        print(e)

                else:

                    self.list_files_andP.append(f'\nEl Sub-Directorio es: {os.path.basename(dirpath)} del Directorio: {os.path.basename(os.path.dirname(dirpath))}')
                    dir_path = (f'El Sub-Directorio es: {os.path.basename(dirpath)} del Directorio: {os.path.basename(os.path.dirname(dirpath))}')

                    try:
                        with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                            vaiable_name.write(f'{dir_path}\n')
                            vaiable_name.close()

                    except Exception as e:
                        print(e)

                # Print the contents of the current directory
                if filenames:

                    self.list_files_andP.append(f'\nContenido de {os.path.basename(dirpath)}:')

                    for filename in filenames:

                        self.list_files_andP.append(f'  - {filename}')
                        dir_path = (f'Archivo: - {filename}')

                        try:

                            with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                                vaiable_name.write(f'{dir_path}\n')
                                vaiable_name.close()

                        except Exception as e:
                            print(e)

                        self.added += 1

            self.list_widget.addItems(self.list_files_andP)
            self.add_log(f"Agregados {self.added} archivo(s) de la carpeta")
            log_message(f"Agregados {self.added} archivo(s) de la carpeta")
            self.update_file_info()

        elif self.visor_1 == False:

            # Construir el árbol completo
            self.list_files_andP.append(f"📌 Directorio Principal: 📂 {self.path_dir_raiz_carpeta}\n")
            folder = self.path_dir_raiz_carpeta
            dir_path = (f"📌 Directorio Principal: 📂 {self.path_dir_raiz_carpeta}\n")

            try:
                with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                    vaiable_name.write(f'{dir_path}\n')
                    vaiable_name.close()

            except Exception as e:
                print(e)

            # Usar os.walk para recorrer todo el árbol
            # Ordenamos para mantener consistencia alfabética
            for dirpath, dirnames, filenames in os.walk(folder):
                # Ordenar directorios y archivos alfabéticamente
                dirnames.sort()
                filenames.sort()
                self.added = 0
                
                # Calcular el nivel de profundidad (nivel 0 = raíz)
                relative_path = os.path.relpath(dirpath, folder)
                if relative_path == ".":
                    level = 0
                else:
                    level = relative_path.count(os.sep) + 1
                
                # Indentación: 1 tabulación por nivel
                indent = "\t" * level
                
                # Si no es el directorio raíz, mostrarlo como sub-directorio
                if level > 0:
                    current_dir_name = os.path.basename(dirpath)
                    self.list_files_andP.append(f"\n{indent}➜ Sub-Directorio: \"📂 {current_dir_name}\"  ||  👀 Y Dentro Hay:\n")
                    dir_path = (f"\n{indent}➜ Sub-Directorio: \"📂 {current_dir_name}\"  ||  👀 Y Dentro Hay:\n")

                    try:
                        with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                            vaiable_name.write(f'{dir_path}\n')
                            vaiable_name.close()

                    except Exception as e:
                        print(e)
                
                # Listar archivos en este directorio (si hay)
                if filenames:
                    file_indent = "\t" * (level + 1)
                    for filename in filenames:
                        # Extraer extensión
                        _, ext = os.path.splitext(filename)
                        if ext:
                            ext_display = ext.lower()
                        else:
                            ext_display = "sin_ext"
                        
                        self.list_files_andP.append(f"{file_indent}•  {filename} [⭐{ext_display}]")
                        dir_path = (f"{file_indent}•  {filename} [⭐{ext_display}]")

                        try:
                            with open(self.dir_path_Resumen, "a", encoding="utf-8", errors='ignore') as vaiable_name:
                                vaiable_name.write(f'{dir_path}\n')
                                vaiable_name.close()

                        except Exception as e:
                            print(e)

                        self.added += 1
            
            # Agregar línea en blanco al final para separar de futuras operaciones
            self.list_files_andP.append("")

            self.list_files_andP.append("🎉 Descompresión Finalizada")
            self.list_files_andP.append(f"📦 Archivo Creado: {folder}")

            self.list_widget.addItems(self.list_files_andP)
            self.add_log(f"Agregados {self.added} archivo(s) de la carpeta")
            log_message(f"Agregados {self.added} archivo(s) de la carpeta")
            self.update_file_info()
        
        if folder:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in self.files:
                        self.files.append(file_path)
    
    ##========================================================================================
    # Borra toda la Selección de Archivos
    ##========================================================================================    
    def clear_all(self):
        self.files.clear()
        self.list_widget.clear()
        self.list_files_andP.clear()
        self.SubDirecty.hide()
        self.btn_VPD.hide()
        self.SubDirecty.setText("Directorio de Archivos: -> ")
        self.add_log("Lista limpiada")
        log_message(f"Lista limpiada")
        self.update_file_info()
    
    ##========================================================================================
    # Selección de Salida del Archivos ya Encriptado
    ##========================================================================================    
    def select_output_dir(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Directorio de Salida"
        )
        
        if folder:
            self.output_path.setText(folder)
            self.add_log(f"Directorio de salida: {folder}")
            log_message(f"Directorio de salida: {folder}")

    ##========================================================================================
    # Generardor, de Contraseñas
    ##========================================================================================   
    def open_password_generator(self):
        dialog = PasswordGeneratorDialog(self, self.key_input.text())
        dialog.password_generated.connect(self.set_generated_password)
        dialog.exec_()
   
    def set_generated_password(self, password):
        self.key_input.setText(password)
        self.add_log(f"🔐 Contraseña generada: {len(password)} caracteres")
        log_message(f"[PasswordGeneratorDialog] 🔐 Contraseña generada: {len(password)} caracteres")

    ##========================================================================================
    # Encriptación Archivos Separados...
    ##========================================================================================
    def encrypt_files(self):

        if not CRYPTO_AVAILABLE:
            QMessageBox.critical(self, "Error", "Instala el módulo 'cryptography'\npip install cryptography")
            return

        if not self.files:
            QMessageBox.warning(self, "Atención", "Selecciona al menos un archivo")
            return
        
        password = self.key_input.text()
        if not password:
            QMessageBox.warning(self, "Atención", "🔑  ↔  Ingresa una clave de seguridad")
            return
        
        directory = self.output_path.text()
        if not directory:
            QMessageBox.warning(self, "Atención", "Ingresa un Directorio para Guardar el Archivo:\n📌  ↔  (🔐  vault_encrypted.dat)")
            return
        
        # Confirmación
        reply = QMessageBox.question(
            self,
            "Confirmar Encriptación",
            f"Se encriptarán {len(self.files)} archivo(s).\n\n"
            "⚠️ IMPORTANTE: Guarda tu clave en un lugar seguro.\n"
            "Sin ella NO podrás recuperar tus archivos.\n\n"
            "¿Continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.setEnabled(False)

        output_dir = self.output_path.text() if self.output_path.text() else None
        print(f"Directorio raíz: --->>> {self.path_dir_raiz_carpeta}")

        if os.path.isdir(self.path_dir_raiz_carpeta):
            CryptoFileVault.encrypt_files_dir(self, self.files.copy(), password, output_dir)

        else:
            
            self.worker = CryptoWorker('encrypt', self.files.copy(), password, output_dir)
            self.worker.progress.connect(self.update_progress)
            self.worker.log.connect(self.add_log)
            self.worker.finished.connect(self.operation_finished)
            self.worker.start()

    ##========================================================================================
    # Encriptación por Grupo (Directorio 6 Sub´s-Directorios)
    ##========================================================================================
    def encrypt_files_dir(self, files, password, output_dir):
        
        output_dir = self.output_path.text() if self.output_path.text() else None
        if self.path_dir_raiz_carpeta:
            path_dir_raiz_carpeta = self.path_dir_raiz_carpeta
        
            self.worker = CryptoWorker('encrypt_grup', self.files.copy(), password, output_dir, path_dir_raiz_carpeta=path_dir_raiz_carpeta)
            self.worker.progress.connect(self.update_progress)
            self.worker.log.connect(self.add_log)
            self.worker.finished.connect(self.operation_finished)
            self.worker.start()
    
    ##========================================================================================
    # Desencriptación
    ##========================================================================================
    def decrypt_files(self):
        if not CRYPTO_AVAILABLE:
            QMessageBox.critical(self, "Error", "Instala el módulo 'cryptography'\npip install cryptography")
            return
        
        if not self.files:
            QMessageBox.warning(self, "Atención", "Selecciona archivos .dat para desencriptar")
            return
        
        # Filtrar solo archivos .dat
        dat_files = [f for f in self.files if f.endswith('.dat')]
        if not dat_files:
            QMessageBox.warning(self, "Atención", "Selecciona archivos .dat válidos")
            return
        
        password = self.key_input.text()
        if not password:
            QMessageBox.warning(self, "Atención", "🔑  ↔  Ingresa la clave de desencriptación")
            return
        
        directory = self.output_path.text()
        if not directory:
            QMessageBox.warning(self, "Atención", "Ingresa un Directorio para Guardar el Archivo:\n🔐 (*.dat)  ↔  📂 Desencriptado")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.setEnabled(False)
        
        output_dir = self.output_path.text() if self.output_path.text() else None
        
        self.worker = CryptoWorker('decrypt', dat_files, password, output_dir)
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.operation_finished)
        self.worker.start()
    
    ##========================================================================================
    # Callbacks del Worker
    ##========================================================================================
    def update_progress(self, current, total, filename):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"{current}/{total} - {filename}")
    
    def operation_finished(self, success, message, count):
        self.setEnabled(True)
        self.progress_bar.setVisible(False)

        if os.path.exists(self.dir_path_Resumen):
            os.remove(self.dir_path_Resumen)
            self.dir_path_Resumen = ""
        
        if success:
            self.add_log(f"✅ {message}: {count} archivo(s) procesados")
            log_message(f"✅ {message}: {count} archivo(s) procesados")
            QMessageBox.information(self, "Completado", 
                f"{message}\n\nArchivos procesados: {count}")
        else:
            self.add_log(f"❌ Error: {message}")
            log_message(f"❌ Error: {message}")
            QMessageBox.critical(self, "Error", message)

        self.clear_all()

    def ver_Estructura_ArbolRaiZ(self):

        resp = CryptoFileVault.show_question(self, "Pregunta", "Deseas, Ver una Vista Previa de el Arbol (Directorio)?.")
        if resp == True:

            try:
                if not self.dir_path_Resumen:
                    return

                # Guardamos en Temporales...
                path_txt = self.dir_path_Resumen
                msn = '''Vista del Directorio a Encriptar: ...'''
                TXT_Lec.Frame_TXT_Lec(self, path_txt, msn)

            except Exception as e:
                print(e)

    def log_events(self):

        resp = CryptoFileVault.show_question(self, "Pregunta", "Deseas, Ver los Eventos Registrados, en LOG´s?.")
        if resp == True:

            try:
                if not self.LogFile:
                    return

                # Guardamos en Temporales...
                print(self.LogFile)
                msn = '''Lectura, de LOG´s, para: [AUDITORIA DE EVENTOS]: ...'''
                TXT_Lec.Frame_TXT_Lec(self, self.LogFile, msn)

            except Exception as e:
                print(e)

    # =========================
    # MENSAJES
    # =========================
    def show_question(self, titulo, texto):
        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)
        msg.setText(texto)

        msg.setIcon(QMessageBox.Question)

        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)

        respuesta = msg.exec_()

        return respuesta == QMessageBox.Yes

##====================================================================================
##====================================================================================

class TXT_Lec(CryptoFileVault):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.msn = msn

    def Frame_TXT_Lec(self, output_path, msn):

        dialog = QDialog(self)
        dialog.setWindowTitle("Contenido del Archivo")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()
        dialog.setLayout(layout)

        label = QLabel(f'{msn}'+ " " * 110)
        label.setStyleSheet('''
            QLabel{
                background-color: #0a0a0a;
                color: #00ff41;
                font-size: 18px;
            }
            ''')
        layout.addWidget(label)

        # Create Font Size, Font Bold, Font Wieight, Font PonintSize
        self.font_txt = QtGui.QFont("Courier New")
        self.font_txt.setPointSize(6)
        self.font_txt.setBold(True)
        self.font_txt.setWeight(200)

        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet('''
            QPlainTextEdit{
                background-color: #0a0a0a;
                color: #00ff41;
                font-size: 20px;
            }
            ''')

        self.editor.setReadOnly(True)
        self.editor.setFont(self.font_txt)
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0 )

        layout.addWidget(self.editor)

        try:

            try:

                with open(output_path, 'r', encoding="utf-8", errors='ignore') as f:
                    text = f.read()

                    print(text)
                    self.editor.setPlainText(text)

            except Exception as e:
                print(e)

                with open(output_path, 'r', encoding="utf-8") as f:
                    text = f.read()

                    print(text)
                    self.editor.setPlainText(text)

        except Exception as e:
            print(e)

            with open(output_path, 'r', encoding="utf-8") as f:
                text = f.read()

                print(text)
                self.editor.setPlainText(text)

        dialog.exec_()

##====================================================================================
# Diálogo de información
##====================================================================================
class app_info(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("✨ Información del Software ✨")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        icon_path = ":/imagenes/Resources/1.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("✨ CryptoFile Vault ✨")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00c3ff;
            }
        """)
        layout.addWidget(title)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText('''
Desarrollado por: 👉 Cristian M. Veliz Cano ✔
Versión del Soft: 👉 V-05
Nombre del Soft: ✨ CryptoFile Vault ✨
✨ Encriptador Universal de Archivos ✨

✅ Este Soft-Ware fue diseñado para encriptar y desencriptar
cualquier tipo de archivo de forma segura, ya sean Archivos, 
en grupo, pero sin Directorio, "O", se puede con un Directoiro, Completo,
utilizando criptografía simétrica con clave personalizada.

⚙️ El funcionamiento del Programa es Directo:

📄 El Usuario selecciona archivos individuales o múltiples,
   ingresa una clave privada, y el sistema los encripta
   convirtiéndolos en archivos seguros .dat

⭐ El Soft-Ware permite trabajar con:

✔ Archivos Individuales de Cualquier Tipo (*.*)
✔ Múltiples Archivos (auto-comprime en ZIP y encripta)
✔ Múltiples Archivos (auto-comprime en ZIP y encripta, Con Gerarquia de Arbol)
✔ Con Compreción, y Des-Compreción, Original, [osea si tiene Gerarquia de Arbol]
✔ Directorios Completos (con contenido recursivo, [Gerarquia de Arbol])
✔ Desencriptación con Recuperación de Nombres Originales, [Gerarquia de Arbol]
✔ Extracción Organizada en Carpeta "Desencriptados", [Gerarquia de Arbol]
✔ Con Visor, para Ver la Gerarquia del Arbol de 2 Formas, y poder Hacer Una Revición
✔ Con Visor, de LOG´s [EVENTOS], que hemos Hecho hasta el Momento, Herrores, o Auditoria

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Algoritmo de Encriptación:

➜ Fernet (AES-128 en modo CBC + HMAC)
➜ ZIP (pyzipper) ↔ Con soporte password ↔ CON CONTRASEÑA AES-256
➜ Clave derivada mediante PBKDF2HMAC (100,000 iteraciones)
➜ Salt aleatorio único por cada archivo
➜ Verificación de integridad integrada
➜ Verificación de la Creación del Archivo RESUMEN-LOG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Funciones Principales:

📎 Encriptar Archivos: Convierte cualquier archivo a formato
   .dat seguro usando tu clave personalizada.

📎 Encriptar Múltiples: Comprime automáticamente en ZIP y
   encripta el paquete completo en un solo .dat

📎 Ahora, con: 
   ➜ ZIP (pyzipper) ↔ Con soporte password ↔ CON CONTRASEÑA AES-256
   para cifrar, el ZIP, antes de ser Cifrado nuevamente, con FERMET

📎 Desencriptar: Recupera archivos originales usando la
   misma clave. Detecta automáticamente si es ZIP.
   ➜ Con soporte password ↔ CON CONTRASEÑA AES-256

📎 Al momento, de Selecciónar un Directorio, este lo comprimira,
   de manera Fideidigna, al Original, y de Igual Modo, al ser
   descompreso, este des-comprimira, el Directorio, tal cual fue
   Propocionado, es decir, con Sub-Directorios, y archivos, 
   dentro de cada, rama, sin perder, el Arbol, completo.

📎 Extracción Organizada: Los archivos múltiples se extraen
   en carpeta "Desencriptados" manteniendo estructura.

📎 Cualquier Extensión: Funciona con .png, .jpg, .pdf, .doc,
   .exe, .mp4, .zip, y cualquier archivo (*.*)

📎 Crea un Archivo, donde se podra, Visualizar, el Arbol de los Directorios 
   de 2 Formas distintas, pero solo es vicible, dentro de la Selección por 
   Directorios.

📎 Crea, un Archivo, de Eventos, LOG´s, pero solamente, es legible, durante,
   este abierto, el Soft, es decir, los Log´s, solamente, seran Vicibles, si
   el Programa CryptoFile Vault_v3, está, avierto, es decir si se está -
   trabajando en el.

📎 Al Momento, de Cerrar, el Soft-Ware, [Programa], este Borra de forma, automatica
   tanto el Archivo, LOG, como el ultimo, resumen de Directorio a ser Encriptado, 
   el Archivo, del Resumen del Directorio, solamente, sera, visible, si el Programa
   ahun apunta a esa directorio, y si ahun está, abierto, el Soft-Ware, pues, al 
   cambiar, de Directorio, este se borra, hasi como se creo, no dejando, rastro, 
   tambien se borra, automaticamente, si se cambia, de Directorio, a Archivos, Sim-
   ples, y la otra forma mientras, ahun está abierto el programa, seria, en el boton
   Limpiar (CLEANER), o Porque ya se Encripto el Directorio, pero el Resumen, queda,
   Criptado, tambien, para, hacer una Comparación, acá, mismo se Explica como se trabaja
   con este Archivo.

📎 El Visor, de los Archivos, LOG´s, y el RESUMEN-DIRECTORIO, seran utilizados, unicamente,
   si estos, Archivos, existen, de lo contrario, no habrira, el Visor, ahora, bien con 
   el archivo, de los LOG´s, este ciempre, estara, Disponible, desde su primer Innicio, 
   hastá su cierre.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Nota Importante:

➜ Este Soft-Ware trabaja completamente de forma Local.

✔ No requiere conexión a Internet.
✔ No utiliza Servicios Externos.
✔ No transmite Información.
✔ No borra archivos, originales
✔ Las claves NO se almacenan en ningún lado.
✔ Sin tu clave, NADIE puede recuperar los archivos.

💯% OFF-LINE y SEGURO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️ Atajos del Teclado:

📎 F1
• Para mostrar información del software.

📎 CTRL+K
⌨️ Para mostrar los Atajos del Teclado.

📎 CTRL+B
→ Te Muestra su Imagen Poster ↔ Tipo Banner, para Reprecentar, al Mismo
  Soft-Ware (Programa).

📎 ESC
• Cierra inmediatamente el Soft-Ware.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Nota:
    → Este Soft-Ware (Programa), Ignorara, las Carpetas Vacias, dentro
    de un Arbol Seleccionado, es decir, que si se selecciona un Direc-
    torio, si este llegara, a Tener una Carpeta, (Sub-Directorio), -
    Vacio, el Soft, simplemente, la ignorara, por no tener nada, Dentro,
    quiere decir, que si la Carpeta tendria, Alvun Valor, vien por su,
    Nombre, o bien porque Si habia, algo dentro, pero al momento, de
    Criptar, Dicho Directorio, está ya no tiene el Archivo, el Soft,
    simplemente ignorara, el Echo, y la Carpeta, no la Incluira, porque
    estaria, gastando, recursos, que al mismo, le son Utiles, para la 
    Elaboración, del Criptado, y sus Acciónes, Consecuentemente.-

    Gracias, por la Comprención, la carpeta, Ignorada, porque se encuentra
    Vacia, tendria, que volverse a crear, de forma Manual, despues, de su
    Desencriptadura, es lo unico, que el soft, no Atiende, los Directorios
    Vacios...

📌 Nota:
    → Este Soft-Ware, tambien crea una Lista descriptiva, de todos, los Archivos
    que puedieren estar dentro del Directorio Principal, a la hora, de crearse
    el Encriptamiento, del mismo Directorio, Esto lo hace en Aras, de Evitar,
    Pocibles, confuciones, de si Estaria, o No el Archivo, dentro de la Carpeta,
    que no Guardo, por el Echo de Estar, Vacia, de está Manera, el Soft, Demuestra
    que dicha Carpeta, no tenia, ningun Archivo, y es Complementa, Inalterable,
    dicho Archivo: Resumen-Arbol_(Directorio).txt, ya que este estara, dentro del 
    (vault_encrypted.dat), Encriptado, y sera Expuesto, cuando, los Archivos, sean 
    desencriptados, quedando, en el Mismo Directorio, de los Archivos, Desencriptados.

📌 Nota:
    Ahora también se le integra un Generador, de Contraseñas:
    • 🔐 Generador de Contraseñas Seguras ↔ Entropía: L * log2(R)
    → Ideal para ser Utilizado con: 
      • FERNET + PBKDF2HMAC ↔ CON SOPORTE AES-256 (EN *.ZIP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Licencia:

MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software y de los archivos de
documentación asociados, para utilizar el Software sin
restricción, incluyendo sin limitación los derechos de uso,
copia, modificación, fusión, publicación, distribución,
sublicencia y/o venta de copias del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 De Caracter Gratuito, Portable,
🎭 Open-Source, Didáctico y Free-Code.

🛠️ Diseñado para Protección de Datos,
Privacidad y Seguridad de Archivos.
        ''')
        
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #111118;
                color: #F1F1F1;
                border: 1px solid #00c3ff;
                border-radius: 5px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        layout.addWidget(info_text)
        
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #00c3ff;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)
        layout.addWidget(close_button)

##====================================================================================
##====================================================================================
class key_info(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("⌨️ Atajos de Teclas")
        self.setFixedSize(520, 420)
        self.setModal(True)
        
        icon_path = ":/imagenes/Resources/1.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("⌨️ Atajos de Teclas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00c3ff;
            }
        """)
        layout.addWidget(title)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️ Atajos del Teclado:

📎 F1
• Para mostrar información del software.

📎 CTRL+K
⌨️ Para mostrar esta ventana de Atajos del Teclado.

📎 CTRL+O
📄 Agregar archivos individuales.
   Soporta múltiples selección de archivos (*.*)

📎 CTRL+I
📁 Agregar carpeta completa.
   Busca todos los archivos recursivamente.

📎 CTRL+E
🔒 Encriptar archivos seleccionados.
   Solicita confirmación antes de procesar.

📎 CTRL+D
🔓 Desencriptar archivos .dat.
   Recupera archivos originales con la clave.

📎 CTRL+L
🗑️ Limpia completamente la lista de archivos.
   Vacía todas las selecciones actuales.

📎 CTRL+1
→ Con la Tecla Control & el Número (1), Cambiamos, la Vista en el Visor
  de Eventos, donde estan los Archivos, Reien Ingresados.

📎 CTRL+B
→ Te Muestra su Imagen Poster ↔ Tipo Banner, para Reprecentar, al Mismo
  Soft-Ware (Programa).


📎 ESC
• Cierra inmediatamente el Soft-Ware.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Consejos de Uso:

🔐 Seguridad:
• Usa claves de al menos 8 caracteres.
• Combina letras, números y símbolos.
• Nunca compartas tu clave por medios inseguros.
• Guarda tu clave en un lugar seguro.

📦 Múltiples Archivos:
• Al encriptar varios archivos, se crea un ZIP
  temporal que luego se encripta como .dat único.
• Al desencriptar, se detecta automáticamente si
  contiene múltiples archivos y extrae en carpeta
  "Desencriptados", si tuviere, multiples archivos
  es Desenpaqueta, el ZIP, con Gerarquia, de Arbol.

📂 Directorio de Salida:
• Detecta si no se ha seleccionado una carpeta de salida, para los archivos
  una vez sean Desencriptados.
• Puedes seleccionar un destino diferente con el botón "Seleccionar" en la 
  sección de Directorio.

✔ El Soft-Ware [Programa], Cuenta, con un Visor, para Ver la Gerarquia del 
  Arbol de 2 Formas, y poder Hacer Una Revición, de los Archivos, a ser Encriptados.

✔ El Soft-Ware [Programa], Cuenta, con un Visor, de LOG´s [EVENTOS], 
  que hemos Hecho hasta el Momento, Herrores, o poder hacer una 
  Auditoria, rapida, de donde se ha cometido, algun tipo de herror, 
  o simplemente, para ver que hemos, encriptado hastá el momento.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Licencia:

MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software...

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #111118;
                color: #F1F1F1;
                border: 1px solid #00c3ff;
                border-radius: 5px;
                padding: 8px;
                font-size: 10.5pt;
            }
        """)
        layout.addWidget(info_text)
        
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #00c3ff;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)
        layout.addWidget(close_button)

##====================================================================================
##====================================================================================

class Viewer_Image(CryptoFileVault):

    def __init__(self, parent=None):
        super().__init__(parent)

    def Frame_Viewer_Image(self, output_path):

        self.path = output_path

        dialog = QDialog(self)
        dialog.setWindowTitle("Contenido del Archivo")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        ##self.center_on_screen()

        layout = QVBoxLayout()        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        dialog.setLayout(layout)

        Image_App = QGroupBox()
        layout_image = QVBoxLayout()
        layout_image.setContentsMargins(0, 0, 0, 0)
        layout_image.setSpacing(0)

        #fpath, fname = os.path.split(output_path)
        label = QLabel('✨ 🔐 CryptoFile Vault ✨')
        label.setStyleSheet('''
        QLabel {
            font-weight: bold;
            color: #00c3ff;
            background-color: #000000;
            font-size: 30px;
        }
        ''')
        # label.setFixedWidth(25)
        label.setFixedHeight(50)
        label.setAlignment(Qt.AlignCenter)
        layout_image.addWidget(label)
        
        self.LBL_Image_Banner = QLabel()
        self.LBL_Image_Banner.setAlignment(Qt.AlignCenter)
        self.LBL_Image_Banner.setScaledContents(True)

        layout_image.addWidget(self.LBL_Image_Banner)
        Image_App.setLayout(layout_image)
        layout.addWidget(Image_App)

        try:

            try:

                scaled = self.path.scaled(
                    self.width()-50, self.height(), 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )

                self.LBL_Image_Banner.setText("")
                self.LBL_Image_Banner.setPixmap(scaled)

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)

        dialog.exec_()

# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Estilo global adicional
    app.setStyleSheet("""
        QToolTip{
            background:#1a1a2e;
            color:#00c3ff;
            border:1px solid #00c3ff;
            padding:5px;
        }
    """)
    
    window = CryptoFileVault()
    window.show()
    sys.exit(app.exec_())

# =====================================================
# =====================================================