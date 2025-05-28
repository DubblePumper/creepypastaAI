# 🌍 Multilingual Support - CreepyPasta AI

CreepyPasta AI ondersteunt volledig meertalige content generatie, waarmee je stories kunt vertalen en TTS-audio kunt genereren in verschillende talen met taal-specifieke stemmen.

## 🎯 Overzicht

De multilingual ondersteuning biedt:
- **Automatische Vertaling**: Reddit stories vertalen naar je gewenste taal
- **Taal-specifieke Stemmen**: Verschillende stemmen per taal voor natuurlijke uitspraak
- **Dynamisch Taalbeheer**: Talen in- en uitschakelen tijdens runtime
- **Meerdere Vertaalproviders**: Keuze uit verschillende vertaalservices
- **Batch Processing**: Meerdere talen tegelijk verwerken

## 🌐 Ondersteunde Talen

| Code | Taal | Native Name | TTS Support |
|------|------|-------------|-------------|
| `en` | English | English | ✅ Volledig |
| `nl` | Dutch | Nederlands | ✅ Volledig |
| `de` | German | Deutsch | ✅ Volledig |
| `fr` | French | Français | ✅ Volledig |
| `es` | Spanish | Español | ✅ Volledig |
| `it` | Italian | Italiano | ✅ Volledig |
| `pt` | Portuguese | Português | ✅ Volledig |
| `ru` | Russian | Русский | ✅ Volledig |
| `ja` | Japanese | 日本語 | ✅ Volledig |
| `ko` | Korean | 한국어 | ✅ Volledig |
| `zh` | Chinese | 中文 | ✅ Volledig |
| `ar` | Arabic | العربية | ⚠️ Beperkt |
| `hi` | Hindi | हिन्दी | ⚠️ Beperkt |

## ⚙️ Configuratie

### Basis Configuratie (settings.yaml)

```yaml
# Multilingual Configuration
multilingual:
  enabled: true
  default_language: "en"
  
  # Enabled languages (runtime can override)
  enabled_languages:
    en: true    # English (altijd enabled als default)
    nl: true    # Dutch
    de: false   # German (disabled)
    fr: false   # French (disabled)
    es: false   # Spanish (disabled)
    
  # Translation settings
  translation:
    provider: "google"  # google, deepl, azure, libre
    detect_source_language: true
    preserve_formatting: true
    cache_translations: true
    
    # Provider-specific settings
    google:
      service_key_path: null  # Path to service account JSON (optional)
    
    deepl:
      formality: "default"  # default, more, less, prefer_more, prefer_less
    
  # Language-specific voice configurations
  voices:
    en:
      elevenlabs: "3SF4rB1fGBMXU9xRM7pz"  # Rachel (creepy/dramatic)
      openai: "onyx"
      azure: "en-US-AriaNeural"
      gtts: "en"
    
    nl:
      elevenlabs: "pNInz6obpgDQGcFmaJgB"  # Dutch voice
      openai: "nova"
      azure: "nl-NL-ColetteNeural"
      gtts: "nl"
    
    de:
      elevenlabs: "ErXwobaYiN019PkySvjV"  # German voice
      openai: "alloy"
      azure: "de-DE-KatjaNeural"
      gtts: "de"
    
    fr:
      elevenlabs: "EXAVITQu4vr4xnSDxMaL"  # French voice
      openai: "shimmer"
      azure: "fr-FR-DeniseNeural"
      gtts: "fr"
```

### Environment Variables

Voor bepaalde vertaalservices heb je API keys nodig:

```bash
# Google Translate (optioneel, gebruikt gratis service als niet ingesteld)
GOOGLE_TRANSLATE_API_KEY=your_google_api_key

# DeepL (voor premium vertaalservice)
DEEPL_API_KEY=your_deepl_api_key

# Azure Translator (Microsoft)
AZURE_TRANSLATOR_KEY=your_azure_key
AZURE_TRANSLATOR_REGION=your_region
```

## 🎮 Gebruik

### CLI Commando's

#### Taalbeheer

```bash
# Alle ondersteunde talen weergeven
python main.py --list-languages

# Huidige taalstatus bekijken
python main.py --language-status

# Momenteel ingeschakelde talen tonen
python main.py --list-enabled

# Taal inschakelen (runtime)
python main.py --enable-language nl
python main.py --enable-language de

# Taal uitschakelen (runtime)
python main.py --disable-language fr

# ⚠️ Opmerking: Runtime wijzigingen zijn tijdelijk
# Voor permanente wijzigingen: bewerk config/settings.yaml
```

#### Content Generatie

```bash
# Complete workflow in het Nederlands met vertaling
python main.py --mode complete --language nl --translate --stories 5

# Alleen audio genereren in het Duits
python main.py --mode audio --language de

# Specifieke vertaalprovider gebruiken
python main.py --language fr --translate --translation-provider deepl

# Meerdere talen verwerken (batch)
python main.py --languages nl,de,fr --translate --stories 3

# Video's genereren in het Spaans
python main.py --mode video --language es --translate
```

### Programmatisch Gebruik

```python
from src.utils.language_manager import LanguageManager
from src.utils.translation_manager import TranslationManager
from src.audio.tts_manager import TTSManager

# Initialize components
config = ConfigManager()
lang_manager = LanguageManager(config)
translator = TranslationManager(config)
tts_manager = TTSManager(config)

# Check available languages
enabled_langs = lang_manager.get_enabled_languages()
print(f"Enabled languages: {enabled_langs}")

# Enable a language
lang_manager.enable_language('nl')

# Translate content
story_text = "This is a scary story about shadows."
dutch_text = translator.translate_text(story_text, target_language='nl')

# Generate TTS in Dutch
tts_manager.set_language('nl')
audio_file = tts_manager.generate_speech(dutch_text, "scary_story_nl.mp3")
```

