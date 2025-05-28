# 🌐 Data Scrapers Module

This module handles data collection from external sources, primarily Reddit, for gathering creepypasta stories and content.

## 📁 Module Contents

- **Reddit Scraper**: Automated story collection from Reddit communities
- **Content Filtering**: Quality-based story filtering and validation
- **Data Processing**: Story text cleaning and optimization
- **Duplicate Detection**: Intelligent duplicate prevention and management

## 🔍 Reddit Integration

### Subreddit Support
- **Primary Source**: r/nosleep for high-quality horror stories
- **Flexible Configuration**: Support for any subreddit with story content
- **Flair Filtering**: Configurable flair-based content filtering
- **Sorting Options**: Multiple sorting methods (hot, new, top, rising)

### API Integration
- **Reddit API (PRAW)**: Official Reddit API integration
- **Authentication**: Secure API authentication with client credentials
- **Rate Limiting**: Respectful API usage with proper rate limiting
- **Error Handling**: Robust error handling for API failures

## 📊 Content Filtering

### Quality Metrics
- **Story Length**: Configurable minimum and maximum length requirements
- **Engagement Score**: Reddit upvote-based quality assessment
- **Content Validation**: Text quality and readability analysis
- **Format Compliance**: Ensure content is suitable for TTS processing

### Filtering Criteria
```yaml
reddit:
  subreddit: "nosleep"
  allowed_flairs: ["*"]    # Accept all flairs
  min_score: 5             # Minimum upvotes
  min_length: 100          # Minimum characters
  max_length: 5000         # Maximum characters
  sort_by: "top"           # Sorting method
  time_filter: "all"       # Time range filter
```

### Content Validation
- **Text Quality**: Ensure readable, coherent story content
- **Language Detection**: Verify content is in expected language
- **Format Checking**: Validate text format for TTS compatibility
- **Duplicate Prevention**: Sophisticated duplicate detection algorithms

## 🔄 Data Processing Pipeline

### Story Collection Workflow
1. **API Authentication**: Secure connection to Reddit API
2. **Subreddit Query**: Fetch posts based on configuration criteria
3. **Content Filtering**: Apply quality and length filters
4. **Duplicate Check**: Verify story hasn't been previously collected
5. **Text Processing**: Clean and optimize text for TTS processing
6. **Database Storage**: Store validated stories in local database

### Text Processing
- **Markdown Removal**: Clean Reddit markdown formatting
- **Character Normalization**: Standardize character encoding
- **Structure Optimization**: Optimize text structure for narration
- **Metadata Extraction**: Extract relevant post metadata

## 🗄️ Database Integration

### Story Storage
- **JSON Database**: Efficient local storage in JSON format
- **Metadata Tracking**: Comprehensive metadata for each story
- **Processing Status**: Track processing status for each story
- **Analytics Data**: Quality metrics and performance data

### Data Structure
```json
{
  "story_id": {
    "title": "Story Title",
    "content": "Full story text...",
    "url": "https://reddit.com/...",
    "score": 125,
    "author": "reddit_username",
    "created_date": "2025-05-28T10:30:00Z",
    "subreddit": "nosleep",
    "flair": "Story Flair",
    "length": 1250,
    "processed": false,
    "quality_score": 0.85
  }
}
```

## 🔧 Configuration Management

### Flexible Settings
- **Subreddit Selection**: Easy switching between different communities
- **Quality Thresholds**: Adjustable quality and engagement criteria
- **Processing Limits**: Configurable batch sizes and rate limits
- **Content Preferences**: Customizable content filtering preferences

### Dynamic Configuration
- **Runtime Adjustments**: Modify settings during operation
- **A/B Testing**: Compare different scraping strategies
- **Quality Tuning**: Adjust quality thresholds based on results
- **Performance Optimization**: Optimize based on system capabilities

## 🛡️ Error Handling and Resilience

### Robust Error Management
- **Network Failures**: Graceful handling of network connectivity issues
- **API Limits**: Proper handling of rate limits and quotas
- **Content Issues**: Manage problematic or malformed content
- **Authentication Errors**: Clear error messages for credential issues

### Recovery Mechanisms
- **Retry Logic**: Intelligent retry mechanisms for transient failures
- **Partial Recovery**: Continue processing after individual failures
- **Data Integrity**: Ensure database consistency during failures
- **Graceful Degradation**: Continue operation with reduced functionality

## 🔒 Security and Privacy

### Data Protection
- **API Key Security**: Secure storage and handling of credentials
- **User Privacy**: Respectful handling of user-generated content
- **Data Minimization**: Collect only necessary data
- **Compliance**: Follow Reddit's terms of service and API guidelines

### Ethical Considerations
- **Content Attribution**: Proper attribution of original authors
- **Copyright Respect**: Respect for intellectual property rights
- **Community Guidelines**: Adherence to community standards
- **Responsible Usage**: Respectful use of community resources

## 📈 Performance Optimization

### Efficient Data Collection
- **Batch Processing**: Collect multiple stories efficiently
- **Parallel Operations**: Concurrent processing where appropriate
- **Memory Management**: Efficient memory usage for large datasets
- **Network Optimization**: Minimize API calls and bandwidth usage

### Scalability Features
- **Configurable Limits**: Adjust processing limits based on system capabilities
- **Resource Monitoring**: Track system resource usage during scraping
- **Queue Management**: Manage scraping queues for optimal performance
- **Load Balancing**: Distribute processing load effectively

## 🔍 Analytics and Monitoring

### Data Quality Metrics
- **Collection Success Rate**: Track successful story collection rates
- **Quality Distribution**: Analyze quality metrics across collected content
- **Content Diversity**: Monitor variety and diversity of collected stories
- **Processing Efficiency**: Track processing times and resource usage

### Usage Analytics
- **Collection Patterns**: Understand content collection patterns
- **Quality Trends**: Identify trends in content quality over time
- **Performance Metrics**: Monitor scraper performance and efficiency
- **Error Analysis**: Analyze and learn from collection errors

## 🛠️ Maintenance and Updates

### Regular Maintenance
- **Database Cleanup**: Periodic cleanup of old or invalid entries
- **Quality Review**: Regular review of quality metrics and thresholds
- **Performance Tuning**: Ongoing optimization of scraping performance
- **Update Management**: Keep Reddit API integration current

### Future Enhancements
- **Additional Sources**: Support for additional content sources
- **Advanced Filtering**: More sophisticated content filtering algorithms
- **AI-Powered Quality**: AI-based content quality assessment
- **Real-Time Processing**: Real-time content collection and processing
