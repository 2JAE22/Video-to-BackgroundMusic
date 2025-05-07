import subprocess
import torch
import time
import librosa
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm

torch.cuda.empty_cache()  # 사용하지 않는 메모리 해제

# 실행 시간 측정 시작
start_time = time.time()

# Step 1: 비디오 길이 가져오기
def get_video_duration(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"❌ Error getting video duration: {e}")
        return None

# VideoLLaMA3 Input Video Path
video_path = "/home/jaegun/projects/knu_project/VideoLLaMA3/assets/videos/running.mp4"
video_duration = get_video_duration(video_path)

if video_duration is None:
    print("❌ Failed to get video duration. Exiting...")
    exit(1)

print(f"\n🎥 Video Duration: {video_duration:.2f} seconds")

# Step 2: VideoLLaMA3 실행 (실시간 출력)
print("\n🚀 Running VideoLLaMA3 to generate music genre tags...")

start_videollama_time = time.time()
videollama_cmd = ["python", "/home/jaegun/projects/knu_project/VideoLLaMA3/inference/250310_example1.py"]

with subprocess.Popen(videollama_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
    for line in p.stdout:
        print(line, end="")  # 실시간 출력

end_videollama_time = time.time()
print("✅ VideoLLaMA3 Execution Time: {:.2f} seconds".format(end_videollama_time - start_videollama_time))

# VideoLLaMA3 출력값에서 genre 태그 가져오기
generated_tags = line.strip()  # 마지막 줄을 태그로 사용
print(f"\n🎵 Generated Genre Tags: {generated_tags}")

# Step 3: 비디오 길이에 맞춰 `max_new_tokens` 설정
tokens_per_second = 3000 / 58  # 58초당 3000 tokens 기준
max_new_tokens = int(video_duration * tokens_per_second)

print(f"\n🛠 Adjusted max_new_tokens for YuE: {max_new_tokens}")

# Step 4: YuE 실행 (실시간 출력)

# YuE 실행 경로
yue_inference_path = "/home/jaegun/projects/knu_project/YuE/inference"

print("\n🚀 Running YuE to generate background music...")

yue_cmd = [
    "python", "250310_infer_copy.py",
    "--genre", generated_tags,
    "--lyrics_txt", "/home/jaegun/projects/knu_project/YuE/prompt_egs/lyrics copy.txt",
    "--cuda_idx", "0",
    "--stage1_model", "m-a-p/YuE-s1-7B-anneal-en-cot",
    "--stage2_model", "m-a-p/YuE-s2-1B-general",
    "--run_n_segments", "2",
    "--stage2_batch_size", "4",
    "--output_dir", "/home/jaegun/projects/knu_project/main/output",
    "--max_new_tokens", str(max_new_tokens),  # 🎯 비디오 길이에 맞게 동적 조정
    "--repetition_penalty", "1.1"
]

start_yue_time = time.time()
with subprocess.Popen(yue_cmd, cwd=yue_inference_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
    for line in p.stdout:
        print(line, end="")  # 실시간 출력

end_yue_time = time.time()
print("✅ YuE Execution Time: {:.2f} seconds".format(end_yue_time - start_yue_time))

# 실행 시간 종료
end_time = time.time()
print("\n⏳ Total Execution Time: {:.2f} seconds".format(end_time - start_time))

print("\n🎬 Your video now has a background music file that matches its length!")


# Step 5: YuE가 생성한 음악 길이 확인
generated_audio_path = "/home/jaegun/projects/knu_project/main/output/YuE_generated.mp3"
output_video_path = "/home/jaegun/projects/knu_project/main/output/final_output.mp4"

print("\n🎬 비디오와 생성된 배경 음악을 병합하는 중...")

# 비디오와 오디오 로드
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(generated_audio_path)

# 비디오에 오디오 설정
# 원본 오디오는 제거되고 새 오디오로 대체됩니다
final_clip = video_clip.set_audio(audio_clip)

# 최종 비디오 저장
# 비디오 코덱을 'libx264'로 설정하여 호환성 확보
final_clip.write_videofile(
    output_video_path,
    fps=video_clip.fps,  # 원본 비디오의 fps 유지
)

# 리소스 해제
video_clip.close()
audio_clip.close()

print(f"✅ 최종 비디오 저장 위치: {output_video_path}")

# 실행 시간 종료
end_time = time.time()
print("\n⏳ Total Execution Time: {:.2f} seconds".format(end_time - start_time))
print("\n🎬 Your video now has a background music file that matches its length!")

