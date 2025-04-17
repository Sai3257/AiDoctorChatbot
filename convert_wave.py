from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    """
    Converts an MP3 file to a WAV file.

    Args:
    mp3_path (str): Path to the input MP3 file.
    wav_path (str): Path to save the output WAV file.
    """
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_path)

        # Export as WAV
        audio.export(wav_path, format="wav")
        print(f"Conversion successful! WAV file saved to: {wav_path}")

    except Exception as e:
        print(f"Error during conversion: {e}")


# Example usage:
mp3_file_path = "path_to_input.mp3"  # Replace with the path to your MP3 file
wav_file_path = "path_to_output.wav"  # Replace with the desired output WAV path

# Call the function to convert MP3 to WAV
convert_mp3_to_wav(mp3_file_path, wav_file_path)
