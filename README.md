# CreepyPasta AI 🎭👻

**AI-powered creepypasta story narration with atmospheric audio and video experiences**

CreepyPasta AI is a comprehensive horror content generation system that automatically scrapes stories from Reddit's r/creepypasta subreddit, converts them to realistic speech using AI text-to-speech technology, and creates immersive multimedia experiences with atmospheric audio and video content.

## ✨ Features

- **Automated Story Scraping**: Fetches stories from Reddit with intelligent filtering and duplicate detection
- **JSON Database Storage**: Comprehensive story tracking with metadata (title, content, URL, timestamps)
- **Smart Duplicate Prevention**: Automatically skips stories that already exist in the database
- **Modular Execution Modes**: Run individual components or complete workflow independently
- **Multiple TTS Providers**: Supports Google TTS (free), OpenAI TTS, and Azure Speech Services
- **Automatic Fallback System**: Gracefully falls back to free TTS when premium APIs fail
- **Video Generation**: Creates atmospheric horror videos with AI-generated imagery
- **Atmospheric Audio**: Combines narration with background music and sound effects
- **Smart Text Processing**: Cleans and optimizes text for better speech synthesis
- **Cross-Platform Support**: Fully compatible with Windows, macOS, and Linux
- **CLI Interface**: Command-line tools for flexible workflow management
- **Professional Code Quality**: Well-structured, documented, and thoroughly tested codebase
- **Python 3.13 Compatible**: Fully supports the latest Python version

## 🏗️ Project Structure

The project follows software engineering best practices with clear separation of concerns and logical organization:

```
creepypastaAI/
├── src/                    # Source code modules
│   ├── audio/              # Audio processing components
│   │   ├── tts_manager.py  # Text-to-speech management
│   │   └── audio_mixer.py  # Audio mixing and effects
│   ├── cli/                # Command-line interface
│   │   ├── cli_handler.py  # Argument parsing and validation
│   │   └── execution_modes.py # Mode-specific execution handlers
│   ├── scrapers/           # Data collection modules
│   │   └── reddit_scraper.py # Reddit API integration
│   ├── utils/              # Utility modules
│   │   ├── config_manager.py  # Configuration handling
│   │   ├── story_processor.py # Text processing and validation
│   │   ├── story_tracker.py   # JSON database management
│   │   └── logger.py          # Logging utilities
│   └── video/              # Video generation components
│       └── video_generator.py # Video creation and effects
├── config/                 # Configuration files
│   └── settings.yaml      # Main application configuration
├── data/                   # Persistent data storage
│   └── generated_stories.json # Story database with metadata
├── assets/                 # Static assets and generated content
│   ├── images/            # AI-generated horror imagery
│   ├── music/             # Background music and sound effects
│   ├── output/            # Generated audio files
│   └── videos/            # Generated video content
├── tests/                  # Test modules and validation
│   ├── results/           # Test output files (following guidelines)
│   └── *.py               # Test scripts with clear naming
├── scripts/               # Convenience execution scripts
│   ├── *.bat              # Windows batch scripts
│   ├── *.sh               # Linux/macOS shell scripts
│   └── README.md          # Script usage documentation
├── docs/                   # Project documentation
├── logs/                   # Application logs
└── main.py                # Application entry point
```

## 🏛️ Development Guidelines & Code Organization

This project follows software engineering best practices to ensure maintainability, readability, and collaboration:

### Code Organization Principles
- **Clear Structure**: Logical separation using folders and subfolders
- **Descriptive Naming**: Clear, descriptive names for files, functions, and variables
- **Separation of Concerns**: Related code grouped together, unrelated code separated
- **Single Responsibility**: Each module, class, and function has a clear, focused purpose

### Code Quality Standards
- **Clean & Readable**: Code is clean, readable, and maintainable
- **Well Documented**: Comments explain complex logic and important design decisions
- **Simplicity First**: Avoid unnecessary complexity, strive for simple solutions
- **Error Handling**: Comprehensive edge case and error handling throughout
- **Type Hints**: Use Python type hints for better code clarity and IDE support

