# Docker 作图咒语生成器

<img src="./.github/prompt.png" width="300px">

> 使用模型来生成作图咒语的偷懒工具，支持 MidJourney、Stable Diffusion 等。

## 功能预览

如同 MidJourney 官方新推出的功能，工具支持一键从图片中解析出 Prompt 描述，并能够基于描述进行扩展，以便二次图片生成。

![](./.github/preview.jpg)

工具支持直接使用中文进行原始 Prompt 描述，并能够将中文转换为模型生成效果更好的英文 Prompt 描述。

![](./.github/preview-translate.jpg)

## 使用方法


在过去的[几篇文章](https://soulteary.com/tags/python.html)里，我提到过了我个人习惯和推荐的开发环境，基于 Docker 和 Nvidia 官方基础容器的深度学习环境，所以就不再赘述相关知识点，感兴趣可以自行翻阅，比如这篇[《基于 Docker 的深度学习环境：入门篇》](https://soulteary.com/2023/03/22/docker-based-deep-learning-environment-getting-started.html)。相信老读者应该已经很熟悉啦。

当然，因为本文包含纯 CPU 也能玩的部分，你也可以参考几个月前的[《在搭载 M1 及 M2 芯片 MacBook设备上玩 Stable Diffusion 模型》](https://soulteary.com/2022/12/10/play-the-stable-diffusion-model-on-macbook-devices-with-m1-and-m2-chips.html)，来配置你的环境。

在准备好 Docker 环境的配置之后，我们就可以继续玩啦。

我们随便找一个合适的目录，使用 `git clone` 或者下载 Zip 压缩包的方式，先把“Docker Prompt Generator(Docker 作图咒语生成器)”项目的代码下载到本地。

```bash
git clone https://github.com/soulteary/docker-prompt-generator.git
# or
curl -sL -o docker-prompt-generator.zip https://github.com/soulteary/docker-prompt-generator/archive/refs/heads/main.zip
```

接着，进入项目目录，使用 Nvidia 原厂的 PyTorch Docker 基础镜像来完成基础环境的构建，相比于我们直接从 DockerHub 拉制作好的镜像，自行构建将能节约大量时间。

我们在项目目录中执行下面的命令，就能够完成应用模型应用的构建啦：

```bash
# 构建基础镜像
docker build -t soulteary/prompt-generator:base . -f docker/Dockerfile.base

# 构建 CPU 应用
docker build -t soulteary/prompt-generator:cpu . -f docker/Dockerfile.cpu

# 构建 GPU 应用
docker build -t soulteary/prompt-generator:gpu . -f docker/Dockerfile.gpu
```

然后，根据你的硬件环境，选择性执行下面的命令，就能够启动一个带有 Web UI 界面的模型应用啦。

```bash
# 运行 CPU 镜像
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -p 7860:7860 soulteary/prompt-generator:cpu

# 运行 GPU 镜像
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -p 7860:7860 soulteary/prompt-generator:gpu
```

我们在浏览器中输入运行容器的宿主机的 IP 地址，就能够开始使用工具啦。


## 相关项目

模型类项目:

- Prompt Model: [succinctly/text2image-prompt-generator](https://huggingface.co/succinctly/text2image-prompt-generator)
- Translator Model: [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) / [GitHub](https://github.com/Helsinki-NLP/OPUS-MT-train)
- CLIP Model: [laion/CLIP-ViT-H-14-laion2B-s32B-b79K](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K)

数据集项目:

- Datasets: [succinctlyai/midjourney-texttoimage](https://www.kaggle.com/datasets/succinctlyai/midjourney-texttoimage)
