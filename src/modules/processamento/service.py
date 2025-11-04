import base64
import os
import uuid
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

from modules.processamento.schemas import ImageMetadata, ProcessamentoImagemResponse


class ProcessamentoImagemService:
    def __init__(self):
        self.output_folder = "processed_images"
        self._ensure_output_folder()

    def processar_imagem(
        self,
        imagem: np.ndarray,
        pre_processamento,
        segmentacao,
        pos_processamento,
        extracao_atributos,
        classificacao_reconhecimento,
    ) -> ProcessamentoImagemResponse:
        processed_image = imagem.copy()

        if pre_processamento:
            pass

        if segmentacao:
            processed_image = self.segmentacao(imagem)

        if pos_processamento:
            pass

        if extracao_atributos:
            atributes = self.extracao_atributos(imagem)

        if classificacao_reconhecimento:
            pass

        image_id = str(uuid.uuid4())
        filepath, filename = self._save_processed_image(processed_image, image_id)
        img_base64 = self._convert_to_base64(processed_image)

        image_metadata = ImageMetadata(
            image_id=image_id,
            filename=filename,
            filepath=filepath,
            file_base64=img_base64,
        )

        return ProcessamentoImagemResponse(
            message="Imagem processada com sucesso!",
            generated_at=datetime.now(),
            image_metadata=image_metadata,
        )

    def pre_processamento(self, imagem: np.ndarray):
        pass

    def segmentacao(self, imagem: np.ndarray) -> np.ndarray:
        grayscale: np.ndarray = self._convert_to_gray(imagem)
        blurred: np.ndarray = cv2.GaussianBlur(grayscale, (5, 5), 0)
        return blurred

    def pos_processamento(self, imagem: np.ndarray):
        pass

    def extracao_atributos(self, imagem: np.ndarray):
        # Streamlit precisa rodar como sub-processo
        gray_image: np.ndarray = self._convert_to_gray(imagem)
        
        img_histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        print(gray_image)
        print(img_histogram)
        plt.hist(img_histogram)
        plt.show()


    def classificacao_reconhecimento(self, imagem: np.ndarray):
        pass

    def _ensure_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def _save_processed_image(self, cv_image: np.ndarray, image_id: str):
        filename = f"{image_id}.jpg"
        filepath = os.path.join(self.output_folder, filename)

        if len(cv_image.shape) == 2:
            pil_image = Image.fromarray(cv_image, mode="L")
        else:
            pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

        pil_image.save(filepath, "JPEG", quality=95)
        return filepath, filename

    def _convert_to_gray(self, cv_image:np.ndarray) -> np.ndarray:
        gray_image: np.ndarray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def _convert_to_base64(self, cv_image: np.ndarray):
        if len(cv_image.shape) == 2:
            pil_image = Image.fromarray(cv_image, mode="L")
        else:
            pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG", quality=95)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_base64
