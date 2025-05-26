# CreepyPasta AI 🎭👻

**AI-powered creepypasta story narration with atmospheric audio experiences**

CreepyPasta AI automatically scrapes horror stories from Reddit's r/creepypasta subreddit, converts them to realistic speech using AI text-to-speech technology, and creates immersive audio experiences with scary background music and atmospheric effects.

## ✨ Features

- **Automated Story Scraping**: Fetches stories from Reddit with intelligent filtering and duplicate detection
- **JSON Database Storage**: Stores scraped stories with metadata (title, content, URL) in JSON format
- **Smart Duplicate Prevention**: Automatically skips stories that already exist in the database
- **Separated Workflow**: First scrapes and stores stories, then generates audio from stored data
- **Multiple TTS Providers**: Supports Google TTS (free), OpenAI TTS, and Azure Speech Services
- **Automatic Fallback System**: Gracefully falls back to free TTS when premium APIs fail
- **Atmospheric Audio**: Combines narration with background music and sound effects
- **Smart Text Processing**: Cleans and optimizes text for better speech synthesis
- **Configurable Pipeline**: Flexible configuration system for all components
- **Professional Code Quality**: Well-structured, documented, and tested codebase
- **Python 3.13 Compatible**: Fully supports the latest Python version

## 📁 Project Structure

The project follows best practices for code organization with clear separation of concerns:

```
creepypastaAI/
├── src/                    # Source code modules
│   ├── audio/              # Audio processing components
│   │   ├── tts_manager.py  # Text-to-speech management
│   │   └── audio_mixer.py  # Audio mixing and effects
│   ├── scrapers/           # Data collection modules
│   │   └── reddit_scraper.py # Reddit API integration
│   └── utils/              # Utility modules
│       ├── config_manager.py  # Configuration handling
│       ├── story_processor.py # Text processing
│       ├── story_tracker.py   # JSON database management
│       └── logger.py          # Logging utilities
├── config/                 # Configuration files
│   └── settings.yaml      # Main configuration
├── data/                   # Persistent data storage
│   └── generated_stories.json # Story database
├── assets/                 # Static assets
│   ├── music/             # Background music files
│   └── output/            # Generated audio files
├── tests/                  # Test modules
├── docs/                   # Documentation
└── main.py                # Application entry point
```

## 🔄 Workflow

The application follows a two-phase workflow for better organization and error handling:

### Phase 1: Story Collection
1. **Scrape Reddit**: Fetch stories from r/creepypasta subreddit
2. **Process Content**: Clean and validate story text
3. **Check Duplicates**: Compare against existing stories in JSON database
4. **Store New Stories**: Save unique stories to `data/generated_stories.json`

### Phase 2: Audio Generation
1. **Load Pending Stories**: Find stories without audio files
2. **Generate TTS**: Convert text to speech using configured provider
3. **Apply Audio Effects**: Add background music and atmospheric sounds
4. **Update Database**: Mark stories as processed with audio file paths

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher** (Python 3.13 recommended)
- **Reddit API credentials** (free from Reddit)
- **Optional**: OpenAI or Azure API keys for premium TTS voices

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
   cp .env.example .env  # On Windows: copy .env.example .env
   
   # Edit .env with your API credentials
   nano .env  # On Windows: notepad .env
   ```

4. **Get Reddit API credentials**
   - Go to https://www.reddit.com/prefs/apps
   - Create a new application (choose "script")
   - Add your credentials to the `.env` file:
     ```env
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_CLIENT_SECRET=your_client_secret
     REDDIT_USER_AGENT=your_app_name
     ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Reddit API (Required)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=CreepyPastaAI/1.0

# OpenAI API (Optional - for premium TTS)
OPENAI_API_KEY=your_openai_api_key

# Azure Speech Services (Optional - for premium TTS)
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region

# Application Settings
NUM_STORIES=10
DEBUG=false
```

### Settings Configuration (`config/settings.yaml`)

```yaml
reddit:
  subreddit: "creepypasta"
  limit: 10
  min_score: 5
  min_length: 500

tts:
  provider: "openai"  # Options: gtts, openai, azure
  language: "en"
  openai:
    model: "tts-1"
    voice: "onyx"  # Options: alloy, echo, fable, onyx, nova, shimmer
  azure:
    voice: "en-US-AriaNeural"

audio:
  background_music: true
  music_volume: 0.3
  voice_volume: 0.8
  effects: true

output:
  directory: "assets/output"
  format: "mp3"
