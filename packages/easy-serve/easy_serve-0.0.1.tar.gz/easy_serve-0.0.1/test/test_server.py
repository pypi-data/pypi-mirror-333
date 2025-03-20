import os 
import subprocess
import pytest 
from unittest.mock import MagicMock , patch
from easy_serve.server import run_prediction , load_model , app as App
import easy_serve.server


def test_run_prediction(get_model):
    CustomModel = get_model
    custom_args = {"param1": 10}
    test_model_instance = CustomModel(param1=custom_args['param1'])
    
    request = MagicMock()
    request.json = {"data": "hello"}
    
    with patch.object(easy_serve.server , "model" , test_model_instance):
        output = run_prediction(request=request)
        assert output == "Output: hello 10"
        
@pytest.fixture
def app():
    App.config.update({
        "TESTING": True 
    })
    
    yield App 
    
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_check_status(client): 
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"It's working."
    
def test_prediction(client , get_model):
    CustomModel = get_model
    custom_args = {"param1": 30}
    test_model_instance = CustomModel(param1=custom_args['param1'])
    
    request = MagicMock()
    request.json = {"data": "hello"}
    
    with patch.object(easy_serve.server , "model" , test_model_instance):
        response = client.post("/prediction" , json={"data": "haha"})
        assert response.status_code == 200
        assert response.json == "Output: haha 30"
        