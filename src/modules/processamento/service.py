import os
from core.settings import settings


class ProcessamentoImagemService:
    def __init__(self):
        self.output_folder = settings.OUTPUT_FOLDER
        self.ensure_output_folder()

    def ensure_output_folder(self):
        if not os.path.exists(settings.OUTPUT_FOLDER):
            os.makedirs(settings.OUTPUT_FOLDER)

    def processar_imagem(
        self,
        imagem,
        pre_processamento,
        segmentacao,
        pos_processamento,
        extracao_atributos,
        classificacao_reconhecimento,
    ):
        if pre_processamento:
            imagem = self.pre_processamento(imagem)
        if segmentacao:
            imagem = self.segmentacao(imagem)
        if pos_processamento:
            imagem = self.pos_processamento(imagem)
        if extracao_atributos:
            imagem = self.extracao_atributos(imagem)
        if classificacao_reconhecimento:
            imagem = self.classificacao_reconhecimento(imagem)

        # TODO: Implementar o processamento da imagem
        # return ProcessamentoImagemResponse(
        #     file_base64=imagem.file_base64,
        #     message="Imagem processada com sucesso!",
        #     filename=imagem.filename,
        #     processed_image_url=None,
        # )

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
