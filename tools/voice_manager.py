#!/usr/bin/env python3
"""
Voice profile management tool for the CloneIA project.
"""
import os
import sys
import json
import argparse
import logging
import shutil
from typing import Dict, List, Optional, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.utils import (
    load_voice_config, save_voice_config, get_available_profiles,
    CONFIG_DIR, DEFAULT_VOICE_SETTINGS
)

logger = logging.getLogger('cloneia.tools.voice_manager')

def list_profiles() -> List[Dict[str, str]]:
    """
    List all available voice profiles.
    
    Returns:
        List[Dict[str, str]]: List of profile information
    """
    profiles = get_available_profiles()
    
    if profiles:
        print("Available profiles:")
        for profile in profiles:
            print(f"- {profile['name']}: {profile['voice_name']} (ID: {profile['voice_id']})")
    else:
        print("No profiles found.")
    
    return profiles

def get_current_profile() -> Optional[Dict[str, Any]]:
    """
    Get the current voice profile.
    
    Returns:
        Optional[Dict[str, Any]]: Current profile information
    """
    config = load_voice_config()
    
    if config:
        print(f"Current profile: {config.get('voice_name')} (ID: {config.get('voice_id')})")
        print("Settings:")
        for key, value in config.get('settings', {}).items():
            print(f"  {key}: {value}")
    else:
        print("No current profile found.")
    
    return config

def switch_profile(profile_name: str) -> bool:
    """
    Switch to the specified voice profile.
    
    Args:
        profile_name: Name of the profile to switch to
        
    Returns:
        bool: True if successful, False otherwise
    """
    config_dir = CONFIG_DIR
    
    # Determine the profile file
    if profile_name.lower() == "default":
        # Check if there's a backup of the default profile
        backup_path = os.path.join(config_dir, "voice_config.json.bak")
        if os.path.exists(backup_path):
            profile_file = backup_path
        else:
            print("Default profile not found.")
            return False
    elif profile_name.lower() == "mix" or profile_name.lower() == "flukakumix":
        # Mixed profile
        profile_file = os.path.join(config_dir, "voice_config_mix.json")
    else:
        profile_file = os.path.join(config_dir, f"voice_config_{profile_name}.json")
    
    if not os.path.exists(profile_file):
        print(f"Profile {profile_name} not found.")
        return False
    
    # Backup the current profile
    current_config_path = os.path.join(config_dir, "voice_config.json")
    backup_path = os.path.join(config_dir, "voice_config.json.bak")
    
    if os.path.exists(current_config_path):
        shutil.copy2(current_config_path, backup_path)
        print(f"Backup of current profile created: {backup_path}")
    
    # Copy the new profile
    shutil.copy2(profile_file, current_config_path)
    
    # Verify the operation
    try:
        with open(current_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        print(f"Profile switched to: {config.get('voice_name')} (ID: {config.get('voice_id')})")
        return True
    except Exception as e:
        print(f"Error verifying new profile: {e}")
        return False

def create_profile(profile_name: str, voice_id: str, voice_name: Optional[str] = None) -> bool:
    """
    Create a new voice profile.
    
    Args:
        profile_name: Name of the profile to create
        voice_id: ID of the voice
        voice_name: Name of the voice (if None, uses profile_name)
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not voice_name:
        voice_name = profile_name
    
    # Create the configuration
    config = {
        "voice_id": voice_id,
        "voice_name": voice_name,
        "settings": DEFAULT_VOICE_SETTINGS
    }
    
    # Save the configuration
    if profile_name.lower() == "mix" or profile_name.lower() == "flukakumix":
        result = save_voice_config(config, "mix")
    else:
        result = save_voice_config(config, profile_name)
    
    if result:
        print(f"Profile {profile_name} created successfully.")
    else:
        print(f"Failed to create profile {profile_name}.")
    
    return result

def update_profile_settings(profile_name: Optional[str] = None, 
                           stability: Optional[float] = None,
                           similarity_boost: Optional[float] = None,
                           style: Optional[float] = None,
                           use_speaker_boost: Optional[bool] = None,
                           model_id: Optional[str] = None) -> bool:
    """
    Update settings for a voice profile.
    
    Args:
        profile_name: Name of the profile to update (if None, updates current profile)
        stability: Stability value (0.0-1.0)
        similarity_boost: Similarity boost value (0.0-1.0)
        style: Style value (0.0-1.0)
        use_speaker_boost: Whether to use speaker boost
        model_id: Model ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Load the profile
    config = load_voice_config(profile_name)
    
    if not config:
        print(f"Profile {profile_name or 'current'} not found.")
        return False
    
    # Update settings
    settings = config.get('settings', DEFAULT_VOICE_SETTINGS.copy())
    
    if stability is not None:
        settings['stability'] = max(0.0, min(1.0, stability))
    
    if similarity_boost is not None:
        settings['similarity_boost'] = max(0.0, min(1.0, similarity_boost))
    
    if style is not None:
        settings['style'] = max(0.0, min(1.0, style))
    
    if use_speaker_boost is not None:
        settings['use_speaker_boost'] = use_speaker_boost
    
    if model_id is not None:
        settings['model_id'] = model_id
    
    # Update the configuration
    config['settings'] = settings
    
    # Save the configuration
    result = save_voice_config(config, profile_name)
    
    if result:
        print(f"Profile {profile_name or 'current'} updated successfully.")
        print("New settings:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
    else:
        print(f"Failed to update profile {profile_name or 'current'}.")
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Voice profile management tool")
    parser.add_argument("--list", action="store_true", help="List available profiles")
    parser.add_argument("--current", action="store_true", help="Show current profile")
    parser.add_argument("--switch", help="Switch to the specified profile")
    parser.add_argument("--create", help="Create a new profile")
    parser.add_argument("--voice-id", help="Voice ID for creating a profile")
    parser.add_argument("--voice-name", help="Voice name for creating a profile")
    parser.add_argument("--update", help="Update settings for a profile (use 'current' for current profile)")
    parser.add_argument("--stability", type=float, help="Stability value (0.0-1.0)")
    parser.add_argument("--similarity-boost", type=float, help="Similarity boost value (0.0-1.0)")
    parser.add_argument("--style", type=float, help="Style value (0.0-1.0)")
    parser.add_argument("--speaker-boost", type=bool, help="Whether to use speaker boost")
    parser.add_argument("--model-id", help="Model ID")
    
    args = parser.parse_args()
    
    if args.list:
        list_profiles()
    
    elif args.current:
        get_current_profile()
    
    elif args.switch:
        switch_profile(args.switch)
    
    elif args.create:
        if not args.voice_id:
            print("Error: --voice-id is required when creating a profile.")
            return
        
        create_profile(args.create, args.voice_id, args.voice_name)
    
    elif args.update:
        profile_name = None if args.update.lower() == "current" else args.update
        update_profile_settings(
            profile_name,
            args.stability,
            args.similarity_boost,
            args.style,
            args.speaker_boost,
            args.model_id
        )
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
