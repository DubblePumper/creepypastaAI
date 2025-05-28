# Translation System

This directory contains the modular translation system for the CreepyPasta AI project. The system has been reorganized from a monolithic structure to a modular, provider-based architecture for better maintainability and extensibility.

## Architecture Overview

The translation system consists of:

1. **Base Abstract Class** (`base_translator.py`) - Defines the interface for all translation providers
2. **Individual Providers** (`providers/`) - Separate implementations for each translation service
3. **Translation Manager** (`translation_manager.py`) - Coordinates multiple providers with fallback support
4. **Configuration Examples** (`config_examples.py`) - Sample configurations for different use cases

## Directory Structure

```
translation/
├── __init__.py                    # Main package exports
├── base_translator.py             # Abstract base class
├── translation_manager.py         # Main translation coordinator
├── config_examples.py             # Configuration examples
├── test_translation.py            # Test suite
├── README.md                      # This file
└── providers/                     # Translation provider implementations
    ├── __init__.py               # Provider registry
    ├── google_translate.py       # Google Translate (googletrans)
    ├── deepl.py                  # DeepL (deep-translator)
    ├── deepl_api.py             # Official DeepL API
    ├── azure_translator.py      # Azure Translator
    ├── openai_translator.py     # OpenAI GPT translation
    └── libretranslate.py        # LibreTranslate (open source)
```

## Available Providers

| Provider | API Key Required | Quality | Cost | Notes |
|----------|------------------|---------|------|-------|
| Google Translate | No | Good | Free | Uses googletrans library |
| DeepL (free) | No | Excellent | Free (limited) | Uses deep-translator |
| DeepL API | Yes | Excellent | Paid | Official DeepL API |
| Azure Translator | Yes | Excellent | Paid | Microsoft Cognitive Services |
| OpenAI | Yes | Excellent | Paid | GPT-based contextual translation |
| LibreTranslate | Optional | Good | Free | Open source, self-hostable |

## Quick Start

### Basic Usage (Google Translate)

```python
from src.utils.translation import TranslationManager

# Create manager with default configuration (Google Translate)
translator = TranslationManager({
    'primary_provider': 'google',
    'providers': {'google': {}}
})

# Translate text
result = translator.translate_text("Hello world", "es")
print(result['translated_text'])  # "Hola mundo"

# Detect language
detection = translator.detect_language("Bonjour le monde")
print(detection['language_code'])  # "fr"
```

### Multiple Providers with Fallback

```python
from src.utils.translation import TranslationManager

config = {
    'primary_provider': 'deepl_api',
    'fallback_providers': ['google', 'azure'],
    'providers': {
        'deepl_api': {'api_key': 'your-deepl-key'},
        'google': {},
        'azure': {
            'api_key': 'your-azure-key',
            'region': 'your-region'
        }
    }
}

translator = TranslationManager(config)
result = translator.translate_text("Creative horror story", "fr")
```

### Legacy Compatibility

```python
# Old import still works (with deprecation warning)
from src.utils.translation_manager import TranslationManager

translator = TranslationManager()
translated = translator.translate("Hello", "es")  # Legacy method
```

## Configuration

### Environment Variables

Set these environment variables for automatic configuration:

```bash
# Primary provider
export TRANSLATION_PRIMARY_PROVIDER=deepl_api

# API keys
export DEEPL_API_KEY=your-deepl-key
export AZURE_TRANSLATOR_KEY=your-azure-key
export AZURE_TRANSLATOR_REGION=your-region
export OPENAI_API_KEY=your-openai-key

# Optional services
export LIBRETRANSLATE_URL=https://libretranslate.de
```

Then use the environment-based configuration:

```python
from src.utils.translation.config_examples import get_config_from_env
from src.utils.translation import TranslationManager

config = get_config_from_env()
translator = TranslationManager(config)
```

### Configuration Examples

See `config_examples.py` for complete configuration examples:

