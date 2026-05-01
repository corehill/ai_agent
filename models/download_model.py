import os
import tarfile
import requests

# ======================
# 全局：强制国内镜像
# ======================
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ======================
# 1. 下载 BGE 向量模型
# ======================
# from huggingface_hub import snapshot_download
#
# print("正在下载 BGE 向量模型...")
# snapshot_download(
#     repo_id="BAAI/bge-small-zh-v1.5",
#     local_dir="./models/embedding/bge-small-zh-v1.5",
#     local_dir_use_symlinks=False
# )

# ======================
# 2. 下载 PaddleOCR 模型（det/rec/cls）
# ======================
# 国内镜像下载地址
OCR_MODELS = {
    "det": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_infer.tar",
    "rec": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar",
    "cls": "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar",
}

def download_and_extract(url, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    tar_path = os.path.join(target_folder, "model.tar")

    # 下载
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tar_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # 解压
    with tarfile.open(tar_path, "r") as tar:
        # 解压到临时目录
        temp_dir = os.path.join(target_folder, "tmp")
        tar.extractall(temp_dir)

        # 把里面的模型文件移到目标文件夹
        inner_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        for fname in os.listdir(inner_dir):
            src = os.path.join(inner_dir, fname)
            dst = os.path.join(target_folder, fname)
            with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                fdst.write(fsrc.read())

    # 清理垃圾文件
    os.remove(tar_path)
    import shutil
    shutil.rmtree(os.path.join(target_folder, "tmp"))

print("正在下载 OCR det 模型...")
download_and_extract(OCR_MODELS["det"], "./det")

print("正在下载 OCR rec 模型...")
download_and_extract(OCR_MODELS["rec"], "./rec")

print("正在下载 OCR cls 模型...")
download_and_extract(OCR_MODELS["cls"], "./cls")

print("✅ 所有模型下载完成！全部自动就位！")