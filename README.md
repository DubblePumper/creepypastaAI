# CreepyPasta AI 🎭👻

**AI-powered creepypasta story narration with atmospheric audio experiences**

CreepyPasta AI automatically scrapes horror stories from Reddit's r/creepypasta subreddit, converts them to realistic speech using AI text-to-speech technology, and creates immersive audio experiences with scary background music and atmospheric effects.

## ✨ Features

- **Automated Story Scraping**: Fetches stories from Reddit with intelligent filtering
- **Multiple TTS Providers**: Supports Google TTS, OpenAI TTS, and Azure Speech Services
- **Atmospheric Audio**: Combines narration with background music and effects
- **Smart Text Processing**: Cleans and optimizes text for better speech synthesis
- **Configurable Pipeline**: Flexible configuration system for all components
- **Professional Code Quality**: Well-structured, documented, and tested codebase

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Reddit API credentials (free)
- Optional: OpenAI or Azure API keys for premium TTS

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/creepypastaAI.git
   cd creepypastaAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env with your API credentials
   notepad .env
   ```

4. **Get Reddit API credentials**
   - Go to https://www.reddit.com/prefs/apps
   - Create a new application (choose "script")
   - Add your credentials to the `.env` file

5. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
creepypastaAI/
├── src/                          # Source code
│   ├── scrapers/                 # Data scraping modules
│   │   └── reddit_scraper.py     # Reddit API integration
│   ├── audio/                    # Audio processing modules
│   │   ├── tts_manager.py        # Text-to-speech conversion
│   │   └── audio_mixer.py        # Audio mixing and effects
│   └── utils/                    # Utility modules
│       ├── config_manager.py     # Configuration management
│       ├── story_processor.py    # Text processing and cleaning
│       └── logger.py             # Logging configuration
├── assets/                       # Static assets
│   ├── images/                   # Background images
│   ├── music/                    # Background music files
│   └── output/                   # Generated audio files
├── config/                       # Configuration files
│   └── settings.yaml             # Main configuration
├── tests/                        # Test files
├── docs/                         # Documentation
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── .env.example                  # Environment variables template
```

## ⚙️ Configuration

The application uses a YAML configuration file (`config/settings.yaml`) for all settings:

### Reddit Settings
```yaml
reddit:
  subreddit: "creepypasta"
  allowed_flairs:
    - "Text Story"
    - "Very Short Story"
  sort_by: "hot"
  limit: 25
```

### TTS Settings
```yaml
tts:
  provider: "gtts"  # gtts, openai, azure
  language: "en"
  
  # OpenAI settings (premium)
  openai:
    model: "tts-1"
    voice: "onyx"
    
  # Azure settings (premium)
  azure:
    voice: "en-US-AriaNeural"
```

### Audio Settings
```yaml
audio:
  volume:
    narration: 0.8
    background_music: 0.3
  background_music:
    enabled: true
    fade_in_duration: 2.0
```

## 🎵 Adding Background Music

1. Place your audio files in the `assets/music/` directory
2. Supported formats: MP3, WAV
3. The application will randomly select music for each story
4. Music is automatically looped and faded to match story duration

## 🔧 Advanced Usage

### Using Premium TTS Providers

**OpenAI TTS** (High quality, paid):
```bash
# Add to .env
OPENAI_API_KEY=your_api_key_here

# Update config/settings.yaml
tts:
  provider: "openai"
```

**Azure Speech Services** (Enterprise grade, paid):
```bash
# Add to .env
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=your_region_here

# Update config/settings.yaml
tts:
  provider: "azure"
```

### Custom Story Processing

Modify `src/utils/story_processor.py` to customize:
- Text cleaning rules
- Length requirements
- Content filtering
- Reading level analysis

### Audio Effects

Enhance `src/audio/audio_mixer.py` to add:
- Reverb and echo effects
- Dynamic volume control
- Advanced audio filtering
- Multi-track mixing

## 🧪 Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📊 Monitoring and Logging

The application provides comprehensive logging:

- **Console output**: Real-time status with color coding
- **File logging**: Detailed logs saved to `logs/creepypasta_ai.log`
- **Error tracking**: Automatic error capture and reporting
- **Performance metrics**: Processing time and success rates

## 🛠️ Development Guidelines

### Code Quality Standards

- **Clean Architecture**: Separation of concerns with distinct modules
- **Type Hints**: Full type annotation for better IDE support
- **Documentation**: Comprehensive docstrings for all functions
- **Error Handling**: Graceful error handling with proper logging
- **Testing**: Unit tests for all core functionality

### Code Organization

- **Modular Design**: Each component is independently testable
- **Configuration-Driven**: All settings externalized to config files
- **Dependency Injection**: Clean dependency management
- **Single Responsibility**: Each class/function has a single purpose

### Best Practices

- **Environment Variables**: Sensitive data stored securely
- **Version Control**: Meaningful commit messages and branching
- **Code Formatting**: Automated formatting with Black
- **Linting**: Code quality checks with Flake8
- **Type Checking**: Static analysis with MyPy

## 🔐 Security Considerations

- **API Keys**: Never commit credentials to version control
- **Rate Limiting**: Respectful API usage with built-in delays
- **Input Validation**: All user inputs are sanitized
- **Error Messages**: No sensitive information in error outputs
- **Dependencies**: Regular security updates for all packages

## 🚀 Performance Optimization

- **Caching**: TTS results cached to avoid regeneration
- **Async Processing**: Parallel processing where possible
- **Memory Management**: Efficient handling of large audio files
- **File Compression**: Optimized output formats
- **Resource Cleanup**: Proper cleanup of temporary files

## 📈 Monitoring and Analytics

- **Success Rates**: Track processing success/failure ratios
- **Performance Metrics**: Monitor processing times
- **Quality Metrics**: Audio quality and duration statistics
- **Error Analysis**: Categorized error reporting
- **Usage Patterns**: Story preferences and trends

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow coding standards**: Run `black`, `flake8`, and `mypy`
4. **Add tests**: Ensure new functionality is tested
5. **Update documentation**: Keep docs current
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy pytest

# Set up pre-commit hooks
pip install pre-commit
pre-commit install

# Run quality checks
black src/
flake8 src/
mypy src/
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Reddit API**: For providing access to creepypasta content
- **PRAW**: Python Reddit API Wrapper library
- **gTTS**: Google Text-to-Speech library
- **Pydub**: Audio processing capabilities
- **Pygame**: Audio playback functionality

## 📞 Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/creepypastaAI/issues)
- **Discussions**: Join conversations on [GitHub Discussions](https://github.com/yourusername/creepypastaAI/discussions)
- **Documentation**: Full docs available in the `docs/` directory

## 🗺️ Roadmap

- [ ] **Video Generation**: Create atmospheric videos with images
- [ ] **Voice Cloning**: Custom voice training for unique narrators  
- [ ] **Interactive Mode**: Real-time story selection and playback
- [ ] **Web Interface**: Browser-based control panel
- [ ] **Mobile App**: Companion mobile application
- [ ] **Podcast Export**: Automated podcast generation and distribution

---

**Made with 💀 for horror story enthusiasts**
