# ⚙️ Configuration Directory

This directory contains configuration files and settings for the CreepyPasta AI application.

## 📁 Contents

- **Application Settings**: Core configuration parameters
- **Service Configurations**: API keys and service-specific settings
- **Processing Parameters**: Audio, video, and content generation settings

## 🔧 Configuration Files

### `settings.yaml`
Main application configuration file containing:

- **Reddit Settings**: Subreddit preferences, filtering criteria, and API parameters
- **TTS Configuration**: Text-to-speech provider settings and voice options
- **Audio Processing**: Background music, volume levels, and audio format settings
- **Video Generation**: Video quality, resolution, and rendering options
- **Content Filtering**: Story quality thresholds and content validation rules

## 🔑 Environment Variables

Configuration also relies on environment variables defined in `.env` (located in project root):

```env
# API Keys and Credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
OPENAI_API_KEY=your_openai_key
AZURE_SPEECH_KEY=your_azure_key

# Application Settings
NUM_STORIES=10
DEBUG=false
```

## 📝 Configuration Structure

```yaml
reddit:
  subreddit: "creepypasta"
  limit: 10
  min_score: 5
  min_length: 500
  max_length: 10000

tts:
  provider: "openai"  # Options: gtts, openai, azure
  voice_settings:
    speed: 1.0
    pitch: 0.0

audio:
  background_music: true
  format: "mp3"
  quality: "high"
  volume_mixing:
    narration: 1.0
    background: 0.3

video:
  enabled: true
  resolution: "1080p"
  format: "mp4"
  fps: 30
```

## 🛠️ Customization

### Modifying Settings

1. **Edit settings.yaml**: Adjust application parameters
2. **Update .env**: Modify API keys and credentials
3. **Restart Application**: Changes take effect after restart

### Common Adjustments

- **Story Filtering**: Adjust `min_score`, `min_length`, `max_length`
- **Audio Quality**: Modify `tts.provider` and `audio.quality`
- **Video Output**: Change `video.resolution` and `video.format`
- **Content Volume**: Adjust `reddit.limit` for batch processing

## 🔒 Security Considerations

- **API Keys**: Never commit sensitive credentials to version control
- **Environment Files**: Keep `.env` files private and secure
- **Access Permissions**: Restrict configuration file access as needed
- **Key Rotation**: Regularly update API keys and credentials

## 📊 Performance Tuning

- **Batch Sizes**: Adjust processing limits based on system capabilities
- **Quality vs Speed**: Balance output quality with processing time
- **Resource Usage**: Configure based on available system resources
- **Caching Settings**: Optimize for performance vs storage trade-offs

## 🔄 Backup and Recovery

- **Configuration Backup**: Regularly backup configuration files
- **Version Control**: Track configuration changes for rollback capability
- **Documentation**: Document custom settings and their purposes
- **Testing**: Validate configuration changes in development environment
