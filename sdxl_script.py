import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image, ImageEnhance
import gc

# ==========================================
# SETTINGS
# ==========================================
# SDXL base generation settings
base_width = 768  # SDXL default
base_height = 768
base_steps = 30
base_guidance = 7.5

# Memory optimization settings
enable_attention_slicing = True
low_vram_mode = True  # Set True if you have <16GB VRAM

device = "cuda"
dtype = torch.float16

# Seed for reproducibility (set to None for random)
seed = None  # Change to a number like 12345 for consistent results

# Prompts (SDXL supports longer prompts)
# EDIT THESE TO GENERATE YOUR DESIRED IMAGE
prompt = "a beautiful landscape with mountains and a lake, sunset, photorealistic, high quality, detailed"
negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, watermark, text"

# ==========================================
# HELPER FUNCTION: Aggressive Memory Cleanup
# ==========================================
def clear_memory():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

# ==========================================
# PART A: GENERATE BASE IMAGE (SDXL)
# ==========================================
print("=" * 50)
print("SDXL IMAGE GENERATION PIPELINE")
print("(VRAM-Optimized for P100)")
print("=" * 50)

print("\n--- Loading SDXL Model ---")
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = StableDiffusionXLPipeline.from_pretrained(
    model_id, torch_dtype=dtype, use_safetensors=True
).to(device)

if enable_attention_slicing:
    pipe.enable_attention_slicing()

# Set up generator for reproducibility
generator = None
if seed is not None:
    generator = torch.Generator(device=device).manual_seed(seed)
    print(f"Using seed: {seed}")

print(f"\n--- Generating Base Image ({base_width}x{base_height}) ---")
print(f"Steps: {base_steps}, Guidance: {base_guidance}")

base_image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=base_width,
    height=base_height,
    num_inference_steps=base_steps,
    guidance_scale=base_guidance,
    generator=generator,
    output_type="pil"
).images[0]

base_image.save("sdxl_base_image.png")
print("Base image saved!")

# ==========================================
# PART B: POST-PROCESSING ENHANCEMENT
# ==========================================
print("\n--- Applying Post-Processing Enhancements ---")

def enhance_image(img, sharpness=1.10, contrast=1.05, color=1.03):
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color)
    return img

enhanced_image = enhance_image(base_image)
enhanced_image.save("sdxl_final_enhanced.png")

# Clean up
clear_memory()

print("\n" + "=" * 50)
print("SDXL GENERATION COMPLETE!")
print("=" * 50)
print("\nOutput files:")
print("  1. sdxl_base_image.png - Initial ({base_width}x{base_height})")
print("  2. sdxl_final_enhanced.png - Post-processed (BEST)")
print("=" * 50)

enhanced_image
