# 💻 Command Line Interface Module

This module provides the command-line interface for the CreepyPasta AI application, handling user input, argument parsing, and execution coordination.

## 📁 Module Contents

- **Argument Parsing**: Command-line argument processing and validation
- **Execution Modes**: Different operation modes and workflow management
- **User Interaction**: Interactive prompts and user feedback
- **Error Handling**: Graceful error management and user guidance

## 🔧 Command Structure

### Basic Usage
```bash
python main.py [OPTIONS] [COMMAND]
```

### Available Commands
- **Complete Workflow**: `--mode complete` - Full pipeline execution
- **Story Scraping**: `--mode scrape` - Reddit story collection only
- **Audio Generation**: `--mode audio` - TTS and audio mixing only
- **Video Creation**: `--mode video` - Video generation only
- **System Information**: `--info` - Display system status and configuration

### Command Options
- **Story Count**: `--stories N` - Number of stories to process
- **Output Directory**: `--output PATH` - Custom output location
- **Configuration**: `--config FILE` - Custom configuration file
- **Debug Mode**: `--debug` - Enable verbose logging
- **TTS Provider**: `--tts PROVIDER` - Override TTS provider

## 🎯 Execution Modes

### Complete Mode (`--mode complete`)
Executes the full workflow:
1. Scrape stories from Reddit
2. Generate TTS audio with background music
3. Create AI-generated imagery
4. Produce final video content

### Individual Component Modes
- **Scrape Mode**: Story collection and database updates
- **Audio Mode**: Audio generation for existing stories
- **Video Mode**: Video creation for existing audio/images

### Special Modes
- **Info Mode**: System status and diagnostic information
- **Stats Mode**: Database statistics and content analytics
- **Validation Mode**: Configuration and dependency validation

## 🔄 Workflow Orchestration

### Process Coordination
The CLI module coordinates between different components:
- **Configuration Loading**: Initialize application settings
- **Dependency Validation**: Verify required tools and services
- **Resource Management**: Monitor system resources and limitations
- **Progress Tracking**: Real-time progress updates and status

### Error Recovery
- **Graceful Failures**: Handle component failures without data loss
- **Resume Capability**: Resume interrupted workflows from checkpoints
- **Rollback Options**: Undo partial operations when necessary
- **User Guidance**: Provide clear next steps when errors occur

## 🛠️ User Experience Features

### Interactive Elements
- **Progress Indicators**: Visual progress bars and status updates
- **Confirmation Prompts**: User confirmation for destructive operations
- **Help System**: Comprehensive help and usage information
- **Error Explanations**: Clear, actionable error messages

### Output Management
- **Structured Logging**: Organized log output with different verbosity levels
- **Result Summaries**: Concise summaries of completed operations
- **File Location Reporting**: Clear indication of generated file locations
- **Performance Metrics**: Execution time and resource usage reporting

## 📊 Configuration Integration

### Settings Management
- **Default Configuration**: Sensible defaults for new users
- **Custom Overrides**: Command-line overrides for configuration values
- **Environment Variables**: Integration with environment-based configuration
- **Validation**: Configuration validation and error reporting

### Dynamic Configuration
- **Runtime Adjustments**: Modify settings during execution
- **Provider Switching**: Dynamic switching between TTS providers
- **Quality Adjustments**: Real-time quality and performance tuning
- **Resource Adaptation**: Automatic adjustment based on system capabilities

## 🔍 Debugging and Development

### Debug Features
- **Verbose Logging**: Detailed execution information
- **Step-by-Step Mode**: Execute workflow with pauses between steps
- **Component Isolation**: Test individual components separately
- **Performance Profiling**: Detailed timing and resource usage analysis

### Development Tools
- **Dry Run Mode**: Simulate operations without making changes
- **Configuration Testing**: Validate configuration without execution
- **API Testing**: Test external service connectivity
- **File System Testing**: Verify file system permissions and space

## 🚀 Performance and Reliability

### Optimization Features
- **Efficient Argument Parsing**: Fast command-line processing
- **Memory Management**: Minimal memory footprint for CLI operations
- **Resource Monitoring**: Track and report resource usage
- **Background Processing**: Non-blocking operations where appropriate

### Reliability Measures
- **Input Validation**: Comprehensive validation of user input
- **Error Prevention**: Proactive error detection and prevention
- **Safe Defaults**: Conservative default settings to prevent issues
- **Recovery Mechanisms**: Automatic recovery from common failure scenarios

## 🔧 Extension and Customization

### Plugin Architecture
- **Command Extensions**: Add new commands and operations
- **Custom Modes**: Implement custom workflow modes
- **Output Formatters**: Custom output formatting and presentation
- **Integration Points**: Hooks for external tool integration

### Configuration Extensions
- **Custom Arguments**: Add application-specific command-line arguments
- **Validation Rules**: Custom validation for configuration parameters
- **Help Customization**: Custom help text and documentation
- **Internationalization**: Support for multiple languages

## 📚 Usage Examples

### Basic Operations
```bash
# Generate 5 complete stories
python main.py --mode complete --stories 5

# Scrape 10 stories only
python main.py --mode scrape --stories 10

# Generate audio for existing stories
python main.py --mode audio

# Create videos with debug information
python main.py --mode video --debug
```

### Advanced Usage
```bash
# Custom configuration and output
python main.py --config custom.yaml --output /custom/path --stories 3

# Use specific TTS provider
python main.py --tts elevenlabs --mode complete

# System information and validation
python main.py --info
python main.py --validate-config
```
