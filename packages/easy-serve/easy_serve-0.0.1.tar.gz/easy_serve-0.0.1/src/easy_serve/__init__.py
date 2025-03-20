import requests

class EasyServe():
    
    def model_init(self):
        raise NotImplementedError("model_init method is not implemented")
    
    def preprocessing(self, request:requests.Request):
        raise NotImplementedError("preprocessing is not implemented yet")
    
    def postprocessing(self):
        raise NotImplementedError("postprocessing is not implemented yet")
    
    def inference(self , *args):
        return self.model.forward(*args)