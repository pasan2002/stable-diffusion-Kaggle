import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, AutoencoderKL, DPMSolverMultistepScheduler
from PIL import Image, ImageEnhance
import numpy as np
import gc
import os

# ==========================================
# BULK GENERATION SETTINGS
# ==========================================
num_images = 10  # Set how many images you want to generate
output_dir = "bulk_outputs"
os.makedirs(output_dir, exist_ok=True)

# Base generation settings
base_width = 512
base_height = 768
base_steps = 40
base_guidance = 7.0
upscale_factor = 1.5
refiner_steps = 35
refiner_strength = 0.35
refiner_guidance = 7.0

enable_attention_slicing = True
enable_vae_slicing = True
enable_vae_tiling = True
low_vram_mode = True

# EDIT THIS PROMPT TO GENERATE YOUR DESIRED IMAGES
prompt = "a beautiful landscape with mountains and a lake, sunset, photorealistic, high quality, detailed"
negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, watermark, text"

device = "cuda"
dtype = torch.float16

# ==========================================
def clear_memory():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

def enhance_image(img, sharpness=1.15, contrast=1.05, color=1.02):
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color)
    return img

print("=" * 50)
print(f"BULK IMAGE GENERATION: {num_images} images")
print("=" * 50)

vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=dtype).to(device)
model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"

for i in range(1, num_images + 1):
    print(f"\n--- Generating image {i}/{num_images} ---")
    # Optionally randomize seed for each image
    seed = np.random.randint(0, 2**32 - 1)
    generator = torch.Generator(device=device).manual_seed(seed)
    print(f"Using seed: {seed}")

    # Load Txt2Img Pipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, vae=vae, torch_dtype=dtype, use_safetensors=False
    ).to(device)
    pipe.safety_checker = None
    pipe.requires_safety_checker = False
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++"
    )
    pipe.enable_attention_slicing("max")
    pipe.enable_vae_slicing()
    if enable_vae_tiling:
        pipe.enable_vae_tiling()

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
    base_path = os.path.join(output_dir, f"01_base_image_{i}.png")
    base_image.save(base_path)
    print(f"Base image saved: {base_path}")

    # Upscale
    target_width = int(base_width * upscale_factor)
    target_height = int(base_height * upscale_factor)
    upscaled_input = base_image.resize((target_width, target_height), resample=Image.LANCZOS)
    del pipe
    clear_memory()

    refiner = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_id, vae=vae, torch_dtype=dtype, use_safetensors=False
    ).to(device)
    refiner.safety_checker = None
    refiner.scheduler = DPMSolverMultistepScheduler.from_config(
        refiner.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++"
    )
    refiner.enable_attention_slicing("max")
    refiner.enable_vae_slicing()
    if enable_vae_tiling:
        refiner.enable_vae_tiling()
    clear_memory()

    refined_image = refiner(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=upscaled_input,
        num_inference_steps=refiner_steps,
        strength=refiner_strength,
        guidance_scale=refiner_guidance,
        generator=generator,
    ).images[0]
    refined_path = os.path.join(output_dir, f"02_refined_upscale_{i}.png")
    refined_image.save(refined_path)
    print(f"Refined image saved: {refined_path}")

    enhanced_image = enhance_image(refined_image)
    enhanced_path = os.path.join(output_dir, f"03_final_enhanced_{i}.png")
    enhanced_image.save(enhanced_path)
    print(f"Enhanced image saved: {enhanced_path}")

    del refiner
    clear_memory()

print("\n" + "=" * 50)
print(f"BULK GENERATION COMPLETE! {num_images} images saved in '{output_dir}'")
print("=" * 50)
