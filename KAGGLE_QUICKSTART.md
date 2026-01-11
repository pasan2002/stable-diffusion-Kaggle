# Kaggle Quick Start Guide

This guide will help you run these scripts on Kaggle in under 5 minutes.

## Step 1: Create a Kaggle Notebook

1. Go to [kaggle.com/code](https://www.kaggle.com/code)
2. Click **"New Notebook"**
3. You'll see a new notebook interface

## Step 2: Enable GPU

1. In the notebook, click **"⚙️ Settings"** on the right sidebar
2. Under **"Accelerator"**, select **"GPU P100"**
3. Click **"Save"** (GPU will activate)

## Step 3: Clone This Repository

Create a new code cell and run:

```python
# Clone the repository
!git clone https://github.com/yourusername/stable-diffusion-kaggle.git

# Change to the project directory
%cd stable-diffusion-kaggle

# List files to verify
!ls -la
```

## Step 4: Install Dependencies

In a new cell, run:

```python
!pip install -q diffusers transformers accelerate safetensors
```

This will take ~1-2 minutes.

## Step 5: Run Your First Generation

### Option A: Generate with SDXL (Best Quality)

```python
!python sdxl_script.py
```

**First run takes ~5 minutes** (downloads ~7GB model)  
**Subsequent runs take ~30 seconds**

### Option B: Generate 10 Images (Bulk)

```python
!python bulk_generate.py
```

### Option C: Generate 4K Wallpaper

```python
!python wallpaper.py
```

## Step 6: View Your Generated Images

```python
from IPython.display import Image, display

# Display the generated image
display(Image('sdxl_final_enhanced.png'))
```

## Step 7: Download Your Images

1. Click the **"Output"** tab on the right
2. Find your PNG files
3. Click download icon

## Customizing Your Generation

### Edit Prompts

Before running the script, edit it:

```python
# Open the script
!nano sdxl_script.py
# Or view it first
!cat sdxl_script.py | grep -A 2 "prompt ="
```

Or create a modified version:

```python
# Create a custom script
with open('my_custom_generation.py', 'w') as f:
    f.write('''
import torch
from diffusers import StableDiffusionXLPipeline

prompt = "YOUR CUSTOM PROMPT HERE"
negative_prompt = "blurry, low quality, ugly"

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", 
    torch_dtype=torch.float16
).to("cuda")

pipe.enable_attention_slicing()

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=768,
    height=768,
    num_inference_steps=30,
    guidance_scale=7.5
).images[0]

image.save("my_custom_image.png")
print("Done!")
''')

# Run it
!python my_custom_generation.py
```

## Understanding GPU Quota

Kaggle provides:
- **~30 hours of GPU per week** (free tier)
- **Sessions timeout after 12 hours**
- **Check your quota**: Settings → Your Account → GPU Quota

### Tips to Save GPU Time:
- ✅ Turn off GPU when editing code (no generation)
- ✅ Download images regularly
- ✅ Test with low steps first (20 steps)
- ✅ Increase steps for final version (30-50 steps)

## Common Kaggle Issues

### "CUDA out of memory"

**Solution 1**: Restart kernel and clear cache
```python
import torch
torch.cuda.empty_cache()
```

**Solution 2**: Reduce resolution in script
```python
base_width = 512   # Instead of 768
base_height = 512  # Instead of 768
```

### "Session expired"

**Solution**: Your 12-hour limit hit
- Download all generated images
- Close and create new session
- Models are cached for 7 days (won't re-download)

### "Permission denied"

**Solution**: You need to enable internet
- Settings → Internet → On

## Example Workflow

Here's a complete workflow in one notebook:

```python
# Cell 1: Setup
!git clone https://github.com/yourusername/stable-diffusion-kaggle.git
%cd stable-diffusion-kaggle
!pip install -q diffusers transformers accelerate safetensors

# Cell 2: Generate first image
!python sdxl_script.py

# Cell 3: View it
from IPython.display import Image, display
display(Image('sdxl_final_enhanced.png'))

# Cell 4: Generate more with different prompts
# Edit sdxl_script.py first, then run again
!python sdxl_script.py

# Cell 5: Generate bulk images
!python bulk_generate.py

# Cell 6: View all outputs
import os
from IPython.display import Image, display

for img in os.listdir('bulk_outputs'):
    if img.endswith('.png'):
        print(f"\\n{img}:")
        display(Image(f'bulk_outputs/{img}'))
```

## Tips for Best Results

### Prompt Engineering

✅ **Good prompts**:
```
"a majestic mountain landscape, golden hour, photorealistic, 8k, detailed"
"portrait of a wise old wizard, fantasy art, detailed face, magical atmosphere"
"modern architecture, glass building, sunset reflection, urban photography"
```

❌ **Bad prompts**:
```
"nice picture"  # Too vague
"a cat dog mountain sunset beach city..."  # Too many things
"best quality masterpiece ultra mega super..."  # Too many quality keywords
```

### Generation Settings

| Purpose | Steps | Guidance | Resolution |
|---------|-------|----------|------------|
| Quick test | 20 | 7.0 | 512x512 |
| Balanced | 30 | 7.5 | 768x768 |
| High quality | 50 | 8.0 | 768x768 |
| Wallpaper | 30 | 7.0 | See wallpaper.py |

## Next Steps

1. ⭐ Star the GitHub repo
2. 🎨 Experiment with different prompts
3. 🔧 Try different models
4. 📖 Read the main README.md for advanced features
5. 🤝 Share your results and contribute

## Need Help?

- 📘 Main README: [README.md](README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/stable-diffusion-kaggle/issues)
- 💬 Kaggle Community: [Kaggle Forums](https://www.kaggle.com/discussions)

---

**Happy generating!** 🎨✨
