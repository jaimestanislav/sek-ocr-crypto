# DeepSeek OCR Crypto Bot 🤖📈

Un bot de criptomonedas avanzado que utiliza la tecnología DeepSeek OCR para analizar imágenes relacionadas con criptomonedas, extraer datos de gráficos y precios, y proporcionar información del mercado en tiempo real.

## Características 🌟

- **OCR con DeepSeek**: Análisis avanzado de imágenes de criptomonedas usando DeepSeek Vision
- **Análisis de Gráficos**: Extrae tendencias, patrones y niveles de soporte/resistencia de gráficos
- **Extracción de Precios**: Lee precios de criptomonedas desde capturas de pantalla
- **API de Mercado**: Consulta precios en tiempo real, capitalización de mercado y volúmenes
- **Análisis Técnico Avanzado**: Indicadores técnicos completos para análisis de mercado
  - **Medias Móviles**: SMA y EMA para identificar tendencias
  - **RSI**: Índice de Fuerza Relativa para detectar sobrecompra/sobreventa
  - **MACD**: Convergencia/Divergencia de Medias Móviles
  - **Bandas de Bollinger**: Identificación de volatilidad y niveles extremos
  - **Análisis de Volumen**: Comparación con promedios históricos
  - **Patrones de Velas**: Detección automática de patrones importantes
  - **Soporte y Resistencia**: Identificación de niveles clave y dinámicos
  - **Cruces Dorado/Muerte**: Detección de señales de trading importantes
  - **Recomendaciones**: Análisis integral con sentimiento y recomendaciones de trading
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

**Obtener análisis técnico completo de Bitcoin**:
```bash
python bot.py --technical bitcoin
```

**Análisis técnico con datos de 180 días**:
```bash
python bot.py --technical ethereum --days 180
```

### Análisis en Tiempo Real con DEBUG 🔍

El script `latest_analysis.py` proporciona un análisis rápido con información técnica detallada en formato DEBUG.

**Uso básico**:
```bash
python latest_analysis.py bitcoin
```

**Con más datos históricos (recomendado para SMA 200)**:
```bash
python latest_analysis.py ethereum --days 250
```

**Ejemplo de salida**:
```
--- DEBUG: Latest Row Data ---
open           118700.691887
high           118791.929738
low            117494.145643
close          118700.691887
SMA_50         114980.102802
SMA_200        102706.514495
RSI_14             53.791814
MACD            1853.802289
MACD_hist         86.695951
MACD_signal     1767.106338
BB_lower       111059.883039
BB_upper       123752.233052
Name: 2025-10-25 02:40:56, dtype: float64
--------------------------------
Latest Analysis for bitcoin:
--- Price & Moving Averages ---
Latest Close Price: $118700.69
Trend: Bullish - Price is above both SMA 50 and SMA 200.

--- Oscillators ---
RSI (14): 53.79
RSI Status: Neutral (30-70).
MACD (1853.80) | Signal (1767.11) | Histogram (86.70)
MACD Status: Bullish momentum.

--- Volatility ---
Bollinger Bands: Upper=$123752.23, Lower=$111059.88
BB Status: Price is within the bands.

[Strategy]:
BUY - Multiple bullish indicators suggest an upward trend.
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

# Análisis técnico completo
bot.get_technical_analysis('bitcoin', days=90)

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
├── bot.py                      # Aplicación principal del bot
├── latest_analysis.py          # Script de análisis en tiempo real con DEBUG
├── config.py                   # Configuración y variables de entorno
├── ocr_module.py               # Módulo de OCR con DeepSeek
├── crypto_api.py               # Cliente API de criptomonedas
├── technical_analysis.py       # Módulo de análisis técnico
├── examples.py                 # Ejemplos de uso
├── test_bot.py                 # Tests del bot
├── test_technical_analysis.py  # Tests de análisis técnico
├── requirements.txt            # Dependencias de Python
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Archivos a ignorar en git
└── README.md                   # Este archivo
```

