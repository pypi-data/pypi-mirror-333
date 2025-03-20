# Easy Serve
High level abstraction for deploying simple machine learning models using Flask. 
This project allows you to quickly deploy a small testing model locally as an API service without complicated setup.

<div align="center">

[![Build Status](https://github.com/tchiayan/easy_serve/actions/workflows/build.yml/badge.svg)](https://github.com/tchiayan/easy_serve/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/easy_serve.svg)](https://badge.fury.io/py/easy_serve)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Getting started
1. Install the package using pip command: `pip install easy_serve`
2. Extend your model using `EasyServe` class. 
3. Run server using this command: `python -m easy_deploy.serve --class_path PATH_TO_easy_serve_CLASS --class_name YOUR_CUSTOM_easy_serve --port PORT --model_args param1=value1;param2=value2`

## Example
1. Create a file custom_model.py
Here's a complete example of creating and deploying a simple model:
```python
from easy_serve import EasyServe

class TextProcessor(EasyServe):
    def __init__(self, prefix=""):
        self.prefix = prefix
    
    def model_init(self):
        print("Model initialized!")
    
    def preprocessing(self, request):
        return request.json.get('text', '')
    
    def inference(self, text):
        return f"{self.prefix} {text}".strip()
    
    def postprocessing(self, result):
        return {"result": result.upper()}
```
2. Run the server
```shell
python -m easy_serve.server --class_path custom_model --class_name TextProcessor --port 5000 --model_args prefix=Hello
```
3. Test with curl:
```shell
curl -X POST http://localhost:5000/prediction -H "Content-Type: application/json" -d '{"text":"world"}'
```
Response:
```json
{"result":"HELLO WORLD"}
```
