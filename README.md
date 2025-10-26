# DeepSeek OCR Crypto Bot 🤖📈

Un bot de criptomonedas avanzado que utiliza la tecnología DeepSeek OCR para analizar imágenes relacionadas con criptomonedas, extraer datos de gráficos y precios, y proporcionar información del mercado en tiempo real.

## Características 🌟

- **OCR con DeepSeek**: Análisis avanzado de imágenes de criptomonedas usando DeepSeek Vision
- **Análisis de Gráficos**: Extrae tendencias, patrones y niveles de soporte/resistencia de gráficos
- **Extracción de Precios**: Lee precios de criptomonedas desde capturas de pantalla
- **API de Mercado**: Consulta precios en tiempo real, capitalización de mercado y volúmenes
- **Búsqueda de Monedas**: Encuentra criptomonedas por nombre o símbolo
- **Tendencias**: Descubre las criptomonedas más populares del momento

## Requisitos 📋

- Python 3.8 o superior
- Una API key de DeepSeek (obtener en [deepseek.com](https://www.deepseek.com))
- Conexión a Internet para consultas de API

## Instalación 🚀

1. **Clonar el repositorio**:
```bash
git clone https://github.com/jaimestanislav/sek-ocr-crypto.git
cd sek-ocr-crypto
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
cp .env.example .env
```

Editar `.env` y agregar tu API key de DeepSeek:
```
DEEPSEEK_API_KEY=tu_api_key_aqui
```

## Uso 💻

### Línea de Comandos

**Analizar una imagen de gráfico de criptomonedas**:
```bash
python bot.py --analyze-image chart.png --type chart
```

**Extraer precios de una captura de pantalla**:
```bash
python bot.py --analyze-image prices.png --type price
```

**Consultar precio de Bitcoin**:
```bash
python bot.py --price bitcoin
```

**Obtener datos detallados del mercado de Ethereum**:
```bash
python bot.py --market ethereum
```

**Buscar una criptomoneda**:
```bash
python bot.py --search cardano
```

**Ver criptomonedas en tendencia**:
```bash
python bot.py --trending
```

### Uso Programático

```python
from bot import CryptoBot

# Inicializar el bot
bot = CryptoBot()

# Analizar un gráfico
bot.analyze_image('chart.png', 'chart')

# Obtener precio
bot.get_crypto_price('bitcoin')

# Datos de mercado detallados
bot.get_detailed_market_data('ethereum')

# Buscar monedas
bot.search_crypto('solana')

# Ver tendencias
bot.get_trending()
```

### Ejemplos

Ejecutar los ejemplos incluidos:
```bash
python examples.py
```

## Estructura del Proyecto 📁

```
sek-ocr-crypto/
├── bot.py              # Aplicación principal del bot
├── config.py           # Configuración y variables de entorno
├── ocr_module.py       # Módulo de OCR con DeepSeek
├── crypto_api.py       # Cliente API de criptomonedas
├── examples.py         # Ejemplos de uso
├── requirements.txt    # Dependencias de Python
├── .env.example        # Plantilla de variables de entorno
├── .gitignore         # Archivos a ignorar en git
└── README.md          # Este archivo
```

## Módulos 🔧

### `bot.py`
Aplicación principal que integra todos los módulos y proporciona interfaz de línea de comandos.

### `ocr_module.py`
Maneja la integración con DeepSeek OCR para:
- Extracción de datos de criptomonedas de imágenes
- Análisis de gráficos y patrones
- Lectura de precios desde capturas de pantalla

### `crypto_api.py`
Cliente para la API de CoinGecko que proporciona:
- Precios en tiempo real
- Datos de mercado detallados
- Búsqueda de criptomonedas
- Tendencias del mercado

### `config.py`
Gestión de configuración y validación de variables de entorno.

## Capacidades de OCR 🔍

El bot puede analizar varios tipos de imágenes relacionadas con criptomonedas:

1. **Gráficos de Trading**: Identifica tendencias, patrones técnicos, soportes y resistencias
2. **Capturas de Precios**: Extrae precios, cambios porcentuales y capitalización de mercado
3. **Tablas de Mercado**: Lee datos tabulares de múltiples criptomonedas
4. **Infografías**: Analiza información visual sobre criptomonedas

## API de CoinGecko 📊

Este bot utiliza la API gratuita de CoinGecko para obtener datos del mercado de criptomonedas. No requiere API key para funcionalidad básica.

Límites de la API gratuita:
- 10-50 llamadas por minuto
- Datos con retraso mínimo
- Acceso a datos históricos limitados

## Configuración Avanzada ⚙️

Puedes personalizar el comportamiento del bot editando el archivo `.env`:

```bash
# Modelo de DeepSeek
OCR_MODEL=deepseek-chat

# Parámetros de OCR
OCR_TEMPERATURE=0.0      # Más bajo = más determinista
OCR_MAX_TOKENS=2000      # Máximo de tokens en respuesta

# Límites de imagen
MAX_IMAGE_SIZE=5242880   # 5MB máximo
```

## Solución de Problemas 🔧

**Error: "DEEPSEEK_API_KEY is required"**
- Asegúrate de haber creado el archivo `.env` y agregado tu API key

**Error al analizar imagen**
- Verifica que la imagen existe y está en formato soportado (PNG, JPG, JPEG, WEBP)
- Asegúrate de que el tamaño de la imagen no exceda 5MB

**Errores de API**
- Verifica tu conexión a Internet
- Comprueba que no has excedido los límites de la API

## Contribuir 🤝

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Licencia 📄

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor ✨

Desarrollado por Jaime Stanislav

## Agradecimientos 🙏

- [DeepSeek](https://www.deepseek.com) por su tecnología OCR avanzada
- [CoinGecko](https://www.coingecko.com) por su API gratuita de criptomonedas
- La comunidad de Python y cripto

## Soporte 💬

Si encuentras algún problema o tienes preguntas:
- Abre un issue en GitHub
- Consulta la documentación de DeepSeek
- Revisa los ejemplos incluidos

---

**Nota**: Este bot es solo para fines educativos e informativos. No constituye asesoramiento financiero. Siempre investiga antes de invertir en criptomonedas.