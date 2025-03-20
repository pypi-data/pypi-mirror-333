from flask import Flask , request , jsonify 
from easy_serve import EasyServe 
import importlib 
from flask_cors import CORS
import argparse
import traceback
import requests

model = None
def load_model(path , model_name , *args, **kwargs): 
    mod = importlib.import_module(path)
    customModel = getattr(mod , model_name)
    model = customModel(*args , **kwargs)
    model.model_init()
    
    assert isinstance(model , EasyServe) , "Model must be instance of model class"
    
    return model

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "It's working."

def run_prediction(request: requests.Request):
    global model
    if model is None: 
        raise Exception("Model is not loaded")
    data = model.preprocessing(request)
    model_output = model.inference(data)
    post_output = model.postprocessing(model_output)
    
    return post_output

@app.route('/prediction' , methods=["GET" , "POST"])
def prediction():
    try:
        post_output = run_prediction(request)
        return jsonify(post_output)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)})
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_path" , type=str , required=True)
    parser.add_argument("--class_name" , type=str , required=True)
    parser.add_argument("--model_args" , type=str , required=False , default=None)
    parser.add_argument("--port" , type=int , default=5000)

    args = parser.parse_args()
    
    additional_args = {}    
    if args.model_args:
        _args = args.model_args.split(",")
        for arg in _args:
            key , value = arg.split("=")
            additional_args[key] = value
            
    model = load_model(args.class_path , args.class_name , **additional_args)
    app.run(host="0.0.0.0" , port=args.port)