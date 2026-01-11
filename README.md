# Stable Diffusion on Kaggle GPU P100 - Complete Setup Guide

Learn how to run Stable Diffusion models on Kaggle's free GPU P100 (16GB VRAM). This repository contains optimized scripts and step-by-step guides to help you set up your own AI image generation pipeline.

## 🎯 What You'll Learn

- Set up Stable Diffusion XL and other models on Kaggle
- Optimize memory usage for 16GB VRAM (P100 GPU)
- Generate single images, bulk images, and 4K wallpapers
- Understand progressive upscaling techniques
- Customize prompts and settings for your needs

## 📚 Perfect For

- Beginners learning about diffusion models
- Students wanting to experiment with AI art
- Developers building image generation tools
- Anyone wanting free GPU access for Stable Diffusion

## 🖥️ Target Platform: Kaggle GPU P100

This guide is specifically optimized for **Kaggle's free GPU P100** which has:
- 16GB VRAM
- CUDA support
- Free usage hours
- Pre-installed PyTorch

All scripts are tested and working on Kaggle's environment.

## 🚀 Quick Start on Kaggle

### Option 1: Using Kaggle Notebooks (Recommended)

1. **Create a new Kaggle Notebook**
   - Go to [kaggle.com/code](https://www.kaggle.com/code)
   - Click "New Notebook"
   - Turn on GPU: Settings → Accelerator → GPU P100

2. **Clone this repository in Kaggle**
   ```python
   !git clone https://github.com/yourusername/stable-diffusion-kaggle.git
   %cd stable-diffusion-kaggle
   ```

3. **Install dependencies**
   ```python
   !pip install -q diffusers transformers accelerate safetensors
   ```

4. **Run a script**
   ```python
   !python sdxl_script.py
   ```

### Option 2: Local Setup

If you have your own GPU:

```bash
git clone https://github.com/pasan2002/stable-diffusion-Kaggle
cd stable-diffusion-kaggle
pip install -r requirements.txt
python sdxl_script.py
```

## 📖 Three Scripts Included

### 1️⃣ `sdxl_script.py` - Single Image with SDXL

**Best for**: High-quality single images using Stable Diffusion XL

```python
# In Kaggle or Terminal
!python sdxl_script.py
```

**What it does**:
- Generates 768x768 base image
- Applies post-processing enhancement
- Memory optimized for P100

**Customize**: Edit the script to change:
- `prompt` - Your image description (line 25)
- `base_width/height` - Resolution (lines 11-12)
- `base_steps` - Quality vs speed (line 13)
- `seed` - For reproducible results (line 23)

### 2️⃣ `bulk_generate.py` - Multiple Images

**Best for**: Generating many variations or building datasets

```python
!python bulk_generate.py
```

**What it does**:
- Generates N images with random seeds
- Progressive upscaling for each
- Saves to `bulk_outputs/` folder

**Customize**:
- `num_images` - How many images (line 9)
- `prompt` - Your description (line 26)

### 3️⃣ `wallpaper.py` - 4K Wallpapers

**Best for**: High-resolution wallpapers with progressive upscaling

```python
!python wallpaper.py
```

**Pipeline**: 512x288 → 960x540 → 1920x1080 → 3840x2160

**What it does**:
- Multi-stage AI upscaling
- Final PIL upscale to 4K
- Memory-efficient for P100

**Customize**:
- `prompt` - Your wallpaper theme (line 48)

## 📝 Understanding the Code

### Script Structure

All scripts follow this pattern:

```python
# 1. SETTINGS - Configure your generation
base_width = 768
prompt = "your description here"

# 2. HELPER FUNCTIONS - Memory management
def clear_memory():
    # Cleans up GPU RAM

# 3. LOAD MODEL - Downloads/loads from cache
pipe = StableDiffusionXLPipeline.from_pretrained(...)

# 4. GENERATE - Create the image
image = pipe(prompt=prompt, ...)

# 5. POST-PROCESS - Enhance quality
enhanced = enhance_image(image)

# 6. SAVE - Write to disk
image.save("output.png")
```

### Key Functions Explained

**`clear_memory()`**
- Frees up GPU VRAM
- Call between pipeline switches
- Prevents out-of-memory errors

**`enhance_image()`**
- Improves sharpness, contrast, color
- Uses PIL (no GPU needed)
- Apply after generation

**`pipe.enable_attention_slicing()`**
- Reduces VRAM usage
- Slightly slower but memory-safe
- Essential for P100

## 🎨 How to Customize

### Change Your Prompt

Open any script and find the `prompt` variable:

```python
# Replace this with your description
prompt = "YOUR DESCRIPTION HERE"

# Examples:
# "a serene mountain landscape at sunset, photorealistic, 4k"
# "cyberpunk city with neon lights, rainy streets, cinematic"
# "portrait of a cat wearing a crown, oil painting style"
```

### Prompt Engineering Tips

✅ **Do**:
- Start with quality keywords: "masterpiece, best quality, detailed"
- Be specific: "red sports car" not just "car"
- Add style: "photorealistic", "oil painting", "anime style"
- Use negative prompts to avoid bad results

❌ **Don't**:
- Make prompts too long (keep under 77 tokens)
- Use contradictory terms
- Forget negative prompts

### Use Different Models

Change `model_id` in any script:

```python
# Stable Diffusion XL (best quality)
model_id = "stabilityai/stable-diffusion-xl-base-1.0"

# Realistic Vision V6 (photorealistic)
model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"

# DreamShaper (artistic)
model_id = "Lykon/DreamShaper"
```

Find more models on [Hugging Face](https://huggingface.co/models?pipeline_tag=text-to-image)

### Adjust Resolution

```python
# Higher resolution = better quality but slower
base_width = 512   # Try: 512, 768, 1024
base_height = 512  # Keep aspect ratio in mind
```

### Change Generation Speed

```python
# More steps = better quality but slower
base_steps = 30  # Fast: 20, Balanced: 30, Quality: 50
```

## 💾 Output Files

### From `sdxl_script.py`
```
sdxl_base_image.png          # Initial 768x768 image
sdxl_final_enhanced.png      # Post-processed (recommended)
```

### From `bulk_generate.py`
```
bulk_outputs/
  01_base_image_1.png        # Base generation
  02_refined_upscale_1.png   # After upscaling
  03_final_enhanced_1.png    # Best quality
  ... (repeated for each image)
```

### From `wallpaper.py`
```
01_wallpaper_base.png        # 512x288 base
02_wallpaper_960p.png        # First upscale
03_wallpaper_1080p.png       # Full HD
04_wallpaper_4k_raw.png      # 4K raw
04_wallpaper_4k_final.png    # 4K enhanced (best)
```

## 🤖 Models Information

This project uses pre-trained models from Hugging Face:

| Model | Size | Best For | Quality |
|-------|------|----------|----------|
| [SDXL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | ~6.9GB | High quality, any style | ⭐⭐⭐⭐⭐ |
| [Realistic Vision V6](https://huggingface.co/SG161222/Realistic_Vision_V6.0_B1_noVAE) | ~2.1GB | Photorealistic images | ⭐⭐⭐⭐ |
| [SD VAE](https://huggingface.co/stabilityai/sd-vae-ft-mse) | ~330MB | Image quality booster | ⭐⭐⭐⭐ |

**First Run**: Models download automatically (~7GB total)
**Subsequent Runs**: Load from cache (much faster)

## ⚠️ Common Issues & Solutions

### On Kaggle

**"CUDA out of memory"**
- Solution: Reduce resolution or steps
- For wallpaper.py: This is already optimized for P100
- Add this at the top of your script:
  ```python
  import torch
  torch.cuda.empty_cache()
  ```

**"Quota exceeded"**
- Kaggle gives ~30 hours GPU/week
- Check your quota: Settings → GPU Quota
- Turn off GPU when not generating

**"Model download is slow"**
- First run downloads ~6GB model
- Kaggle caches models for 7 days
- Be patient on first run

**"Session timed out"**
- Kaggle sessions timeout after 12 hours
- Save outputs before timeout
- Download generated images regularly

### Image Quality Issues

**Blurry/low quality images**
- ✅ Increase `base_steps` to 40-50
- ✅ Use better prompts with quality keywords
- ✅ Try SDXL model (higher quality)

**Weird/distorted results**
- ✅ Add to negative_prompt: "deformed, ugly, blurry"
- ✅ Increase `guidance_scale` to 8-10
- ✅ Change seed (try different numbers)

**Images don't match prompt**
- ✅ Be more specific in your prompt
- ✅ Increase guidance_scale
- ✅ Check if prompt is too long (>77 tokens)

## Models Used

- [Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- [Realistic Vision V6](https://huggingface.co/SG161222/Realistic_Vision_V6.0_B1_noVAE)
- [SD VAE](https://huggingface.co/stabilityai/sd-vae-ft-mse)

All models are automatically downloaded on first run and cached for future use.


## 📚 Learning Resources

### For Beginners

- [What is Stable Diffusion?](https://stability.ai/stable-diffusion)
- [Hugging Face Diffusers Docs](https://huggingface.co/docs/diffusers)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Kaggle GPU Guide](https://www.kaggle.com/docs/notebooks#gpu)

### Advanced Topics

- **Fine-tuning models**: Train on your own images
- **ControlNet**: Control generation with images
- **LoRA**: Lightweight model adaptations
- **Inpainting**: Edit parts of existing images

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork this repository
2. Try the scripts on Kaggle
3. Suggest improvements via Issues
4. Submit Pull Requests

**Ideas for contributions**:
- Add new model presets
- Optimize for different GPUs
- Create example notebooks
- Improve documentation

## 📝 License

MIT License - Free to use, modify, and share

**Important**: Generated images may be subject to model licenses. Check individual model cards on Hugging Face.

## 👏 Acknowledgments

- **Stability AI** - Stable Diffusion models
- **Hugging Face** - Diffusers library
- **Kaggle** - Free GPU compute
- **Community** - Model creators and contributors

## ❓ FAQ

**Q: Is this really free?**
A: Yes! Kaggle provides free GPU hours weekly.

**Q: Can I use generated images commercially?**
A: Check the specific model's license on Hugging Face.

**Q: How long does generation take?**
A: On P100: ~30 seconds for single image, ~5 minutes for bulk 10 images.

**Q: Can I use this without Kaggle?**
A: Yes, if you have your own NVIDIA GPU with 8GB+ VRAM.

**Q: What if I get low quality results?**
A: Improve your prompt, increase steps, or try different models.

---

**Start generating amazing AI images today!** 🎨

Have questions? Open an issue on GitHub!
