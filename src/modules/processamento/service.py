import os
import uuid
import base64
from datetime import datetime
from core.settings import settings
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


class ProcessamentoImagemService:
    def __init__(self):
        self.output_folder = "processed_images"
        self._ensure_output_folder()

    def _ensure_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def _convert_to_cv_image(self, imagem):
        image_data = imagem.file.read()
        imagem.file.seek(0)
        pil_image = Image.open(BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return cv_image

    def _save_processed_image(self, cv_image, image_id):
        filename = f"{image_id}.jpg"
        filepath = os.path.join(self.output_folder, filename)
        pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        pil_image.save(filepath, "JPEG", quality=95)
        return filepath, filename

    def _convert_to_base64(self, cv_image):
        pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG", quality=95)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_base64

    def processar_imagem(
        self,
        imagem,
        pre_processamento,
        segmentacao,
        pos_processamento,
        extracao_atributos,
        classificacao_reconhecimento,
    ):
        cv_image = self._convert_to_cv_image(imagem)
        original_shape = cv_image.shape
        processed_image = cv_image.copy()
        processing_steps = []

        if pre_processamento:
            pass

        if segmentacao:
            pass

        if pos_processamento:
            pass

        if extracao_atributos:
            pass

        if classificacao_reconhecimento:
            pass

        image_id = str(uuid.uuid4())
        filepath, filename = self._save_processed_image(processed_image, image_id)
        img_base64 = self._convert_to_base64(processed_image)

        return {
            "message": "Imagem processada com sucesso!",
            "image_id": image_id,
            "filename": filename,
            "filepath": filepath,
            "file_base64": img_base64,
            "processing_steps": processing_steps,
            "metadata": {
                "original_shape": original_shape,
                "processed_shape": processed_image.shape,
                "processing_time": datetime.now().isoformat(),
            },
        }

    def pre_processamento(self, imagem):
        pass

    def segmentacao(self, imagem):
        pass

    def pos_processamento(self, imagem):
        pass

    def extracao_atributos(self, imagem):
        pass

    def classificacao_reconhecimento(self, imagem):
        pass
