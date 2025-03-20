import pytest
import vidtoolz_add_sound as w
from moviepy import VideoFileClip, AudioFileClip
import os

# Import the function to be tested
from vidtoolz_add_sound.add_sound import add_audio_to_video, write_clip
from argparse import ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(['test_video.mp4', 'audio.mp3', "-s", "5"])
    assert result.video == "test_video.mp4"
    assert result.audio == "audio.mp3"
    assert result.start_time == 5
    


def test_plugin(capsys):
    w.addsound_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


# Define paths for test files
HERE = os.path.dirname(__file__)
TEST_OUTPUT_PATH = os.path.join(HERE, "output_test_video.mp4")

@pytest.fixture(scope="module")
def test_files():
    TEST_VIDEO_PATH = os.path.join(HERE, "test_video.mp4")
    TEST_AUDIO_PATH = os.path.join(HERE, "test_audio.mp3")
    return TEST_VIDEO_PATH, TEST_AUDIO_PATH

# Clean up test files
def cleanup_test_files():
    for file in [TEST_OUTPUT_PATH]:
        if os.path.exists(file):
            os.remove(file)

def test_add_audio_to_video(test_files):
    # Define the start time for the audio
    TEST_VIDEO_PATH, TEST_AUDIO_PATH = test_files
    start_time = 1

    # Call the function to be tested
    clip=add_audio_to_video(TEST_VIDEO_PATH, TEST_AUDIO_PATH, start_time)
    write_clip(clip, TEST_OUTPUT_PATH)
    # Verify the output file exists
    assert os.path.exists(TEST_OUTPUT_PATH)

    # Load the output video to verify the audio
    output_video = VideoFileClip(TEST_OUTPUT_PATH)
    assert output_video.audio is not None

    # Check the audio start time
    audio_start_time = output_video.audio.start
    assert audio_start_time == 0, f"Expected audio start time {start_time}, but got {audio_start_time}"

    # Clean up the output video
    output_video.close()
    cleanup_test_files()