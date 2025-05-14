# 🎵 Video-to-Background Music End-to-End Framework

### 🎬 Automatic Captioning and Music Generation for Video Content

**👥 Authors:**

- Jaegun Lee ([leejken530@knu.ac.kr](mailto:leejken530@knu.ac.kr))
- Taejun Kwon ([ktjmamamoo0629@knu.ac.kr](mailto:ktjmamamoo0629@knu.ac.kr))
- Janghoon Choi ([jhchoi09@knu.ac.kr](mailto:jhchoi09@knu.ac.kr))
- Data Science Department, Kyungpook National University

---

## ✅ **Overview**

This project introduces an end-to-end framework for generating background music automatically for video content. By integrating state-of-the-art video understanding model **VideoLLaMA3** and text-based music generation model **YuE**, we enable automatic video captioning followed by background music generation. 

### 🚀 **Key Features**

- **Automatic Video Captioning:** Extracts visual content, mood, and emotional cues from video.
- **Music Generation:** Produces background music aligned with video content and emotions.
- **End-to-End Pipeline:** Efficiently integrates video understanding and music synthesis.

---

## 🛠️ **Architecture**

The framework is composed of two main components:

![V2B_구조](src\v2m.png)

1.  **Video Captioning:**
    - Uses **VideoLLaMA3** to generate captions that describe visual content, mood, and scene dynamics.
2.  **Music Generation:**
    - Uses **YuE** to generate background music based on the generated captions.

### 📦 **Workflow**

1. Input video is processed by **VideoLLaMA3** to generate a caption.
2. The caption is analyzed to identify key themes and moods.
3. The processed caption is fed into **YuE** to generate the most suitable background music.
4. The generated music is synchronized and embedded into the original video.

---

### 🔧 **Pipeline Diagram**

```
📹 [Video Input] → 📝 [VideoLLaMA3 (Captioning)] → 🎶 [YuE (Music Generation)] → 📦 [Output Video with Music]

```

---

## 🛠️ **Installation**

### 📋 Requirements

- Python 3.10+
- PyTorch 2.x
- CUDA 11.7+
- ffmpeg

### ⚡ **Setup**

```bash
git clone https://github.com/2JAE22/Video-to-BackgroundMusic.git
cd Video-to-BackgroundMusic
pip install -r requirements.txt

```

### ✅ **Environment Setup and Library Installation**

### **1. Clone Repositories**

First, clone the necessary repositories for both **VideoLLaMA3** and **YuE**:

```bash
# Clone VideoLLaMA3
git clone https://github.com/DAMO-NLP-SG/VideoLLaMA3.git
cd VideoLLaMA3

# Clone YuE
cd ..
git clone https://github.com/multimodal-art-projection/YuE.git

```

### **2. Create a New Virtual Environment**

Create a new virtual environment for VideoLLaMA3:

```bash
cd VideoLLaMA3
python3.10 -m venv VL_LLaMa
source VL_LLaMa/bin/activate

```

### **3. Install Poetry and Dependencies**

Install **Poetry** and set up the environment using the provided `pyproject.toml` file:

```bash
pip install poetry
poetry install

```

### **4. Install Essential Libraries**

Install specific versions of **PyTorch** and **torchvision** to ensure compatibility with CUDA 11.8:

```bash
pip install torch==2.4.0 torchvision==0.19.0 --extra-index-url https://download.pytorch.org/whl/cu118

```

If **Flash Attention 2.0** is required:

```bash
pip install flash-attn==2.0.4 --extra-index-url https://download.pytorch.org/whl/cu118

```

### **5. Check FFmpeg Installation**

Ensure **FFmpeg** is properly installed. If not, install it:

```bash
sudo apt update
sudo apt install ffmpeg

```

### **6. Update Configurations in VideoLLaMA3**

Update the `config.yaml` file in the VideoLLaMA3 project to align with the current file structure:

