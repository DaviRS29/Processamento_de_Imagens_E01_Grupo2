

class ProcessamentoImagemService:
    def __init__(self, pre_processamento, segmentacao, pos_processamento, extracao_atributos, classificacao_reconhecimento):
        self.pre_processamento = pre_processamento
        self.segmentacao = segmentacao
        self.pos_processamento = pos_processamento
        self.extracao_atributos = extracao_atributos
        self.classificacao_reconhecimento = classificacao_reconhecimento

    def processar_imagem(self, imagem):
        if self.pre_processamento:
            imagem = self.pre_processamento(imagem)
        if self.segmentacao:
            imagem = self.segmentacao(imagem)
        if self.pos_processamento:
            imagem = self.pos_processamento(imagem)
        if self.extracao_atributos:
            imagem = self.extracao_atributos(imagem)
        if self.classificacao_reconhecimento:
            imagem = self.classificacao_reconhecimento(imagem)
        
        
        
        #TODO: Implementar o processamento da imagem
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