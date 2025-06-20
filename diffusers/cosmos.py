import torch
from diffusers import Cosmos2TextToImagePipeline

# Available checkpoints: nvidia/Cosmos-Predict2-2B-Text2Image, nvidia/Cosmos-Predict2-14B-Text2Image
model_id = "nvidia/Cosmos-Predict2-2B-Text2Image"
pipe = Cosmos2TextToImagePipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
pipe.to("cuda")

prompt = "A close-up shot captures a vibrant yellow scrubber vigorously working on a grimy plate, its bristles moving in circular motions to lift stubborn grease and food residue. The dish, once covered in remnants of a hearty meal, gradually reveals its original glossy surface. Suds form and bubble around the scrubber, creating a satisfying visual of cleanliness in progress. The sound of scrubbing fills the air, accompanied by the gentle clinking of the dish against the sink. As the scrubber continues its task, the dish transforms, gleaming under the bright kitchen lights, symbolizing the triumph of cleanliness over mess."
negative_prompt = "The video captures a series of frames showing ugly scenes, static with no motion, motion blur, over-saturation, shaky footage, low resolution, grainy texture, pixelated images, poorly lit areas, underexposed and overexposed scenes, poor color balance, washed out colors, choppy sequences, jerky movements, low frame rate, artifacting, color banding, unnatural transitions, outdated special effects, fake elements, unconvincing visuals, poorly edited content, jump cuts, visual noise, and flickering. Overall, the video is of poor quality."

output = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    generator=torch.Generator().manual_seed(1),
).images[0]
output.save("output.png")
