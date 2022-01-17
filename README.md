# Model_Cloning
Repository allows you to replace 9 potential nlp pos-taggers (Legacy Models) with neural network based models (Cloned models). You will find huge efficiency improvement as models can ustilize potential hardwares such as GPUs. Ease-of-use and other powerful properties of neural networks are plus.

## Available models

| **Legacy Models** | **Modelname** | **Domain** | **abbr.** |
| ------------- | ----------------- | ---------- | --------- |
|  NLP4J | Ontonotes | news | on|
| NLP4J  | Mayo | medical | ma |
| Hepple | - | - | hp |
|OpenNLP | Maxent | - | mx |
|OpenNLP | Perceptron | - | pp |
|Stanford|csls-left3w|news|st1|
|Stanford|fast|-|st2|
|Stanford|wsj-0-18-csls|news|st3|


To run the cloned model, we have docker implementation

Please pull docker image and create the container

```docker pull aggarwalpiush/model_cloning```
```docker run -it --name CONTAINERNAME -gpus all ggarwalpiush/model_cloning /bin/bash```

To get the tags, all you need to update the config file. The config file is available at:

```/workspace/delta/model_clone_pos_exp/seq-label/v1/config```

Update train_file path with files available at 

```/workspace/delta/model_clone_pos_exp/seq-label/v1/data/train```

training files are available with variety of data size for each legacy model 


Now update the infer path and res_file with the the input text sentence file and result tags file respectively.


Run the following script:

```python3 /workspace/delta/modelCloneExp/main_batchrun.py```

To save the model, you can use following command:

```python3 delta/main.py --cmd export_model --config <your configuration file>.yml```

Raise issues in case of any clarification or issue raised.

To Postprocess the result files and model evaluation and analysis, provided scripts in this repository can be used.


