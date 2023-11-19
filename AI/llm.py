import os
from pydantic import Field
from typing import List, Mapping, Optional, Any
from langchain.llms.base import LLM
from gpt4all import GPT4All

class MyGPT4ALL(LLM):
    """
    A custom LLM class that integrates gpt4all models
    
    Arguments:

    model_folder_path: (str) Folder path where the model lies
    model_name: (str) The name of the model to use (<model name>.bin)
    allow_download: (bool) whether to download the model or not

    backend: (str) The backend of the model (Supported backends: llama/gptj)
    n_threads: (str) The number of threads to use
    n_predict: (str) The maximum numbers of tokens to generate
    temp: (str) Temperature to use for sampling
    top_p: (float) The top-p value to use for sampling
    top_k: (float) The top k values use for sampling
    n_batch: (int) Batch size for prompt processing
    repeat_last_n: (int) Last n number of tokens to penalize
    repeat_penalty: (float) The penalty to apply repeated tokens
    
    """
    model_folder_path: str = Field(None, alias='model_folder_path')
    model_name: str = Field(None, alias='model_name')
    allow_download: bool = Field(None, alias='allow_download')

    # # all the optional arguments

    backend:        Optional[str]   = 'gptj'
    temp:           Optional[float] = 0.7
    top_p:          Optional[float] = 0.1
    top_k:          Optional[int]   = 40
    n_batch:        Optional[int]   = 8
    n_threads:      Optional[int]   = 4
    n_predict:      Optional[int]   = 1024
    max_tokens:     Optional[int]   = 1024
    repeat_last_n:  Optional[int]   = 64
    repeat_penalty: Optional[float] = 1.18


    # initialize the model
    gpt4_model_instance:Any = None 

    def __init__(self, model_folder_path, model_name, allow_download, **kwargs):
        super(MyGPT4ALL, self).__init__()
        self.model_folder_path: str = model_folder_path
        self.model_name = model_name
        self.allow_download = allow_download
        
        # trigger auto download
        self.auto_download()

        self.gpt4_model_instance = GPT4All(
            model_name=self.model_name,
            model_path=self.model_folder_path,
        )

        
    def auto_download(self) -> None:
        """
        This method will download the model to the specified path
        reference: python.langchain.com/docs/modules/model_io/models/llms/integrations/gpt4all
        """

        # import all the required dependencies
        import requests
        from tqdm import tqdm
        
        # see whether the model name has .bin or not

        model_name = (
            f"{model_name}.bin"
            if not self.model_name.endswith(".bin")
            else self.model_name
        )

        download_path = os.path.join(self.model_folder_path, model_name)

        if not os.path.exists(download_path):
            if self.allow_download:

                # send a GET request to the URL to download the file.
                # Stream it while downloading, since the file is large
        
                try:
                    url = f'http://gpt4all.io/models/{model_name}'

                    response = requests.get(url, stream=True)
                    # open the file in binary mode and write the contents of the response 
                    # in chunks.
                    
                    with open(download_path, 'wb') as f:
                        for chunk in tqdm(response.iter_content(chunk_size=8912)):
                            if chunk: f.write(chunk)
                
                except Exception as e:
                    print(f"=> Download Failed. Error: {e}")
                    return
                
                print(f"=> Model: {self.model_name} downloaded sucessfully 🥳")
            
            else:
                print(
                    f"Model: {self.model_name} does not exists in {self.model_folder_path}",
                    "Please either download the model by allow_download = True else change the path"
                )
    
    @property
    def _get_model_default_parameters(self):
        return {
            "max_tokens": self.max_tokens,
            "n_predict": self.n_predict,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "temp": self.temp,
            "n_batch": self.n_batch,
            "repeat_penalty": self.repeat_penalty,
            "repeat_last_n": self.repeat_last_n,
        }

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get all the identifying parameters
        """
        return {
            'model_name' : self.model_name,
            'model_path' : self.model_folder_path,
            'model_parameters': self._get_model_default_parameters
        }

    @property
    def _llm_type(self) -> str:
        return 'llama'
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """
        Args:
            prompt: The prompt to pass into the model.
            stop: A list of strings to stop generation when encountered

        Returns:
            The string generated by the model        
        """
        
        params = {
            **self._get_model_default_parameters, 
            **kwargs
        }

        resposne = self.gpt4_model_instance.generate(prompt, **params)
        return resposne
    

import hydra


@hydra.main(config_path='configs', config_name='config')
def main(cfg):
    # instantiate the model and populate the arguments using hydra

    chat_model = MyGPT4ALL(
        model_folder_path=cfg.model.gpt4all_model.gpt4all_model_folder_path,
        model_name=cfg.model.gpt4all_model.gpt4all_model_name,
        allow_download=cfg.model.gpt4all_model.gpt4all_allow_downloading,
        allow_streaming=cfg.model.gpt4all_model.gpt4all_allow_streaming,
        
    )

    query = """
Input = [
"The One World",
"Artificial Intelligence and Software Development Intern",
"Dec. 2021 – Aug. 2022",
"Bangalore",

Generate Output like this Example of from above info:
{
    'postion': '',
    'company': '',
    'start_date': '',
    'end_date': '',
    'location': '',
}
"""
    if query == 'exit':
        exit()
    
    print(f"Query: {query}")

    # use hydra to fill the **kwargs
    response = chat_model(
        query,
        n_predict=cfg.model.gpt4all_model.gpt4all_n_predict,
        temp=cfg.model.gpt4all_model.gpt4all_temperature,
        top_p=cfg.model.gpt4all_model.gpt4all_top_p,
        top_k=cfg.model.gpt4all_model.gpt4all_top_k,
        n_batch=cfg.model.gpt4all_model.gpt4all_n_batch,
        repeat_last_n=cfg.model.gpt4all_model.gpt4all_repeat_last_n,
        repeat_penalty=cfg.model.gpt4all_model.gpt4all_penalty,
        max_tokens=cfg.model.gpt4all_model.gpt4all_max_tokens,
    )
    print(f"Response: {response}")
    # print()

if __name__ == '__main__':
    main()