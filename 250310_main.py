import subprocess

import torch
torch.cuda.empty_cache()  # 사용하지 않는 메모리 해제


# Step 1: VideoLLaMA3 실행
print("\n🚀 Running VideoLLaMA3 to generate music genre tags...")
result = subprocess.run(
    ["python", "/home/jaegun/projects/knu_project/VideoLLaMA3/inference/250310_example1.py"], 
    capture_output=True, text=True
)
print("result: ", result)
# VideoLLaMA3 출력값에서 genre 태그 가져오기
generated_tags = result.stdout.strip().split("\n")[-1]
print(f"\ngenerated_tags:{generated_tags}")



# Step 2: YuE 실행 (VideoLLaMA3 결과를 전달)

# YuE 실행 경로
yue_inference_path = "/home/jaegun/projects/knu_project/YuE/inference"

print("\n🚀 Running YuE to generate background music...")
yue_cmd = [
    "python", "250310_infer_copy.py",
    "--genre", generated_tags,
    "--lyrics_txt", "/home/jaegun/projects/knu_project/YuE/prompt_egs/lyrics.txt",
    "--cuda_idx", "0",
    "--stage1_model", "m-a-p/YuE-s1-7B-anneal-en-cot",
    "--stage2_model", "m-a-p/YuE-s2-1B-general",
    "--run_n_segments", "2",
    "--stage2_batch_size", "4",
    "--output_dir", "/home/jaegun/projects/knu_project/main/output",
    "--max_new_tokens", "3000",
    "--repetition_penalty", "1.1"
]

# YuE 실행 시 cwd 지정 (실행 경로 변경)
result = subprocess.run(yue_cmd, cwd=yue_inference_path, capture_output=True, text=True)