### Testing & Validation
- **Test Coverage**: Tests in the `tests/` folder with clear naming conventions
- **Edge Cases**: Tests cover various scenarios including edge cases
- **Output Organization**: Test outputs stored in `tests/results/` with clear naming
- **Regression Prevention**: Tests prevent future regressions and ensure stability

### Version Control & Collaboration
- **Frequent Commits**: Regular commits with clear, descriptive messages
- **Branch Strategy**: Feature branches for new functionality, stable main branch
- **Code Reviews**: Pull requests enable discussions and quality assurance
- **Documentation**: Clear setup and usage instructions in README and code comments

### Security & Performance
- **Data Protection**: Best practices for handling sensitive data (API keys in environment)
- **Performance Optimization**: Profile code to identify bottlenecks, optimize thoughtfully
- **External Dependencies**: Graceful error handling for third-party services and APIs
- **Async Handling**: Proper asynchronous code patterns where applicable

### Project Dependencies
- **Dependency Management**: Well-managed and documented dependencies in `requirements.txt`
- **Framework Conventions**: Follow conventions and best practices of used libraries
- **Environment Variables**: Sensitive configuration stored in environment variables
- **Cross-Platform**: Code works consistently across Windows, macOS, and Linux

## 🔧 Execution Modes

CreepyPasta AI supports independent execution modes for maximum flexibility and development efficiency:

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Individual Components
- **Scraping Only**: `python main.py --mode scrape --stories 10`
- **Audio Only**: `python main.py --mode audio`
- **Video Only**: `python main.py --mode video`
- **System Info**: `python main.py --info`
- **Statistics**: `python main.py --stats`

### Convenience Scripts
Use provided scripts for easier execution:
- **Windows**: `scripts\complete.bat`, `scripts\scrape.bat`, `scripts\audio.bat`, `scripts\video.bat`
- **Linux/Mac**: `./scripts/complete.sh`, `./scripts/scrape.sh`, `./scripts/audio.sh`, `./scripts/video.sh`

See `scripts/README.md` for detailed usage examples.

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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

## 🔧 Execution Modes

CreepyPasta AI supports multiple execution modes for flexible workflow management:

### Complete Workflow (Default)
Runs the full pipeline: scraping → audio generation → video creation
```bash
python main.py --mode complete --stories 5
```

### Scraping Only
Scrapes and stores stories from Reddit without generating audio/video:
```bash
python main.py --mode scrape --stories 10
```

### Audio Generation Only
Generates audio files for existing stories in the database:
```bash
python main.py --mode audio
```

### Video Generation Only
Creates videos for existing audio files:
```bash
python main.py --mode video
```

### System Information
Display system configuration and statistics:
```bash
python main.py --info
python main.py --stats
```

### Convenience Scripts
Use the provided batch/shell scripts for easier execution:

**Windows:**
```cmd
scripts\complete.bat 5    # Full workflow for 5 stories
scripts\scrape.bat 10     # Scrape 10 stories only
scripts\audio.bat         # Generate audio only
scripts\video.bat         # Generate videos only
scripts\status.bat        # Show system status
```

**Linux/Mac:**
```bash
./scripts/complete.sh 5   # Full workflow for 5 stories
./scripts/scrape.sh 10    # Scrape 10 stories only
./scripts/audio.sh        # Generate audio only
./scripts/video.sh        # Generate videos only
./scripts/status.sh       # Show system status
```

### Benefits of Separate Execution
- **Development & Testing**: Test individual components
- **Error Recovery**: Resume from specific steps if failures occur
- **Resource Management**: Run resource-intensive operations separately
- **Batch Processing**: Process large numbers of stories in stages
- **Selective Processing**: Generate content for specific steps only

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
    model: "tts-1