```

## 🔊 TTS Provider Configuration

### Google TTS (Free, Default Fallback)
- **No API key required**
- **Limitations**: Basic voice quality, rate limits
- **Best for**: Development, testing, backup

### OpenAI TTS (Premium, Recommended)
- **High-quality natural voices**
- **Multiple voice options**: alloy, echo, fable, onyx, nova, shimmer
- **Pricing**: Pay-per-use
- **Setup**: Add `OPENAI_API_KEY` to `.env`

### Azure Speech Services (Premium)
- **Enterprise-grade quality**
- **Wide language support**
- **Advanced features**: SSML, custom voices
- **Setup**: Add `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` to `.env`

## 🚨 Troubleshooting

### Common Issues

1. **OpenAI API Quota Exceeded (HTTP 429)**
   - The application automatically falls back to Google TTS
   - Check your OpenAI API usage and billing
   - Consider using a lower story limit in settings

2. **Audio Module Not Found (Python 3.13)**
   - This is handled automatically with `pyaudioop` package
   - If issues persist, try: `pip install --upgrade pyaudioop`

3. **Reddit API Rate Limits**
   - Reduce the story limit in `config/settings.yaml`
   - Add delays between requests if needed

4. **Audio Playback Issues**
   - Ensure pygame is properly installed
   - Check audio file permissions in output directory

### Error Recovery

The application includes comprehensive error recovery:

- **TTS Fallback**: Automatically switches to Google TTS if premium providers fail
- **Retry Logic**: Retries failed operations with exponential backoff
- **Graceful Degradation**: Continues processing remaining stories if individual stories fail
- **Detailed Logging**: All errors are logged with context for debugging

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

## 📋 Development Best Practices

This project follows strict coding standards and best practices to ensure maintainability, reliability, and collaboration:

### Code Organization
- **Modular Structure**: Code is organized into logical modules with clear separation of concerns
- **Descriptive Naming**: Functions, classes, and variables have clear, descriptive names
- **Single Responsibility**: Each module and function has a single, well-defined purpose
- **DRY Principle**: Code duplication is minimized through reusable components

### Code Quality Standards
- **Clean Code**: Code is readable, maintainable, and well-documented
- **Type Hints**: Python type annotations are used throughout for better IDE support and error detection
- **Docstrings**: All functions and classes include comprehensive documentation
- **Comments**: Complex logic includes explanatory comments for clarity

### Error Handling & Testing
- **Comprehensive Error Handling**: All potential failure points are handled gracefully
- **Unit Tests**: Critical functionality is covered by automated tests
- **Edge Case Handling**: Unusual inputs and edge cases are properly managed
- **Regression Prevention**: Tests prevent bugs from reoccurring

### Code Review & Collaboration
- **Version Control**: Git is used effectively with clear commit messages
- **Code Reviews**: All changes undergo review for quality and standards compliance
- **Documentation**: Code structure and important decisions are well-documented
- **Collaboration**: Clear guidelines for team collaboration and contribution

### Security & Performance
- **Data Protection**: Sensitive information is properly secured and not exposed
- **API Security**: Third-party API keys and credentials are safely managed
- **Performance Optimization**: Code is profiled and optimized for efficiency
- **Resource Management**: Memory and file resources are properly cleaned up

### Configuration & Deployment
- **Environment Management**: Different environments (dev, staging, prod) are properly configured
- **Dependency Management**: Dependencies are clearly documented and version-controlled
- **Deployment Ready**: Code is packaged and configured for easy deployment
- **Monitoring**: Application includes logging and monitoring capabilities

### Asynchronous Code Handling
- **Proper Async/Await**: Asynchronous operations are handled correctly
- **Error Propagation**: Async errors are properly caught and handled
- **Resource Cleanup**: Async resources are properly cleaned up
- **Performance**: Async code is optimized for performance and reliability

## 📋 Contributing Guidelines

When contributing to this project, please follow these guidelines:

1. **Code Structure**: Maintain the existing folder structure and separation of concerns
2. **Naming Conventions**: Use clear, descriptive names for all code elements
3. **Documentation**: Update documentation for any new features or changes
4. **Testing**: Add tests for new functionality and ensure existing tests pass
5. **Error Handling**: Include proper error handling for all new code paths
6. **Performance**: Consider performance implications of changes
7. **Security**: Ensure no sensitive data is exposed in the codebase
8. **Dependencies**: Document any new dependencies and their purpose

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
