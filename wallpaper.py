import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, AutoencoderKL, DPMSolverMultistepScheduler
from PIL import Image, ImageEnhance, ImageFilter
import gc

# ==========================================
# HELPER FUNCTION: Aggressive Memory Cleanup
# ==========================================
def clear_memory():
    """Aggressively clear GPU memory"""
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

# ==========================================
# SETTINGS - KAGGLE OPTIMIZED FOR 4K OUTPUT
# ==========================================
# Strategy: 512x288 -> 960x540 (AI) -> 1920x1080 (AI) -> 3840x2160 (PIL)
# This avoids the heavy x4 upscaler that causes OOM on Kaggle

# 1. Base Generation
base_width = 512  
base_height = 288  # 16:9 aspect ratio
base_steps = 30
base_guidance = 7.0

# 2. First Refinement (960x540)
refine1_width = 960
refine1_height = 540
refine1_steps = 25
refine1_strength = 0.45

# 3. Second Refinement (1920x1080 - Full HD)
refine2_width = 1920
refine2_height = 1080
refine2_steps = 20
refine2_strength = 0.30  # Lower to preserve details

# 4. Final 4K (PIL upscale - no AI, very fast, no VRAM)
final_width = 3840
final_height = 2160

# Memory optimizations
enable_vae_tiling = True

# Seed for reproducibility
seed = None

# EDIT THIS PROMPT TO GENERATE YOUR DESIRED WALLPAPER
# Keep it concise and under 77 tokens for best results
prompt = "a beautiful landscape with mountains and a lake, sunset, vibrant colors, 4k wallpaper, high quality, detailed"

negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, watermark, text"

device = "cuda"
dtype = torch.float16
model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"

# ==========================================
# PART A: GENERATE BASE (Composition)
# ==========================================
print("=" * 60)
print("4K WALLPAPER GENERATION - KAGGLE OPTIMIZED")
print("Strategy: 512x288 -> 960x540 -> 1920x1080 -> 3840x2160")
print("(No x4 upscaler - works on 16GB VRAM)")
print("=" * 60)

print("\n--- [1/4] Generating Base Composition ---")
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=dtype).to(device)

pipe = StableDiffusionPipeline.from_pretrained(
    model_id, vae=vae, torch_dtype=dtype, use_safetensors=False
).to(device)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config, 
    use_karras_sigmas=True,
    algorithm_type="dpmsolver++"
)
pipe.safety_checker = None

# Memory optimizations
pipe.enable_attention_slicing("max")
pipe.enable_vae_slicing()
if enable_vae_tiling:
    pipe.enable_vae_tiling()

# Set up generator
generator = None
if seed is not None:
    generator = torch.Generator(device=device).manual_seed(seed)
    print(f"Using seed: {seed}")

print(f"Resolution: {base_width}x{base_height}")
print(f"Steps: {base_steps}")

base_image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=base_width,
    height=base_height,
    num_inference_steps=base_steps,
    guidance_scale=base_guidance,
    generator=generator,
).images[0]

base_image.save("01_wallpaper_base.png")
print("Base saved!")

# ==========================================
# PART B: FIRST REFINEMENT (960x540)
# ==========================================
print(f"\n--- [2/4] Refining to {refine1_width}x{refine1_height} ---")

refine1_input = base_image.resize((refine1_width, refine1_height), resample=Image.LANCZOS)

# Delete base pipeline
del pipe
clear_memory()

# Load refiner
refiner = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id, vae=vae, torch_dtype=dtype, use_safetensors=False
).to(device)

refiner.safety_checker = None
refiner.scheduler = DPMSolverMultistepScheduler.from_config(
    refiner.scheduler.config, 
    use_karras_sigmas=True,
    algorithm_type="dpmsolver++"
)

refiner.enable_attention_slicing("max")
refiner.enable_vae_slicing()
if enable_vae_tiling:
    refiner.enable_vae_tiling()

clear_memory()

print(f"Steps: {refine1_steps}, Strength: {refine1_strength}")

refine1_image = refiner(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=refine1_input,
    num_inference_steps=refine1_steps,
    strength=refine1_strength,
    guidance_scale=base_guidance,
    generator=generator,
).images[0]

refine1_image.save("02_wallpaper_960p.png")
print("960p refinement saved!")

# ==========================================
# PART C: SECOND REFINEMENT (1920x1080 - Full HD)
# ==========================================
print(f"\n--- [3/4] Refining to {refine2_width}x{refine2_height} (Full HD) ---")

# Clear memory before high-res
clear_memory()

refine2_input = refine1_image.resize((refine2_width, refine2_height), resample=Image.LANCZOS)

print(f"Steps: {refine2_steps}, Strength: {refine2_strength}")

refine2_image = refiner(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=refine2_input,
    num_inference_steps=refine2_steps,
    strength=refine2_strength,
    guidance_scale=base_guidance,
    generator=generator,
).images[0]

refine2_image.save("03_wallpaper_1080p.png")
print("1080p refinement saved!")

# Clean up refiner
del refiner, vae
clear_memory()

# ==========================================
# PART D: UPSCALE TO 4K (High-Quality PIL)
# ==========================================
print(f"\n--- [4/4] Upscaling to {final_width}x{final_height} (4K) ---")

# Use PIL's high-quality LANCZOS for 2x upscale (1080p -> 4K)
# This is fast, uses no VRAM, and preserves details well
wallpaper_4k = refine2_image.resize((final_width, final_height), resample=Image.LANCZOS)

# ==========================================
# PART E: POST-PROCESSING ENHANCEMENT
# ==========================================
print("\n--- Applying 4K Enhancement ---")

def enhance_4k_wallpaper(img):
    """Apply enhancements optimized for PIL-upscaled 4K"""
    # Sharpening is important after PIL upscale
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.20)  # Stronger sharpening for 4K
    
    # Subtle contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    
    # Slight color boost
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.03)
    
    # Apply unsharp mask for extra crispness
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=50, threshold=3))
    
    return img

# Apply enhancements
enhanced_4k = enhance_4k_wallpaper(wallpaper_4k)
enhanced_4k.save("04_wallpaper_4k_final.png")

# Also save the raw 4K
wallpaper_4k.save("04_wallpaper_4k_raw.png")

print("\n" + "=" * 60)
print("4K WALLPAPER GENERATION COMPLETE!")
print("=" * 60)
print("\nOutput files:")
print(f"  1. 01_wallpaper_base.png - Base ({base_width}x{base_height})")
print(f"  2. 02_wallpaper_960p.png - First refine ({refine1_width}x{refine1_height})")
print(f"  3. 03_wallpaper_1080p.png - Full HD ({refine2_width}x{refine2_height})")
print(f"  4. 04_wallpaper_4k_raw.png - 4K raw ({final_width}x{final_height})")
print(f"  5. 04_wallpaper_4k_final.png - 4K ENHANCED (BEST)")
print("=" * 60)

enhanced_4k

        