## 🔄 Workflow Integratie

### Automatische Vertaling Workflow

1. **Story Scraping**: Stories worden opgehaald van Reddit in originele taal (meestal Engels)
2. **Taaldetectie**: Automatische detectie van de brontaal
3. **Vertaling**: Content wordt vertaald naar de doeltaal
4. **TTS Generatie**: Audio wordt gegenereerd met taal-specifieke stemmen
5. **Audio Mixing**: Achtergrondmuziek wordt toegevoegd
6. **Video Creatie**: Video's worden gemaakt met ondertitels in de doeltaal

### Batch Processing

```bash
# Multiple languages in één run
python main.py \
  --mode complete \
  --languages "nl,de,fr" \
  --translate \
  --stories 3 \
  --translation-provider google
```

## 🎵 Taal-specifieke Stemmen

### ElevenLabs Stemmen

Elke taal heeft geoptimaliseerde stemmen voor horror content:

- **English**: Rachel (dramatisch, spannend)
- **Dutch**: Nederlandse stem (natuurlijk accent)
- **German**: Duitse stem (grimmige undertone)
- **French**: Franse stem (mysterieus)
- **Spanish**: Spaanse stem (expressief)

### OpenAI Stemmen

Voor verschillende stemkarakteristieken:

- **Onyx**: Diep, mannelijk (geschikt voor donkere verhalen)
- **Nova**: Vrouwelijk, helder (voor diverse content)
- **Alloy**: Neutrale stem (universeel geschikt)

## 🛠️ Troubleshooting

### Veelvoorkomende Problemen

**Vertaling werkt niet:**
```bash
# Check vertaalprovider status
python demo_multilingual.py

# Test met verschillende provider
python main.py --language nl --translate --translation-provider google
```

**TTS stem niet beschikbaar:**
```bash
# Check beschikbare stemmen
python main.py --language-status

# Test met alternatieve provider
python main.py --language de --tts gtts  # Fallback naar Google TTS
```

**Taal niet ingeschakeld:**
```bash
# Enable taal eerst
python main.py --enable-language es

# Of bewerk config/settings.yaml permanent
```

### Debug Mode

```bash
# Verbose output voor troubleshooting
python main.py --mode complete --language nl --translate --verbose --debug
```

## 🎯 Best Practices

### Taalconfiguratie

1. **Start Klein**: Begin met 2-3 talen die je goed kent
2. **Test Stemmen**: Probeer verschillende stemmen per taal uit
3. **Vertaalkwaliteit**: Test vertaalkwaliteit met korte fragmenten eerst
4. **Performance**: Meer talen = langere processing tijd

### Vertaaloptimalisatie

1. **Provider Selectie**: 
   - Google: Gratis, goede kwaliteit voor de meeste talen
   - DeepL: Premium kwaliteit voor Europese talen
   - Azure: Enterprise grade, consistente resultaten

2. **Content Voorbereiding**:
   - Korte zinnen vertalen beter dan lange paragrafen
   - Vermijd Reddit-specifieke markup vóór vertaling
   - Test eerst met sample content

### Audio Kwaliteit

1. **Taal-specifieke Stemmen**: Gebruik native speakers waar mogelijk
2. **Audio Settings**: Pas speech rate aan per taal (sommige talen zijn sneller)
3. **Achtergrondmuziek**: Houd hetzelfde volume voor consistentie

## 📚 Voorbeelden

### Quick Start Nederlands

```bash
# 1. Nederlandse taal inschakelen
python main.py --enable-language nl

# 2. Stories genereren in het Nederlands
python main.py --mode complete --language nl --translate --stories 3

# 3. Resultaat bekijken
ls assets/output/*nl*
```

### Batch Processing Voorbeeld

```bash
# Meerdere talen tegelijk
python main.py \
  --mode complete \
  --languages "nl,de,fr" \
  --translate \
  --stories 2 \
  --output assets/multilingual

# Check resultaten
ls assets/multilingual/
```

### Custom Voice Setup

```python
# Eigen stem configureren
config = ConfigManager()
config.set("multilingual.voices.nl.elevenlabs", "your_voice_id")

# Test de nieuwe stem
tts_manager = TTSManager(config)
tts_manager.set_language('nl')
tts_manager.generate_speech("Test in het Nederlands", "test_nl.mp3")
```

## 🚀 Geavanceerd Gebruik

### Custom Translation Provider

```python
class CustomTranslationProvider:
    def translate(self, text: str, target_lang: str) -> str:
        # Your custom translation logic
        return translated_text

# Register provider
translator = TranslationManager(config)
translator.register_provider("custom", CustomTranslationProvider())
```

### Language-specific Post-processing

```python
def process_translated_content(content: str, language: str) -> str:
    if language == 'nl':
        # Dutch-specific formatting
        content = content.replace('...', '…')
    elif language == 'de':
        # German-specific formatting
        content = content.replace('"', '„') + '"'
    return content
```

---

💡 **Tips**: 
- Test altijd nieuwe taalconfiguraties met korte stories eerst
- Houd een backup van je werkende configuratie
- Monitor audio kwaliteit bij het wijzigen van stemmen
- Gebruik `--debug` voor gedetailleerde logging

Voor meer hulp, zie de [Troubleshooting Guide](docs/troubleshooting.md) of open een issue op GitHub.
