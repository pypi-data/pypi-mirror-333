import os
import subprocess
from pathlib import Path
from typing import List, Optional

from groq import Groq
from pydub import AudioSegment

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
DEFAULT_OVERLAP = 1000  # 1 second overlap in milliseconds

def check_file_size(file_path: str) -> int:
    """Return file size in bytes"""
    return os.path.getsize(file_path)

def calculate_chunk_size(audio_file: str, audio_segment: AudioSegment) -> int:
    """
    Calculate appropriate chunk size based on file size and audio duration
    """
    file_size = check_file_size(audio_file)
    if file_size <= MAX_FILE_SIZE:
        return len(audio_segment)  # Return full duration if file is small enough
        
    # Calculate bytes per millisecond
    bytes_per_ms = file_size / len(audio_segment)
    
    # Calculate maximum chunk duration that would result in ~24MB files (leaving buffer)
    max_chunk_size = int((MAX_FILE_SIZE * 0.95) / bytes_per_ms)
    
    return max_chunk_size

def preprocess_audio(input_file: str) -> Optional[str]:
    """
    Preprocess audio file to 16KHz mono FLAC format.
    
    Args:
        input_file (str): Path to input audio file
        
    Returns:
        str: Path to processed file, or None if processing fails
    """
    try:
        output_file = str(Path(input_file).with_suffix('.flac'))
        command = [
            'ffmpeg', '-i', input_file,
            '-ar', '16000',
            '-ac', '1',
            '-map', '0:a',
            '-c:a', 'flac',
            output_file
        ]
        
        subprocess.run(command, check=True, capture_output=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error preprocessing audio: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def chunk_audio(audio_file: str) -> List[str]:
    """
    Split audio file into overlapping chunks based on size constraints.
    """
    try:
        # Load audio file
        audio = AudioSegment.from_file(audio_file)
        
        # Calculate appropriate chunk size
        chunk_size = calculate_chunk_size(audio_file, audio)
        
        # If no chunking needed, return original file
        if chunk_size >= len(audio):
            return [audio_file]
            
        chunk_files = []
        duration = len(audio)
        chunk_start = 0
        
        # Create temp directory for chunks
        temp_dir = Path(audio_file).parent / "temp_chunks"
        temp_dir.mkdir(exist_ok=True)
        
        # Create chunks with overlap
        while chunk_start < duration:
            chunk_end = min(chunk_start + chunk_size, duration)
            chunk = audio[chunk_start:chunk_end]
            
            # Save chunk
            chunk_file = temp_dir / f"chunk_{chunk_start}_{chunk_end}.flac"
            chunk.export(chunk_file, format="flac")
            
            if check_file_size(str(chunk_file)) > MAX_FILE_SIZE:
                raise ValueError(f"Chunk file still exceeds {MAX_FILE_SIZE} bytes after processing")
                
            chunk_files.append(str(chunk_file))
            
            # Move start position (accounting for overlap)
            chunk_start = chunk_end - DEFAULT_OVERLAP
            
        return chunk_files
    except Exception as e:
        print(f"Error chunking audio: {e}")
        return []

def process_audio(
    audio_file: str,
    model: str = "whisper-large-v3",
    response_format: str = "text",
    language: str = None,
    prompt: str = None,
    temperature: float = 0.0
) -> str:
    """
    Process audio file using Whisper model.
    Automatically handles chunking for files larger than 25MB.
    
    Args:
        audio_file (str): Path to audio file
        model (str): Whisper model to use
        response_format (str): Format of the response
        language (str): Language of the audio
        prompt (str): Optional prompt for context
        temperature (float): Model temperature
        
    Returns:
        str: Transcription or translation result
    """
    file_size = check_file_size(audio_file)
    
    # If file is smaller than 25MB, process directly
    if file_size <= MAX_FILE_SIZE:
        client = Groq()
        with open(audio_file, "rb") as file:
            params = {
                "file": (audio_file, file.read()),
                "model": model,
                "response_format": response_format,
                "temperature": temperature
            }
            
            if language:
                params["language"] = language
            if prompt:
                params["prompt"] = prompt
                
            response = client.audio.transcriptions.create(**params)
            
            if response_format == "verbose_json":
                return _format_verbose_json(response)
            return response #.text
    
    # For larger files, use chunking
    return process_long_audio(
        audio_file=audio_file,
        model=model,
        response_format=response_format,
        language=language,
        prompt=prompt,
        temperature=temperature
    )

def process_long_audio(
    audio_file: str,
    model: str = "whisper-large-v3",
    response_format: str = "text",
    language: str = None,
    prompt: str = None,
    temperature: float = 0.0
) -> str:
    """Process long audio file by splitting into size-appropriate chunks."""
    try:
        # Split audio into chunks based on size
        chunk_files = chunk_audio(audio_file)
        if not chunk_files:
            raise ValueError("Failed to create audio chunks")
            
        # Process each chunk
        results = []
        for chunk_file in chunk_files:
            chunk_result = process_audio(
                audio_file=chunk_file,
                model=model,
                response_format=response_format,
                language=language,
                prompt=prompt,
                temperature=temperature
            )
            results.append(chunk_result)
            
        # Clean up chunk files if they were created
        if len(chunk_files) > 1:  # Only clean up if we actually created chunks
            temp_dir = Path(chunk_files[0]).parent
            for chunk_file in chunk_files:
                Path(chunk_file).unlink()
            temp_dir.rmdir()
            
        # Combine results based on format
        if response_format == "verbose_json":
            return _combine_verbose_json_results(results)
        return " ".join(results)
        
    except Exception as e:
        raise Exception(f"Error processing long audio: {e}")

def _combine_verbose_json_results(results: List[str]) -> str:
    """Combine verbose JSON results with adjusted timestamps."""
    combined = []
    time_offset = 0
    
    for result in results:
        segments = result.split("\n\n")
        for segment in segments:
            if not segment.strip():
                continue
            
            # Parse times from segment
            try:
                time_str = segment[segment.find("[")+1:segment.find("]")]
                start_time, end_time = map(float, time_str.split("->"))
                
                # Adjust timestamps with offset
                adjusted_start = start_time + time_offset
                adjusted_end = end_time + time_offset
                
                # Replace timestamps in segment
                adjusted_segment = segment.replace(
                    f"[{start_time:.2f}s -> {end_time:.2f}s]",
                    f"[{adjusted_start:.2f}s -> {adjusted_end:.2f}s]"
                )
                
                combined.append(adjusted_segment)
            except:
                # If parsing fails, add segment as-is
                combined.append(segment)
                
        # Update offset for next chunk
        if segments:
            try:
                last_time_str = segments[-1][segments[-1].find("[")+1:segments[-1].find("]")]
                _, last_end = map(float, last_time_str.split("->"))
                time_offset += last_end
            except:
                time_offset += 5  # Default to chunk size if parsing fails
                
    return "\n\n".join(combined)

def _format_verbose_json(response) -> str:
    """Format verbose JSON response for better readability."""
    result = []
    for segment in response.segments:
        result.append(
            f"[{segment.start:.2f}s -> {segment.end:.2f}s] "
            f"{segment.text}\n"
            f"Confidence: {segment.avg_logprob:.3f}, "
            f"No Speech Prob: {segment.no_speech_prob:.3f}"
        )
    return "\n\n".join(result)
