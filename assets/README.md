# 🎨 Assets Directory

This directory contains all static assets used by the CreepyPasta AI application, including media files, generated content, and resources.

## 📁 Directory Structure

```
assets/
├── images/          # AI-generated horror imagery and image cache
├── music/           # Background music and audio tracks
├── output/          # Generated audio files (MP3, WAV)
└── videos/          # Generated video content and final outputs
```

## 🎯 Purpose

The assets directory serves as the central storage location for:
- **Generated Content**: All AI-created audio, video, and image files
- **Source Media**: Background music, sound effects, and base assets
- **Output Files**: Final processed content ready for distribution
- **Cache Files**: Performance optimization through asset caching

## 🔄 Workflow Integration

1. **Image Generation**: AI-created horror visuals are stored in `images/`
2. **Audio Processing**: Background music from `music/` is mixed with TTS narration
3. **Output Creation**: Final audio files are saved to `output/`
4. **Video Production**: Complete videos are stored in `videos/`

## 🛠️ Management

- Files are automatically organized by timestamp and content type
- Cache files improve performance by avoiding regeneration
- Output files can be safely deleted to free space (they can be regenerated)
- Source music files should be preserved for consistent audio quality

## 📝 Notes

- Large files may be generated here - monitor disk space
- Generated content is tagged with timestamps for version tracking
- Audio files are normalized for consistent volume levels
- Video files include both raw footage and final processed outputs