```python
video:
  path: /home/jaegun/projects/knu_project/VideoLLaMA3/assets/videos/cow.mp4
  text: 'Analyze the provided video and generate a set of music genre tags that best
    match the visual content.

    The tags should describe the genre, instrument, mood, and timbre of the background
    music that would be most suitable for this video.

    Use space as a delimiter between tags.

    Guidelines: 1.Genre: Specify a primary music genre (e.g., pop, jazz, rock, electronic,
    orchestral, ambient, etc.). 2.Instrument: Include at least one or more key instruments
    (e.g., guitar, piano, synth, violin, drums, etc.). 3.Mood: Describe the overall
    mood (e.g., uplifting, energetic, melancholic, dreamy, intense, cinematic, etc.).
    4.Timbre: Describe the sound quality (e.g., airy, bright, deep, warm, distorted,
    reverberant, etc.).

    Important Rules: - Must generate at least 5 tags (if necessary, add more descriptive
    elements). - Ensure that the tags best represent the atmosphere and emotion conveyed
    by the video.

    Now, generate the best genre tagging prompt for the given video with at least
    5 tags.'
```

### **7. Setting Up YuE**

Install the required libraries for **YuE**:

```bash
pip install -r requirements.txt

```

---

## 🚀 **Usage**

1. 🗂️ **Place your input video** in the desired directory and update the paths in `250403_main.py`.

### ✅ **Execution Flow in main.py**

The `250403_main.py` script executes the entire pipeline:

1. Updates the video path in `config.yaml`.
2. Runs **VideoLLaMA3** to generate genre tags.
3. Passes the generated tags to **YuE** to generate background music.
4. Merges the generated audio with the video.

---

### **1️⃣ Before Running the Script: Set Video and Audio Paths**

Open the `250403_main.py` script and **update the following paths** with your desired input/output locations:

- **Video Path:** (Input video file path)
    
    ```python
    VIDEO_PATH = "/path/to/your/video.mp4"
    
    ```
    
- **Generated Audio Path:** (Output path for generated audio)
    
    ```python
    GENERATED_AUDIO_PATH = "/path/to/output/YuE_generated.mp3"
    
    ```
    
- **Final Output Path:** (Merged video and audio output path)
    
    ```python
    OUTPUT_VIDEO_PATH = "/path/to/output/final_output.mp4"
    
    ```
    
- **YuE Lyrics File Path:** (Optional lyrics text file path)
    
    ```python
    "--lyrics_txt", "/path/to/YuE/prompt_egs/lyrics.txt",
    
    ```
    

### **2️⃣ Running the Script**

After updating the paths, run the script:

```bash
python 250403_main.py

```

This command will:

- Extract genre tags using **VideoLLaMA3** based on the video content.
- Pass the genre tags to **YuE** to generate background music.
- Merge the generated audio with the original video and save it to the specified output path.

### **3️⃣ Output**

📦 The resulting video with background music will be saved in the specified `OUTPUT_VIDEO_PATH`. 

---

## 🏆 **Results**

Our framework has been tested on various video genres, including vlogs, cinematic clips, and nature documentaries.

The generated music exhibits high fidelity and aligns well with the video content and emotional tone.

---

## 📚 **References**

1. Zhang et al., "VideoLLaMA 3: Frontier Multimodal Foundation Models for Image and Video Understanding", arXiv preprint, 2025.
2. Yuan et al., "YuE: Scaling Open Foundation Models for Long-Form Music Generation", arXiv preprint, 2025.
3. Li et al., "BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation", ICML 2022.
4. Copet et al., "Simple and Controllable Music Generation", arXiv, 2023.

---

## 📌 **Citation**

If you use this framework in your research, please cite the following:

```
@article{lee2025video,
  title={Video-to-Background Music End-to-End Framework: Automatic Captioning and Music Generation for Video Content},
  author={Lee, Jaegun and Kwon, Taejun and Choi, Janghoon},
  journal={arXiv preprint arXiv:2501.13106},
  year={2025}
}

```

---

## 📜 **License**

This project is licensed under the MIT License.