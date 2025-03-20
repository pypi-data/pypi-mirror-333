import os
import sys
import shutil
import gc
import torch
import logging
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urlparse
import requests
import zipfile
import subprocess
import shlex

from rvc_inferpy.modules import VC
from rvc_inferpy.split_audio import (
    split_silence_nonsilent,
    adjust_audio_lengths,
    combine_silence_nonsilent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download link (adjusted to use a direct download URL)
RVC_DOWNLOAD_LINK = "https://huggingface.co/NeoPy/rvc-base/resolve/main"
RVC_MODELS = [
    "hubert_base.pt",
    "rmvpe.pt",
    "fcpe.pt",
]
BASE_DIR = Path(".").resolve()
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

def download_manager(url: str, dest_path: Path) -> None:
    """Download a file from the given URL to the destination path."""
    if dest_path.exists():
        logger.info(f"File {dest_path} already exists. Skipping download.")
        return
    logger.info(f"Downloading {url} to {dest_path}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        logger.info(f"Downloaded {dest_path}.")
    else:
        logger.error(f"Failed to download {url}. Status code: {response.status_code}")
        raise Exception(f"Download failed for {url}")

class Configs:
    def __init__(self, device: str, is_half: bool):
        self.device = device
        self.is_half = is_half
        self.n_cpu = cpu_count()
        self.gpu_name = None
        self.gpu_mem = None
        self.x_pad, self.x_query, self.x_center, self.x_max = self.device_config()

    def device_config(self) -> tuple:
        if torch.cuda.is_available():
            i_device = int(self.device.split(":")[-1])
            self.gpu_name = torch.cuda.get_device_name(i_device)
        elif torch.backends.mps.is_available():
            logger.info("No supported NVIDIA GPU found, using MPS for inference")
            self.device = "mps"
        else:
            logger.info("No supported GPU found, using CPU for inference")
            self.device = "cpu"

        if self.is_half:
            # 6G memory configuration
            x_pad = 3
            x_query = 10
            x_center = 60
            x_max = 65
        else:
            # 5G memory configuration
            x_pad = 1
            x_query = 6
            x_center = 38
            x_max = 41

        if self.gpu_mem is not None and self.gpu_mem <= 4:
            x_pad = 1
            x_query = 5
            x_center = 30
            x_max = 32

        return x_pad, x_query, x_center, x_max

class RVCConverter:
    def __init__(self, device: str = "cuda:0", is_half: bool = True, models_dir: Path = MODELS_DIR, download_if_missing: bool = True):
        self.device = device
        self.is_half = is_half
        self.models_dir = models_dir
        self.download_if_missing = download_if_missing

        # Read model paths from environment; if not provided, use defaults and download if needed.
        self.hubert_model_path = os.environ.get("hubert_model_path")
        if not self.hubert_model_path:
            self.hubert_model_path = str(self.models_dir / "hubert_base.pt")
            if self.download_if_missing and not Path(self.hubert_model_path).exists():
                download_manager(f"{RVC_DOWNLOAD_LINK}/hubert_base.pt", Path(self.hubert_model_path))
        else:
            logger.info(f"Using hubert_model_path from environment: {self.hubert_model_path}")

        self.rmvpe_model_path = os.environ.get("rmvpe_model_path")
        if not self.rmvpe_model_path:
            self.rmvpe_model_path = str(self.models_dir / "rmvpe.pt")
            if self.download_if_missing and not Path(self.rmvpe_model_path).exists():
                download_manager(f"{RVC_DOWNLOAD_LINK}/rmvpe.pt", Path(self.rmvpe_model_path))
        else:
            logger.info(f"Using rmvpe_model_path from environment: {self.rmvpe_model_path}")

        self.fcpe_model_path = os.environ.get("fcpe_model_path")
        if not self.fcpe_model_path:
            self.fcpe_model_path = str(self.models_dir / "fcpe.pt")
            if self.download_if_missing and not Path(self.fcpe_model_path).exists():
                download_manager(f"{RVC_DOWNLOAD_LINK}/fcpe.pt", Path(self.fcpe_model_path))
        else:
            logger.info(f"Using fcpe_model_path from environment: {self.fcpe_model_path}")

        self.configs = Configs(self.device, self.is_half)
        self.vc = VC(self.configs)

    @staticmethod
    def get_model(voice_model: str) -> tuple:
        """
        Return the pth and index file paths for the given voice model.
        Expects the voice model files to reside in:
            {current_working_dir}/models/{voice_model}/
        """
        model_dir = Path(os.getcwd()) / "models" / voice_model
        model_filename = None
        index_filename = None
        if not model_dir.exists():
            logger.error(f"Model directory {model_dir} does not exist.")
            return None, None
        for file in os.listdir(model_dir):
            ext = os.path.splitext(file)[1]
            if ext == ".pth":
                model_filename = file
            if ext == ".index":
                index_filename = file

        if model_filename is None:
            logger.error(f"No model file exists in {model_dir}.")
            return None, None

        pth_path = str(model_dir / model_filename)
        index_path = str(model_dir / index_filename) if index_filename else ""
        return pth_path, index_path

    def infer_audio(
        self,
        voice_model: str,
        audio_path: str,
        f0_change: int = 0,
        f0_method: str = "rmvpe+",
        min_pitch: str = "50",
        max_pitch: str = "1100",
        crepe_hop_length: int = 128,
        index_rate: float = 0.75,
        filter_radius: int = 3,
        rms_mix_rate: float = 0.25,
        protect: float = 0.33,
        split_infer: bool = False,
        min_silence: int = 500,
        silence_threshold: int = -50,
        seek_step: int = 1,
        keep_silence: int = 100,
        do_formant: bool = False,
        quefrency: int = 0,
        timbre: int = 1,
        f0_autotune: bool = False,
        audio_format: str = "wav",
        resample_sr: int = 0,
    ) -> str:
        """
        Perform voice conversion inference on the provided audio file.
        If split_infer is True, the audio will first be segmented based on silence.
        """
        pth_path, index_path = self.get_model(voice_model)
        if pth_path is None:
            logger.error("Model loading failed.")
            return ""
        # Initialize the voice conversion engine with the model.
        vc_data = self.vc.get_vc(pth_path, protect, 0.5)

        if split_infer:
            inferred_files = []
            temp_dir = Path(os.getcwd()) / "seperate" / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Splitting audio into silence and nonsilent segments.")
            silence_files, nonsilent_files = split_silence_nonsilent(
                audio_path, min_silence, silence_threshold, seek_step, keep_silence
            )
            logger.info(f"Total silence segments: {len(silence_files)}. Total nonsilent segments: {len(nonsilent_files)}.")
            for i, nonsilent_file in enumerate(nonsilent_files):
                logger.info(f"Inferring nonsilent audio segment {i+1}")
                inference_info, audio_data, output_path = self.vc.vc_single(
                    0,
                    nonsilent_file,
                    f0_change,
                    f0_method,
                    index_path,
                    index_path,
                    index_rate,
                    filter_radius,
                    resample_sr,
                    rms_mix_rate,
                    protect,
                    audio_format,
                    crepe_hop_length,
                    do_formant,
                    quefrency,
                    timbre,
                    min_pitch,
                    max_pitch,
                    f0_autotune,
                    self.hubert_model_path,
                )
                if inference_info[0] == "Success.":
                    logger.info("Inference ran successfully.")
                    logger.info(inference_info[1])
                    logger.info("Times:\nnpy: %.2fs f0: %.2fs infer: %.2fs\nTotal time: %.2fs" % (*inference_info[2],))
                else:
                    logger.error(f"An error occurred: {inference_info[0]}")
                    return ""
                inferred_files.append(output_path)
            logger.info("Adjusting inferred audio lengths.")
            adjusted_inferred_files = adjust_audio_lengths(nonsilent_files, inferred_files)
            logger.info("Combining silence and inferred audios.")
            output_count = 1
            while True:
                output_path = Path(os.getcwd()) / "output" / f"{Path(audio_path).stem}_{voice_model}_{f0_method.capitalize()}_{output_count}.{audio_format}"
                if not output_path.exists():
                    break
                output_count += 1
            output_path = combine_silence_nonsilent(silence_files, adjusted_inferred_files, keep_silence, str(output_path))
            for inferred_file in inferred_files:
                shutil.move(inferred_file, temp_dir)
            shutil.rmtree(temp_dir)
        else:
            inference_info, audio_data, output_path = self.vc.vc_single(
                0,
                audio_path,
                f0_change,
                f0_method,
                index_path,
                index_path,
                index_rate,
                filter_radius,
                resample_sr,
                rms_mix_rate,
                protect,
                audio_format,
                crepe_hop_length,
                do_formant,
                quefrency,
                timbre,
                min_pitch,
                max_pitch,
                f0_autotune,
                self.hubert_model_path,
            )
            if inference_info[0] == "Success.":
                logger.info("Inference ran successfully.")
                logger.info(inference_info[1])
                logger.info("Times:\nnpy: %.2fs f0: %.2fs infer: %.2fs\nTotal time: %.2fs" % (*inference_info[2],))
            else:
                logger.error(f"An error occurred: {inference_info[0]}")
                return ""
        return output_path

if __name__ == "__main__":
    # Download the base models if they are not provided via environment variables.
    for model_file in RVC_MODELS:
        model_path = BASE_DIR / model_file
        if not model_path.exists():
            download_manager(f"{RVC_DOWNLOAD_LINK}/{model_file}", model_path)
    