from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")

prompt = 'Astronaut in a jungle holding a sign reading "Hello World", cold color palette, muted colors, detailed, 8k'
image = pipe(prompt).images[0]

image.save("output.png")
