import subprocess
import torch
import time
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip

# input 비디오 파일 절대 경로
VIDEO_PATH = "/home/jaegun/projects/knu_project/VideoLLaMA3/assets/videos/dog.mp4"
# YuE output이 생성될 폴더와 mp3 이름 
GENERATED_AUDIO_PATH = "/home/jaegun/projects/knu_project/main/output/YuE_generated.mp3"
# 비디오와 음성이 통합될 최종 output 폴더와 mp4 이름 
OUTPUT_VIDEO_PATH = "/home/jaegun/projects/knu_project/main/output/dog_final_output.mp4"

# 명령어 실행 절대 경로
VIDEOLLAMA_CMD = ["python", "/home/jaegun/projects/knu_project/VideoLLaMA3/inference/250310_example1.py"]
YUE_INFERENCE_PATH = "/home/jaegun/projects/knu_project/YuE/inference"
                                    

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

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, fps=video_clip.fps)  # FPS 유지

    video_clip.close()
    audio_clip.close()

    print(f"✅ 최종 비디오 저장 위치: {output_path}")


if __name__ == "__main__":
    start_time = time.time()  # 전체 실행 시간 측정 시작

    # 🔹 1. 비디오 길이 가져오기
    video_duration = get_video_duration(VIDEO_PATH)
    if video_duration is None:
        print("❌ Failed to get video duration. Exiting...")
        exit(1)

    print(f"\n🎥 Video Duration: {video_duration:.2f} seconds")

    # 🔹 2. VideoLLaMA3 실행
    print("\n🚀 Running VideoLLaMA3 to generate music genre tags...")
    line = run_command(VIDEOLLAMA_CMD)

    # VideoLLaMA3 출력값에서 genre 태그 가져오기
    generated_tags = line.strip()
    print(f"\n🎵 Generated Genre Tags: {generated_tags}")

    # 🔹 3. YuE 실행하여 배경 음악 생성
    print("\n🚀 Running YuE to generate background music...")

    yue_cmd = [
        "python", "250310_infer_copy.py",
        "--genre", generated_tags,
        "--lyrics_txt", "/home/jaegun/projects/knu_project/YuE/prompt_egs/lyrics copy.txt",
        "--cuda_idx", "0",
        "--stage1_model", "m-a-p/YuE-s1-7B-anneal-en-cot",
        "--stage2_model", "m-a-p/YuE-s2-1B-general",
        "--run_n_segments", "1",
        "--stage2_batch_size", "4",
        "--output_dir", "/home/jaegun/projects/knu_project/main/output",
        "--max_new_tokens", str(int(video_duration * (3000 / 50))),  # 🎯 비디오 길이에 맞게 동적 조정
        "--repetition_penalty", "1.1"
    ]

    run_command(yue_cmd, cwd=YUE_INFERENCE_PATH)

    # 🔹 4. 비디오 + 오디오 병합
    merge_video_audio(VIDEO_PATH, GENERATED_AUDIO_PATH, OUTPUT_VIDEO_PATH)

    print("\n🎬 Your video now has a background music file that matches its length!")
