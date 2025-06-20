# from diffusers import DiffusionPipeline
#
# pipe = DiffusionPipeline.from_pretrained("nvidia/Cosmos-Predict2-2B-Text2Image")
#
# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
# image = pipe(prompt).images[0]
from diffusers import AutoPipelineForText2Image
import torch

pipeline = AutoPipelineForText2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")
generator = torch.Generator("cuda").manual_seed(31)
image = pipeline(
    'Astronaut in a jungle holding a sign reading "Hello World", the text on the sing must be spelled correctly as "Hello World", cold color palette, muted colors, detailed, 8k',
    generator=generator,
).images[0]
image.save("output.png")
