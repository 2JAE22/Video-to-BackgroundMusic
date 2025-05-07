import subprocess
import torch
import time
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip
from omegaconf import OmegaConf

# input 비디오 파일 절대 경로 
VIDEO_PATH = "/home/jaegun/projects/knu_project/VideoLLaMA3/assets/videos/cow.mp4"
# Audio generation output이 생성될 폴더와 mp3 이름 
GENERATED_AUDIO_PATH = "/home/jaegun/projects/knu_project/main/output/YuE_generated.mp3"
# 비디오와 음성이 통합될 최종 output 폴더와 mp4 이름 
OUTPUT_VIDEO_PATH = "/home/jaegun/projects/knu_project/main/output/cow_final_output.mp4"

# config 파일 경로
CONFIG_PATH = "/home/jaegun/projects/knu_project/VideoLLaMA3/config/250309_config.yaml"

# 명령어 실행 절대 경로
vidio_generation_path = ["python", "/home/jaegun/projects/knu_project/VideoLLaMA3/inference/250310_example1.py"]
audio_generation_path = "/home/jaegun/projects/knu_project/YuE/inference"

def update_config_video_path(config_path, video_path):
    """config.yaml 파일의 video.path 값을 업데이트하는 함수"""
    config = OmegaConf.load(config_path)
    config.video.path = video_path
    OmegaConf.save(config, config_path)
    print(f"✅ Config updated with video path: {video_path}")

def get_video_duration(video_path):
    """ 비디오 길이를 가져오는 함수 """
    try:
        probe = ffmpeg.probe(video_path)
        return float(probe['format']['duration'])
    except Exception as e:
        print(f"❌ Error getting video duration: {e}")
        return None


def run_command(command, cwd=None):
    """ 서브 프로세스를 실행하고, 실시간 출력을 화면에 표시하는 함수 """
    with subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
        for line in p.stdout:
            print(line, end="")  # 실시간 출력
        return line


def merge_video_audio(video_path, audio_path, output_path):
    """ MoviePy를 사용하여 비디오와 오디오를 병합하는 함수 """
    print("\n🎬 비디오와 생성된 배경 음악을 병합하는 중...")

    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # 오디오를 비디오 길이에 맞게 자르기
    audio_clip = audio_clip.subclip(0, video_clip.duration)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, fps=video_clip.fps)  # 비디오 FPS 유지

    video_clip.close()
    audio_clip.close()

    print(f"✅ 최종 비디오 저장 위치: {output_path}")


if __name__ == "__main__":
    start_time = time.time()  # 전체 실행 시간 측정 시작

    # 🔹 0. config.yaml 파일의 video.path 업데이트
    update_config_video_path(CONFIG_PATH, VIDEO_PATH)

    # 🔹 1. 비디오 길이 가져오기
    video_duration = get_video_duration(VIDEO_PATH)
    if video_duration is None:
        print("❌ Failed to get video duration. Exiting...")
        exit(1)

    print(f"\n🎥 Video Duration: {video_duration:.2f} seconds")

    # 🔹 2. Video Generation 실행
    print("\n🚀 Running Vidio generation to generate music genre tags...")
    line = run_command(vidio_generation_path)

    # Video Generation 출력값에서 genre 태그 가져오기
    generated_tags = line.strip()
    print(f"\n🎵 Generated Genre Tags: {generated_tags}")

    # 🔹 3. Audio Generation 실행하여 배경 음악 생성
    print("\n🚀 Running audio generation to generate background music...")

    audio_generation_cmd = [
        "python", "250310_infer_copy.py",
        "--genre", generated_tags,
        "--lyrics_txt", "/home/jaegun/projects/knu_project/YuE/prompt_egs/lyrics copy.txt",
        "--cuda_idx", "0",
        "--stage1_model", "m-a-p/YuE-s1-7B-anneal-en-cot",
        "--stage2_model", "m-a-p/YuE-s2-1B-general",
        "--run_n_segments", "1",
        "--stage2_batch_size", "4",
        "--output_dir", "/home/jaegun/projects/knu_project/main/output",
        "--max_new_tokens", str(3000),  
        "--repetition_penalty", "1.1"
    ]

    run_command(audio_generation_cmd, cwd=audio_generation_path)

    # 🔹 4. 비디오 + 오디오 병합
    merge_video_audio(VIDEO_PATH, GENERATED_AUDIO_PATH, OUTPUT_VIDEO_PATH)

    print("\n🎬 Your video now has a background music file that matches its length!")