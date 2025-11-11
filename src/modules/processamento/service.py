import base64
import os
import uuid
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
import uuid
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
        # Plotar canais de cores da imagem original
        self._plot_single_channel(imagem)
        
        # Converter para escala de cinza
        gray_image: np.ndarray = self._convert_to_gray(imagem)

        # Calcular histograma
        img_histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

        print("Shape imagem cinza:", gray_image.shape)
        print("Soma histograma original:", np.sum(img_histogram))

        normalized_grayscale = self._equalize_hist(gray_image)
        return gray_image, normalized_grayscale

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

    def _convert_to_gray(self, cv_image: np.ndarray) -> np.ndarray:
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

    def _equalize_hist(self, gray_image: np.ndarray) -> np.ndarray:
        """
        Apply histogram equalization and display comparison visualization.
        
        Args:
            gray_image: Input grayscale image
            
        Returns:
            Equalized image
        """
        # Equalize histogram
        equalized = cv2.equalizeHist(gray_image)
        
        # Calculate histograms CORRECTLY
        hist_original = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        hist_equalized = cv2.calcHist([equalized], [0], None, [256], [0, 256])
        
        # Create 2x2 figure
        fig = plt.figure(figsize=(15, 10))
        
        # Original Grayscale Image
        plt.subplot(2, 2, 1)
        plt.imshow(gray_image, cmap='gray')
        plt.title("Imagem Original (Cinza)", fontweight='bold')
        plt.axis('off')
        
        # Original Histogram - FIXED: Use the actual image data, not histogram values
        plt.subplot(2, 2, 2)
        plt.hist(gray_image.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.7)
        plt.title("Histograma Original", fontweight='bold')
        plt.xlabel("Intensidade de Pixel")
        plt.ylabel("Frequência")
        plt.grid(True, alpha=0.3)
        plt.xlim([0, 255])
        
        # Equalized Image
        plt.subplot(2, 2, 3)
        plt.imshow(equalized, cmap='gray')
        plt.title("Imagem Equalizada", fontweight='bold')
        plt.axis('off')
        
        # Equalized Histogram - FIXED: Use the actual image data, not histogram values
        plt.subplot(2, 2, 4)
        plt.hist(equalized.ravel(), bins=256, range=[0, 256], color='red', alpha=0.7)
        plt.title("Histograma Equalizado", fontweight='bold')
        plt.xlabel("Intensidade de Pixel")
        plt.ylabel("Frequência")
        plt.grid(True, alpha=0.3)
        plt.xlim([0, 255])
        
        plt.tight_layout()
        
        # Save the figure
        output_path = os.path.join(self.output_folder, f"histogram_equalization_comparison-{uuid.uuid4()}.jpg")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Histograma equalizado salvo em: {output_path}")
        plt.close(fig)
        
        return equalized
    
    
    def _plot_single_channel(self, original_image: np.ndarray):
        """
        Plot the three color channels (BGR/RGB) of the original image with their histograms.
        
        Args:
            original_image: Input image in BGR format (from OpenCV)
        """
        # Convert BGR to RGB for proper color display
        rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        
        # Split into individual channels
        channels = cv2.split(original_image)  # Returns BGR channels (Blue, Green, Red)
        channel_colors = ['blue', 'green', 'red']
        channel_names = ['Canal Azul (B)', 'Canal Verde (G)', 'Canal Vermelho (R)']
        
        # Create 3x2 figure (3 channels, each with image and histogram)
        fig = plt.figure(figsize=(14, 12))
        
        for i, (channel, color, channel_name) in enumerate(zip(channels, channel_colors, channel_names)):
            # Plot channel image
            plt.subplot(3, 2, i*2 + 1)
            plt.imshow(channel, cmap='gray')
            plt.title(f"{channel_name} - Imagem", fontweight='bold')
            plt.axis('off')
            
            # Plot channel histogram
            plt.subplot(3, 2, i*2 + 2)
            plt.hist(channel.ravel(), bins=256, range=[0, 256], color=color, alpha=0.7)
            plt.title(f"{channel_name} - Histograma", fontweight='bold')
            plt.xlabel("Intensidade de Pixel")
            plt.ylabel("Frequência")
            plt.grid(True, alpha=0.3)
            plt.xlim([0, 255])
        
        plt.tight_layout()
        
        # Save the figure
        output_path = os.path.join(self.output_folder, f"canais_cores-{uuid.uuid4()}.jpg")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Canais de cores salvo em: {output_path}")
        plt.close(fig)