- `BASIC_CONFIG` - Google Translate only
- `MULTI_PROVIDER_CONFIG` - Multiple providers with fallback
- `PRODUCTION_CONFIG` - High-quality paid services
- `DEVELOPMENT_CONFIG` - Free services for development
- `CREATIVE_WRITING_CONFIG` - Optimized for creative content

## Provider-Specific Notes

### Google Translate
- No API key required
- Uses the `googletrans` library
- May be rate-limited
- Good for basic translation needs

### DeepL (deep-translator)
- Free tier with limitations
- Excellent quality
- No API key required
- Limited language support

### DeepL API
- Requires official DeepL API key
- Excellent quality
- Usage tracking and billing
- Professional service

### Azure Translator
- Requires Azure Cognitive Services account
- Excellent quality with customization options
- Pay-per-use model
- Enterprise features

### OpenAI
- Requires OpenAI API key
- Best for creative/contextual content
- Higher cost per translation
- Maintains tone and style well

### LibreTranslate
- Open source and self-hostable
- Free public instances available
- Good quality
- Privacy-focused option

## Adding New Providers

To add a new translation provider:

1. Create a new file in `providers/` directory
2. Implement the `BaseTranslationProvider` interface
3. Add the provider to `providers/__init__.py`
4. Update documentation

Example skeleton:

```python
from ..base_translator import BaseTranslationProvider

class MyProvider(BaseTranslationProvider):
    PROVIDER_NAME = "myprovider"
    
    def __init__(self, config):
        super().__init__(config)
        # Initialize your provider
    
    def is_available(self):
        # Check if provider is available
        return True
    
    def translate_text(self, text, target_language, source_language=None):
        # Implement translation
        pass
    
    def detect_language(self, text):
        # Implement language detection
        pass
    
    def get_supported_languages(self):
        # Return list of supported language codes
        pass
```

## Testing

Run the test suite to verify everything works:

```bash
cd src/utils/translation
python test_translation.py
```

The test suite checks:
- Import functionality
- Basic translation
- Language detection
- Provider information
- Legacy compatibility
- Health checking

## Migration from Old System

The old monolithic `translation_manager.py` has been replaced with a backward-compatible version that uses the new modular system. Existing code should continue to work with deprecation warnings.

### Recommended Migration Steps

1. Update imports to use the new modular system:
   ```python
   # Old
   from src.utils.translation_manager import TranslationManager
   
   # New
   from src.utils.translation import TranslationManager
   ```

2. Update method calls to use the new interface:
   ```python
   # Old
   result = manager.translate("text", "es")
   
   # New
   result = manager.translate_text("text", "es")
   translated = result['translated_text']
   ```

3. Update configuration to use the new format (see examples)

## Error Handling

The new system provides detailed error information:

```python
result = translator.translate_text("Hello", "xx")  # Invalid language
if not result['success']:
    print(f"Translation failed: {result['error']}")
    print(f"Provider used: {result['provider_used']}")
```

## Performance Considerations

- The system automatically falls back to alternative providers if the primary fails
- Provider health is checked before use
- Consider caching translations for repeated content
- Rate limiting varies by provider

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're using the correct import paths
2. **Provider Unavailable**: Check API keys and network connectivity
3. **Language Not Supported**: Verify language codes are correct
4. **Rate Limiting**: Consider using multiple providers or caching

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Translation operations will now show debug info
```

### Health Check

Use the health check to diagnose issues:

```python
health = translator.health_check()
print(health)
```

## Future Enhancements

Planned improvements include:

- Translation caching system
- Batch translation optimization
- Custom language model support
- Translation quality scoring
- Usage analytics and monitoring
- Web UI for translation management

## Contributing

When contributing to the translation system:

1. Follow the existing code structure
2. Implement the `BaseTranslationProvider` interface
3. Add comprehensive error handling
4. Include unit tests
5. Update documentation
6. Consider backward compatibility
