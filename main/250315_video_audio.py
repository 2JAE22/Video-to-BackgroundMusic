from moviepy.editor import VideoFileClip, AudioFileClip

# 파일 경로 설정
video_path = "/home/jaegun/projects/knu_project/VideoLLaMA3/assets/videos/crying.mp4"
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