# CreepyPasta AI - Quick Start Guide

## Getting Your Reddit API Credentials

1. **Go to Reddit Apps**: https://www.reddit.com/prefs/apps
2. **Click "Create App" or "Create Another App"**
3. **Fill in the form**:
   - **Name**: `CreepyPasta AI`
   - **App type**: Select `script`
   - **Description**: `AI app for reading creepypasta stories`
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8080`
4. **Click "Create app"**
5. **Copy your credentials**:
   - **Client ID**: The string under your app name (looks like: `abcdef123456`)
   - **Client Secret**: The "secret" field

## Setting Up Your Environment

1. **Copy the environment template**:
   ```bash
   copy .env.example .env
   ```

2. **Edit the .env file** with your credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=CreepyPastaAI/1.0 by YourRedditUsername
   ```

## First Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the logs directory**:
   ```bash
   mkdir logs
   ```

3. **Run the application**:
   ```bash
   python main.py 5
   ```
   This will process 5 stories from Reddit.

## Expected Output

The application will:
1. Connect to Reddit and fetch stories
2. Process and clean the text
3. Generate speech audio files
4. Mix with background music (if available)
5. Save final audio files to `assets/output/`

## Troubleshooting

### Reddit API Issues
- Make sure your credentials are correct
- Check that your Reddit account is in good standing
- Verify the user agent string includes your Reddit username

### Audio Issues
- Ensure you have sufficient disk space
- Check that the output directory is writable
- For background music, add MP3/WAV files to `assets/music/`

### Dependencies
If you encounter import errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Adding Background Music

1. **Download scary/atmospheric music** (royalty-free)
2. **Save files to `assets/music/`**
3. **Supported formats**: MP3, WAV
4. **Recommended**: 
   - Dark ambient music
   - Horror soundscapes
   - Instrumental pieces
   - 3-10 minute tracks work best

## Next Steps

- **Experiment with different TTS providers** (OpenAI, Azure)
- **Customize the configuration** in `config/settings.yaml`
- **Add your own background music collection**
- **Adjust story filtering criteria**
- **Explore the generated audio files**

Happy horror story listening! 👻🎧
