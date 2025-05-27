# 🚀 Scripts Directory

This directory contains automation scripts and utilities for the CreepyPasta AI application, providing convenient shortcuts for common operations.

## 📁 Contents

- **Cross-Platform Scripts**: Both Windows (.bat) and Unix (.sh) versions
- **Operation Shortcuts**: Quick access to core application functions
- **Automation Tools**: Batch processing and workflow automation
- **Utility Scripts**: Helper tools for maintenance and management

## 🛠️ Available Scripts

## Windows Scripts (.bat)

### Complete Workflow
- **`complete.bat`** - Runs the full workflow (scrape → audio → video)
  ```cmd
  complete.bat [number_of_stories]
  ```

### Individual Components
- **`scrape.bat`** - Scrapes stories from Reddit only
  ```cmd
  scrape.bat [number_of_stories]
  ```

- **`audio.bat`** - Generates audio files for existing stories
  ```cmd
  audio.bat
  ```

- **`video.bat`** - Generates video files for existing audio
  ```cmd
  video.bat
  ```

### System Information
- **`status.bat`** - Shows system info and tracking statistics
  ```cmd
  status.bat
  ```

## Linux/Mac Scripts (.sh)

### Complete Workflow
- **`complete.sh`** - Runs the full workflow (scrape → audio → video)
  ```bash
  ./complete.sh [number_of_stories]
  ```

### Individual Components
- **`scrape.sh`** - Scrapes stories from Reddit only
  ```bash
  ./scrape.sh [number_of_stories]
  ```

- **`audio.sh`** - Generates audio files for existing stories
  ```bash
  ./audio.sh
  ```

- **`video.sh`** - Generates video files for existing audio
  ```bash
  ./video.sh
  ```

### System Information
- **`status.sh`** - Shows system info and tracking statistics
  ```bash
  ./status.sh
  ```

## Usage Examples

### Typical Workflow
1. **Scrape stories first:**
   ```cmd
   scrape.bat 10        # Windows
   ./scrape.sh 10       # Linux/Mac
   ```

2. **Generate audio:**
   ```cmd
   audio.bat            # Windows
   ./audio.sh           # Linux/Mac
   ```

3. **Create videos:**
   ```cmd
   video.bat            # Windows
   ./video.sh           # Linux/Mac
   ```

### Or run everything at once:
```cmd
complete.bat 5          # Windows
./complete.sh 5         # Linux/Mac
```

### Check system status:
```cmd
status.bat             # Windows
./status.sh            # Linux/Mac
```

## Manual Command Line Usage

You can also use the command line interface directly:

```bash
# Complete workflow
python main.py --mode complete --stories 5

# Scraping only
python main.py --mode scrape --stories 10

# Audio generation only
python main.py --mode audio

# Video generation only
python main.py --mode video

# Generate videos for ALL audio files (including existing)
python main.py --mode video --video-all

# Display system information
python main.py --info

# Display tracking statistics
python main.py --stats

# Verbose output
python main.py --mode audio --verbose

# Custom configuration file
python main.py --config custom_config.yaml
```

## Command Line Options

- `--mode` / `-m`: Execution mode (complete, scrape, audio, video)
- `--stories` / `-s`: Number of stories to process
- `--config` / `-c`: Path to configuration file
- `--info` / `-i`: Display system information and exit
- `--stats`: Display tracking statistics and exit
- `--video-all`: Generate videos for all audio files (video mode only)
- `--verbose` / `-v`: Enable verbose output
- `--force`: Force regeneration of existing files

## Benefits of Separate Execution

1. **Development and Testing**: Test individual components without running the full pipeline
2. **Selective Processing**: Generate content for specific steps only
3. **Error Recovery**: If one step fails, restart from that point
4. **Resource Management**: Run resource-intensive operations separately
5. **Batch Processing**: Process large numbers of stories in stages
