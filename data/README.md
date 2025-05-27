# 📊 Data Directory

This directory contains application data, databases, and cached information used by the CreepyPasta AI system.

## 📁 Contents

- **Story Database**: JSON files containing scraped and processed stories
- **Metadata**: Story tracking, analytics, and processing history
- **Cache Files**: Performance optimization data and processed content

## 🗄️ Database Files

### `generated_stories.json`
Primary database file containing:

- **Story Content**: Full text of scraped creepypasta stories
- **Metadata**: Reddit post information, scores, timestamps
- **Processing Status**: Generation history and status tracking
- **Content Analysis**: Story quality metrics and categorization

## 📋 Data Structure

```json
{
  "story_id": {
    "title": "Story Title",
    "content": "Full story text...",
    "url": "https://reddit.com/...",
    "score": 125,
    "created_date": "2025-05-27T10:30:00Z",
    "processed": true,
    "generated_files": {
      "audio": "path/to/audio.mp3",
      "video": "path/to/video.mp4",
      "images": ["path/to/image1.png"]
    },
    "quality_metrics": {
      "length": 1250,
      "readability": 0.85,
      "horror_score": 0.92
    }
  }
}
```

## 🔄 Data Management

### Automatic Updates
- Stories are automatically added during scraping
- Processing status is updated after audio/video generation
- Duplicate detection prevents content repetition
- Quality metrics are calculated and stored

### Manual Management
- Database can be safely backed up by copying JSON files
- Individual stories can be removed by editing JSON files
- Processing history can be reset by clearing status flags

## 📈 Analytics and Tracking

The data directory enables:
- **Content Performance**: Track which stories generate best content
- **Processing History**: Monitor generation success rates
- **Quality Metrics**: Analyze story characteristics and outcomes
- **Usage Patterns**: Understand content generation trends

## 🔒 Data Integrity

### Backup Strategies
- **Regular Backups**: Automated or manual backup schedules
- **Version Control**: Track changes to database files
- **Data Validation**: Integrity checks during application startup
- **Recovery Procedures**: Restore from backups when needed

### File Safety
- **Atomic Updates**: Database writes are performed safely
- **Lock Files**: Prevent concurrent access issues
- **Validation**: Data structure validation on load
- **Error Recovery**: Graceful handling of corrupted data

## 🧹 Maintenance

### Cleanup Operations
- **Old Data Removal**: Periodically clean up outdated entries
- **Cache Management**: Clear temporary and cache files
- **Size Monitoring**: Track database growth and optimize
- **Archival**: Move old data to archive storage

### Performance Optimization
- **Index Management**: Optimize data access patterns
- **Memory Usage**: Monitor and optimize data loading
- **Query Performance**: Efficient data retrieval methods
- **Caching Strategy**: Balance memory usage with performance

## 🛠️ Integration

The data directory integrates with:
- **Reddit Scraper**: Stores newly scraped stories
- **Content Processors**: Tracks processing status and results
- **Audio/Video Generation**: Links generated media to stories
- **Quality Analysis**: Stores content quality assessments

## 📝 Best Practices

- **Regular Monitoring**: Check data directory size and health
- **Backup Schedule**: Implement regular backup procedures
- **Access Control**: Secure sensitive data appropriately
- **Documentation**: Document custom data fields and structures
