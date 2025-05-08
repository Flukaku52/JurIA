#!/usr/bin/env python3
"""
Audio sample extraction tool for the CloneIA project.
"""
import os
import sys
import json
import argparse
import logging
from typing import Dict, List, Optional, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.utils import (
    ensure_directory, PROJECT_ROOT
)
from core.audio import AudioGenerator

logger = logging.getLogger('cloneia.tools.sample_extractor')

class SampleExtractor:
    """
    Class for extracting audio samples from videos.
    """
    
    def __init__(self):
        """
        Initialize the sample extractor.
        """
        # Directories
        self.reference_dir = os.path.join(PROJECT_ROOT, "reference")
        self.videos_dir = os.path.join(self.reference_dir, "videos")
        self.samples_dir = os.path.join(self.reference_dir, "samples")
        self.short_samples_dir = os.path.join(self.samples_dir, "short_samples")
        
        # Ensure directories exist
        for directory in [self.reference_dir, self.videos_dir, self.samples_dir, self.short_samples_dir]:
            ensure_directory(directory)
        
        # Audio generator
        self.audio_generator = AudioGenerator()
        
        logger.info("SampleExtractor initialized")
    
    def extract_from_videos(self, video_dir: Optional[str] = None, 
                           output_dir: Optional[str] = None,
                           max_samples: int = 5, 
                           max_duration: int = 30) -> List[str]:
        """
        Extract audio samples from videos.
        
        Args:
            video_dir: Directory containing videos (if None, uses default)
            output_dir: Directory to save audio samples (if None, uses default)
            max_samples: Maximum number of samples to extract
            max_duration: Maximum duration of each sample in seconds
            
        Returns:
            List[str]: List of paths to extracted audio files
        """
        if not video_dir:
            video_dir = self.videos_dir
        
        if not output_dir:
            output_dir = os.path.join(self.reference_dir, "voice_samples")
        
        # Check if the video directory exists
        if not os.path.exists(video_dir):
            print(f"Error: Video directory not found: {video_dir}")
            return []
        
        # Extract audio samples
        samples = self.audio_generator.extract_audio_samples(
            video_dir, output_dir, max_samples, max_duration
        )
        
        # Display results
        if samples:
            print(f"Extracted {len(samples)} audio samples:")
            for i, sample in enumerate(samples):
                print(f"{i+1}. {sample}")
        else:
            print("No audio samples extracted.")
        
        return samples
    
    def extract_short_samples(self, source_dir: Optional[str] = None,
                             output_dir: Optional[str] = None,
                             min_duration: float = 7.0,
                             max_duration: float = 12.0,
                             num_samples: int = 40) -> List[str]:
        """
        Extract short audio samples from longer audio files.
        
        Args:
            source_dir: Directory containing source audio files (if None, uses default)
            output_dir: Directory to save short samples (if None, uses default)
            min_duration: Minimum duration of each sample in seconds
            max_duration: Maximum duration of each sample in seconds
            num_samples: Number of samples to extract
            
        Returns:
            List[str]: List of paths to extracted audio files
        """
        if not source_dir:
            source_dir = os.path.join(self.reference_dir, "voice_samples")
        
        if not output_dir:
            output_dir = self.short_samples_dir
        
        # Check if the source directory exists
        if not os.path.exists(source_dir):
            print(f"Error: Source directory not found: {source_dir}")
            return []
        
        # Extract short samples
        samples = self.audio_generator.extract_short_samples(
            source_dir, output_dir, min_duration, max_duration, num_samples
        )
        
        # Display results
        if samples:
            print(f"Extracted {len(samples)} short audio samples:")
            for i, sample in enumerate(samples):
                print(f"{i+1}. {sample}")
        else:
            print("No short audio samples extracted.")
        
        return samples
    
    def analyze_samples(self, samples_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze audio samples.
        
        Args:
            samples_dir: Directory containing audio samples (if None, uses default)
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        if not samples_dir:
            samples_dir = self.short_samples_dir
        
        # Check if the samples directory exists
        if not os.path.exists(samples_dir):
            print(f"Error: Samples directory not found: {samples_dir}")
            return {}
        
        try:
            import moviepy.editor as mp
        except ImportError:
            print("Error: moviepy library not found. Install moviepy.")
            return {}
        
        # Analyze samples
        samples = []
        total_duration = 0
        min_duration = float('inf')
        max_duration = 0
        
        for filename in os.listdir(samples_dir):
            if filename.lower().endswith(('.mp3', '.wav', '.m4a')):
                try:
                    file_path = os.path.join(samples_dir, filename)
                    audio = mp.AudioFileClip(file_path)
                    duration = audio.duration
                    
                    samples.append({
                        "file": filename,
                        "path": file_path,
                        "duration": duration
                    })
                    
                    total_duration += duration
                    min_duration = min(min_duration, duration)
                    max_duration = max(max_duration, duration)
                    
                    audio.close()
                except Exception as e:
                    print(f"Error analyzing {filename}: {e}")
        
        # Calculate statistics
        avg_duration = total_duration / len(samples) if samples else 0
        
        # Create analysis report
        analysis = {
            "total_samples": len(samples),
            "total_duration": total_duration,
            "min_duration": min_duration if samples else 0,
            "max_duration": max_duration if samples else 0,
            "avg_duration": avg_duration,
            "samples": samples
        }
        
        # Save analysis report
        report_path = os.path.join(samples_dir, "analysis_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        # Display results
        print("\n=== Sample Analysis ===")
        print(f"Total samples: {len(samples)}")
        print(f"Total duration: {total_duration:.2f} seconds")
        print(f"Minimum duration: {min_duration:.2f} seconds")
        print(f"Maximum duration: {max_duration:.2f} seconds")
        print(f"Average duration: {avg_duration:.2f} seconds")
        print(f"Analysis report saved to: {report_path}")
        
        return analysis

def main():
    parser = argparse.ArgumentParser(description="Audio sample extraction tool for CloneIA")
    parser.add_argument("--extract", action="store_true", help="Extract audio samples from videos")
    parser.add_argument("--extract-short", action="store_true", help="Extract short audio samples")
    parser.add_argument("--analyze", action="store_true", help="Analyze audio samples")
    parser.add_argument("--video-dir", help="Directory containing videos")
    parser.add_argument("--output-dir", help="Directory to save audio samples")
    parser.add_argument("--source-dir", help="Directory containing source audio files")
    parser.add_argument("--samples-dir", help="Directory containing audio samples")
    parser.add_argument("--max-samples", type=int, default=5, help="Maximum number of samples to extract")
    parser.add_argument("--max-duration", type=int, default=30, help="Maximum duration of each sample in seconds")
    parser.add_argument("--min-duration", type=float, default=7.0, help="Minimum duration of each short sample in seconds")
    parser.add_argument("--short-duration", type=float, default=12.0, help="Maximum duration of each short sample in seconds")
    parser.add_argument("--num-samples", type=int, default=40, help="Number of short samples to extract")
    
    args = parser.parse_args()
    
    # Create the extractor
    extractor = SampleExtractor()
    
    # Run the requested operation
    if args.extract:
        extractor.extract_from_videos(
            args.video_dir,
            args.output_dir,
            args.max_samples,
            args.max_duration
        )
    
    elif args.extract_short:
        extractor.extract_short_samples(
            args.source_dir,
            args.output_dir,
            args.min_duration,
            args.short_duration,
            args.num_samples
        )
    
    elif args.analyze:
        extractor.analyze_samples(args.samples_dir)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
