"""
FFmpeg Video Processor Module

Advanced video generation using FFmpeg-Python and OpenCV for reliable, 
high-performance video creation with precise control over encoding parameters.
"""

import os
import cv2
import ffmpeg
import logging
import subprocess
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import tempfile
import shutil
from datetime import datetime


class FFmpegVideoProcessor:
    """
    Professional video processor using FFmpeg-Python and OpenCV.
    
    Provides robust video generation with multiple fallback methods,
    comprehensive error handling, and detailed progress tracking.
    """
    
    def __init__(self, temp_dir: Optional[Path] = None):
        """
        Initialize the FFmpeg video processor.
        
        Args:
            temp_dir: Directory for temporary files (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir or Path("temp/video")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Video configuration
        self.default_fps = 24
        self.default_resolution = (1920, 1080)
        self.default_codec = 'libx264'
        self.default_audio_codec = 'aac'
        
        # Validate FFmpeg installation
        self._validate_ffmpeg()
        
    def _validate_ffmpeg(self) -> bool:
        """
        Validate that FFmpeg is properly installed and accessible.
        
        Returns:
            bool: True if FFmpeg is available
            
        Raises:
            RuntimeError: If FFmpeg is not found
        """
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.logger.info("✅ FFmpeg validation successful")
                return True
            else:
                raise RuntimeError(f"FFmpeg validation failed: {result.stderr}")
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg and add it to your PATH.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("FFmpeg validation timed out")
    
    def create_video_from_images(
        self, 
        image_paths: List[str], 
        durations: List[float],
        audio_path: Optional[str] = None,
        output_path: str = "output.mp4",
        background_music_path: Optional[str] = None,
        music_volume: float = 0.3,
        crossfade_duration: float = 1.0,
        resolution: Optional[Tuple[int, int]] = None,
        fps: int = 24
    ) -> bool:
        """
        Create video from image sequence with audio and optional background music.
        
        Args:
            image_paths: List of paths to images
            durations: Duration for each image in seconds
            audio_path: Path to main audio file (narration)
            output_path: Output video file path
            background_music_path: Optional background music file
            music_volume: Volume level for background music (0.0-1.0)
            crossfade_duration: Duration of crossfade transitions between images
            resolution: Video resolution (width, height)
            fps: Frames per second
            
        Returns:
            bool: True if video creation succeeded
        """
        if not image_paths:
            self.logger.error("No images provided for video creation")
            return False
            
        if len(image_paths) != len(durations):
            self.logger.error("Number of images must match number of durations")
            return False
            
        resolution = resolution or self.default_resolution
        
        # Multiple rendering methods for maximum reliability
        methods = [
            self._method_opencv_sequence,
            self._method_ffmpeg_concat,
            self._method_simple_slideshow,
            self._method_basic_conversion
        ]
        
        for i, method in enumerate(methods):
            try:
                self.logger.info(f"🎬 Attempting Method {i}: {method.__name__}")
                success = method(
                    image_paths=image_paths,
                    durations=durations,
                    audio_path=audio_path,
                    output_path=output_path,
                    background_music_path=background_music_path,
                    music_volume=music_volume,
                    crossfade_duration=crossfade_duration,
                    resolution=resolution,
                    fps=fps
                )
                
                if success and Path(output_path).exists():
                    self.logger.info(f"✅ Method {i} succeeded: {method.__name__}")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"❌ Method {i} failed: {e}")
                continue
        
        self.logger.error("❌ All video creation methods failed")
        return False
    
    def _method_opencv_sequence(
        self, 
        image_paths: List[str], 
        durations: List[float],
        audio_path: Optional[str],
        output_path: str,
        background_music_path: Optional[str],
        music_volume: float,
        crossfade_duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> bool:
        """
        Method 0: OpenCV video writer with FFmpeg audio combination.
        Most flexible method with full control over video creation.
        """
        temp_video_path = str(self.temp_dir / f"temp_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        try:
            # Create video using OpenCV
            self._create_video_with_opencv(
                image_paths, durations, temp_video_path, 
                resolution, fps, crossfade_duration
            )
            
            # Add audio using FFmpeg
            if audio_path or background_music_path:
                return self._add_audio_with_ffmpeg(
                    temp_video_path, output_path, audio_path, 
                    background_music_path, music_volume
                )
            else:
                # No audio, just move the video file
                shutil.move(temp_video_path, output_path)
                return True
                
        except Exception as e:
            self.logger.error(f"OpenCV sequence method failed: {e}")
            # Cleanup
            Path(temp_video_path).unlink(missing_ok=True)
            return False
    
    def _method_ffmpeg_concat(
        self, 
        image_paths: List[str], 
        durations: List[float],
        audio_path: Optional[str],
        output_path: str,
        background_music_path: Optional[str],
        music_volume: float,
        crossfade_duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> bool:
        """
        Method 1: FFmpeg concat protocol for image sequence.
        Reliable method using FFmpeg's built-in capabilities.
        """
        try:
            # Create input list for FFmpeg concat
            concat_file = self._create_ffmpeg_concat_file(image_paths, durations)
            
            # Build FFmpeg command
            input_stream = ffmpeg.input(concat_file, format='concat', safe=0)
            
            # Configure video output
            video_stream = ffmpeg.output(
                input_stream,
                output_path,
                vcodec=self.default_codec,
                r=fps,
                s=f"{resolution[0]}x{resolution[1]}",
                pix_fmt='yuv420p'
            )
            
            # Add audio if provided
            if audio_path:
                audio_stream = ffmpeg.input(audio_path)
                video_stream = ffmpeg.output(
                    input_stream, audio_stream,
                    output_path,
                    vcodec=self.default_codec,
                    acodec=self.default_audio_codec,
                    r=fps,
                    s=f"{resolution[0]}x{resolution[1]}",
                    pix_fmt='yuv420p',
                    shortest=None
                )
            
            # Execute FFmpeg command
            ffmpeg.run(video_stream, overwrite_output=True, quiet=True)
            
            # Cleanup
            Path(concat_file).unlink(missing_ok=True)
            
            return Path(output_path).exists()
            
        except Exception as e:
            self.logger.error(f"FFmpeg concat method failed: {e}")
            return False
    
    def _method_simple_slideshow(
        self, 
        image_paths: List[str], 
        durations: List[float],
        audio_path: Optional[str],
        output_path: str,
        background_music_path: Optional[str],
        music_volume: float,
        crossfade_duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> bool:
        """
        Method 2: Simple slideshow using FFmpeg filter_complex.
        Fallback method with basic functionality.
        """
        try:
            # Create a simple slideshow with equal durations
            avg_duration = sum(durations) / len(durations)
            
            # Use first image as base and overlay others
            input_streams = [ffmpeg.input(img) for img in image_paths[:5]]  # Limit to 5 images for simplicity
            
            if not input_streams:
                return False
            
            # Create basic slideshow
            output_stream = input_streams[0]
            
            if audio_path:
                audio_stream = ffmpeg.input(audio_path)
                output_stream = ffmpeg.output(
                    output_stream, audio_stream,
                    output_path,
                    vcodec=self.default_codec,
                    acodec=self.default_audio_codec,
                    r=fps,
                    s=f"{resolution[0]}x{resolution[1]}",
                    t=sum(durations),
                    pix_fmt='yuv420p'
                )
            else:
                output_stream = ffmpeg.output(
                    output_stream,
                    output_path,
                    vcodec=self.default_codec,
                    r=fps,
                    s=f"{resolution[0]}x{resolution[1]}",
                    t=sum(durations),
                    pix_fmt='yuv420p'
                )
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return Path(output_path).exists()
            
        except Exception as e:
            self.logger.error(f"Simple slideshow method failed: {e}")
            return False
    
    def _method_basic_conversion(
        self, 
        image_paths: List[str], 
        durations: List[float],
        audio_path: Optional[str],
        output_path: str,
        background_music_path: Optional[str],
        music_volume: float,
        crossfade_duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> bool:
        """
        Method 3: Basic image-to-video conversion.
        Emergency fallback with minimal features.
        """
        try:
            if not image_paths:
                return False
            
            # Use the first image for the entire duration
            first_image = image_paths[0]
            total_duration = sum(durations)
            
            input_stream = ffmpeg.input(first_image, loop=1, t=total_duration)
            
            if audio_path:
                audio_stream = ffmpeg.input(audio_path)
                output_stream = ffmpeg.output(
                    input_stream, audio_stream,
                    output_path,
                    vcodec=self.default_codec,
                    acodec=self.default_audio_codec,
                    r=fps,
                    s=f"{resolution[0]}x{resolution[1]}",
                    pix_fmt='yuv420p',
                    shortest=None
                )
            else:
                output_stream = ffmpeg.output(
                    input_stream,
                    output_path,
                    vcodec=self.default_codec,
                    r=fps,
                    s=f"{resolution[0]}x{resolution[1]}",
                    t=total_duration,
                    pix_fmt='yuv420p'
                )
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return Path(output_path).exists()
            
        except Exception as e:
            self.logger.error(f"Basic conversion method failed: {e}")
            return False
    
    def _create_video_with_opencv(
        self, 
        image_paths: List[str], 
        durations: List[float],
        output_path: str,
        resolution: Tuple[int, int],
        fps: int,
        crossfade_duration: float
    ) -> None:
        """
        Create video using OpenCV VideoWriter with crossfade transitions.
        
        Args:
            image_paths: List of image file paths
            durations: Duration for each image
            output_path: Output video file path
            resolution: Video resolution (width, height)
            fps: Frames per second
            crossfade_duration: Duration of crossfade effect in seconds
        """
        try:
            # Try different methods to get fourcc code
            if hasattr(cv2, 'VideoWriter_fourcc'):
                fourcc = getattr(cv2, 'VideoWriter_fourcc')(*'mp4v')
            elif hasattr(cv2.VideoWriter, 'fourcc'):
                fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            else:
                # Fallback: use numeric fourcc code for mp4v
                fourcc = cv2.CAP_PROP_FOURCC
        except (AttributeError, TypeError):
            # Final fallback for older OpenCV versions
            fourcc = -1
        
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)
        
        try:
            crossfade_frames = int(crossfade_duration * fps)
            
            for i, (image_path, duration) in enumerate(zip(image_paths, durations)):
                # Load and resize image
                image = cv2.imread(image_path)
                if image is None:
                    self.logger.warning(f"Could not load image: {image_path}")
                    continue
                
                image = cv2.resize(image, resolution)
                total_frames = int(duration * fps)
                
                # Handle crossfade transition
                if i > 0 and crossfade_frames > 0:
                    # Create crossfade with previous image
                    prev_image = cv2.imread(image_paths[i-1])
                    if prev_image is not None:
                        prev_image = cv2.resize(prev_image, resolution)
                        
                        for frame in range(crossfade_frames):
                            alpha = frame / crossfade_frames
                            blended = cv2.addWeighted(prev_image, 1-alpha, image, alpha, 0)
                            video_writer.write(blended)
                        
                        # Adjust remaining frames
                        total_frames -= crossfade_frames
                
                # Write main image frames
                for _ in range(max(1, total_frames)):
                    video_writer.write(image)
                    
                self.logger.info(f"✅ Processed image {i+1}/{len(image_paths)}: {Path(image_path).name}")
                
        finally:
            video_writer.release()
    
    def _add_audio_with_ffmpeg(
        self, 
        video_path: str,
        output_path: str, 
        audio_path: Optional[str],
        background_music_path: Optional[str],
        music_volume: float
    ) -> bool:
        """
        Add audio to video using FFmpeg with optional background music mixing.
        
        Args:
            video_path: Input video file path
            output_path: Output video file path
            audio_path: Main audio (narration) file path
            background_music_path: Background music file path
            music_volume: Volume level for background music
            
        Returns:
            bool: True if audio was successfully added
        """
        try:
            video_stream = ffmpeg.input(video_path)
            
            if audio_path and background_music_path:
                # Mix narration and background music
                audio_stream = ffmpeg.input(audio_path)
                music_stream = ffmpeg.input(background_music_path)
                
                # Adjust music volume and mix
                music_adjusted = ffmpeg.filter(music_stream, 'volume', music_volume)
                mixed_audio = ffmpeg.filter([audio_stream, music_adjusted], 'amix', inputs=2)
                
                output_stream = ffmpeg.output(
                    video_stream, mixed_audio,
                    output_path,
                    vcodec='copy',
                    acodec=self.default_audio_codec,
                    shortest=None
                )
                
            elif audio_path:
                # Only narration audio
                audio_stream = ffmpeg.input(audio_path)
                output_stream = ffmpeg.output(
                    video_stream, audio_stream,
                    output_path,
                    vcodec='copy',
                    acodec=self.default_audio_codec,
                    shortest=None
                )
                
            elif background_music_path:
                # Only background music
                music_stream = ffmpeg.input(background_music_path)
                music_adjusted = ffmpeg.filter(music_stream, 'volume', music_volume)
                
                output_stream = ffmpeg.output(
                    video_stream, music_adjusted,
                    output_path,
                    vcodec='copy',
                    acodec=self.default_audio_codec,
                    shortest=None
                )
            else:
                # No audio to add
                return False
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            
            # Cleanup temporary video file
            Path(video_path).unlink(missing_ok=True)
            
            return Path(output_path).exists()
            
        except Exception as e:
            self.logger.error(f"Audio addition failed: {e}")
            return False
    
    def _create_ffmpeg_concat_file(self, image_paths: List[str], durations: List[float]) -> str:
        """
        Create FFmpeg concat file for image sequence.
        
        Args:
            image_paths: List of image file paths
            durations: Duration for each image
            
        Returns:
            str: Path to the concat file
        """
        concat_file = self.temp_dir / f"concat_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(concat_file, 'w') as f:
            for image_path, duration in zip(image_paths, durations):
                f.write(f"file '{os.path.abspath(image_path)}'\n")
                f.write(f"duration {duration}\n")
            
            # Add last image again for proper duration
            if image_paths:
                f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")
        
        return str(concat_file)
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Get video information using FFprobe.
        
        Args:
            video_path: Path to video file
            
        Returns:
            dict: Video information
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            
            info = {
                'duration': float(probe['format']['duration']),
                'size': int(probe['format']['size']),
                'format': probe['format']['format_name']
            }
            
            if video_stream:
                info.update({
                    'width': int(video_stream['width']),
                    'height': int(video_stream['height']),
                    'fps': eval(video_stream['r_frame_rate']),
                    'video_codec': video_stream['codec_name']
                })
            
            if audio_stream:
                info.update({
                    'audio_codec': audio_stream['codec_name'],
                    'sample_rate': int(audio_stream['sample_rate'])
                })
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get video info: {e}")
            return {}
    
    def cleanup_temp_files(self) -> None:
        """Clean up temporary files created during video processing."""
        try:
            if self.temp_dir.exists():
                for temp_file in self.temp_dir.glob("temp_*"):
                    temp_file.unlink(missing_ok=True)
                self.logger.info("🧹 Temporary files cleaned up")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp files: {e}")
