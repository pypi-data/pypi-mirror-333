from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_audio_to_video(video_path, audio_path, start_time):
    # Load the video and audio clips
    video = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)

    # Ensure the sound starts at the specified time
    sound = sound.with_start(start_time)

    # Prepare audio clips to combine
    audio_clips = []
    if video.audio is not None:
        audio_clips.append(video.audio)
    audio_clips.append(sound)

    # Create composite audio
    final_audio = CompositeAudioClip(audio_clips)

    # Set the video's audio to the combined audio
    video.audio = final_audio
    return video


def write_clip(video, output_path):
    # Write the output file
    video.write_videofile(
        output_path,
        codec='libx264',
        temp_audiofile='temp_audio.m4a',
        remove_temp=True,
        audio_codec="aac"
    )
    video.close()
