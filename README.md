# Docker Prompt Generator

<img src="./.github/prompt.png" width="300px">

[中文文档](./README-CN.md)

> Using a Model to generate prompts for Model applications (MidJourney, Stable Diffusion, etc...)

## Preview

Like the official Mid Journey function, it supports parsing prompts from images and secondary extensions based on prompts.

![](./.github/preview.jpg)

Support writing prompts directly in Chinese, and then get prompts text that can be used for better effect generation.

![](./.github/preview-translate.jpg)

## Usage

In the past [several articles](https://soulteary.com/tags/python.html), I mentioned my personal habits and recommended development environment, which is based on Docker and Nvidia's official base container for deep learning environments. I won't go into details about that here, but if you're interested, you can check out articles like this one on [getting started with Docker-based deep learning environments](https://soulteary.com/2023/03/22/docker-based-deep-learning-environment-getting-started.html). I believe that long-time readers should already be quite familiar with it.

Of course, since this article includes parts that can be played with just a CPU, you can also refer to [Playing with the Stable Diffusion Model on MacBook Devices with M1 and M2 chips](https://soulteary.com/2022/12/10/play-the-stable-diffusion-model-on-macbook-devices-with-m1-and-m2-chips.html) from a few months ago to configure your environment.

Once you have prepared the Docker environment configuration, we can continue to have fun.

Find a suitable directory and use `git clone` or download the Zip archive to get the "Docker Prompt Generator" project code onto your local machine.

```bash
git clone https://github.com/soulteary/docker-prompt-generator.git
# or
curl -sL -o docker-prompt-generator.zip https://github.com/soulteary/docker-prompt-generator/archive/refs/heads/main.zip
```

Next, enter the project directory and use Nvidia's official PyTorch Docker base image to build the basic environment. Compared to pulling a pre-made image directly from DockerHub, building it yourself will save a lot of time.

Execute the following commands in the project directory to complete the model application build:

```bash
# Build the base image
docker build -t soulteary/prompt-generator:base . -f docker/Dockerfile.base

# Build the CPU application
docker build -t soulteary/prompt-generator:cpu . -f docker/Dockerfile.cpu

# Build the GPU application
docker build -t soulteary/prompt-generator:gpu . -f docker/Dockerfile.gpu
```

Then, depending on your hardware environment, selectively execute the following commands to start a model application with a Web UI interface.

```bash
# Run the CPU image
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -p 7860:7860 soulteary/prompt-generator:cpu

# Run the GPU image
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -p 7860:7860 soulteary/prompt-generator:gpu
```

Enter the IP address of the host running the container in your browser, and you can start using the tool.


## Credits

Models:

- Prompt Model: [succinctly/text2image-prompt-generator](https://huggingface.co/succinctly/text2image-prompt-generator)
- Translator Model: [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) / [GitHub](https://github.com/Helsinki-NLP/OPUS-MT-train)
- CLIP Model: [laion/CLIP-ViT-H-14-laion2B-s32B-b79K](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K)

Datasets:

- Datasets: [succinctlyai/midjourney-texttoimage](https://www.kaggle.com/datasets/succinctlyai/midjourney-texttoimage)