## Módulos 🔧

### `bot.py`
Aplicación principal que integra todos los módulos y proporciona interfaz de línea de comandos.

### `latest_analysis.py`
Script dedicado para análisis en tiempo real con información DEBUG detallada que muestra:
- Datos de la última vela OHLC (Open, High, Low, Close)
- Indicadores técnicos actuales (SMA 50/200, RSI, MACD, Bollinger Bands)
- Análisis de tendencia basado en medias móviles
- Estado de osciladores (RSI, MACD)
- Análisis de volatilidad (Bandas de Bollinger)
- Recomendación de estrategia (BUY/SELL/HOLD)

Este script es ideal para obtener un snapshot rápido del estado técnico de una criptomoneda con información detallada de depuración.

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
- Datos OHLCV para análisis técnico

### `technical_analysis.py`
Módulo de análisis técnico avanzado que incluye:
- Cálculo de indicadores técnicos (MA, RSI, MACD, Bollinger Bands)
- Detección de patrones de velas
- Identificación de niveles de soporte y resistencia
- Análisis de volumen
- Generación de recomendaciones basadas en múltiples indicadores

### `config.py`
Gestión de configuración y validación de variables de entorno.

## Capacidades de OCR 🔍

El bot puede analizar varios tipos de imágenes relacionadas con criptomonedas:

1. **Gráficos de Trading**: Identifica tendencias, patrones técnicos, soportes y resistencias
2. **Capturas de Precios**: Extrae precios, cambios porcentuales y capitalización de mercado
3. **Tablas de Mercado**: Lee datos tabulares de múltiples criptomonedas
4. **Infografías**: Analiza información visual sobre criptomonedas

## Análisis Técnico 📈

El módulo de análisis técnico proporciona indicadores profesionales para trading:

### Indicadores Implementados

1. **Medias Móviles (MA)**
   - SMA 20, 50, 200: Identifica tendencias de corto, medio y largo plazo
   - EMA 12, 26: Para análisis MACD
   - Detección de Cruces Dorado/Muerte (Golden/Death Cross)

2. **Análisis de Tendencia**
   - Comparación del precio actual con SMA 200
   - Clasificación de tendencia: alcista/bajista con fuerza (débil/moderada/fuerte)
   - Distancia porcentual desde niveles clave

3. **RSI (Relative Strength Index)**
   - Período de 14 días por defecto
   - Detección de sobrecompra (>70) y sobreventa (<30)
   - Señales de momentum alcista/bajista

4. **MACD (Moving Average Convergence Divergence)**
   - Configuración estándar (12, 26, 9)
   - Detección de cruces alcistas/bajistas
   - Histograma para análisis de momentum

5. **Bandas de Bollinger**
   - Período de 20 días, 2 desviaciones estándar
   - Identificación de zonas de sobrecompra/sobreventa
   - Posición del precio dentro de las bandas

6. **Análisis de Volumen**
   - Comparación con media móvil de 20 períodos
   - Detección de volumen anormal (alto/bajo)
   - Confirmación de movimientos de precio

7. **Patrones de Velas**
   - Doji: Indecisión del mercado
   - Inside Bar: Consolidación
   - Velas extremas: Movimientos fuertes alcistas/bajistas

8. **Soporte y Resistencia**
   - Niveles estáticos basados en puntos pivote
   - Niveles dinámicos usando SMA 50 y 200
   - Identificación automática de mínimos y máximos locales

9. **Recomendación Integral**
   - Análisis ponderado de todos los indicadores
   - Puntuación de sentimiento (-100 a +100)
   - Recomendación clara: STRONG BUY/BUY/WEAK BUY/HOLD/WEAK SELL/SELL/STRONG SELL

### Marco de Tiempo

El análisis técnico se puede realizar con diferentes períodos:
- Corto plazo: 30 días
- Medio plazo: 90 días (por defecto)
- Largo plazo: 180-365 días

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