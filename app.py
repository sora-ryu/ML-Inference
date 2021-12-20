import json
from io import BytesIO

import torch
from PIL import Image
from flask import Flask, request, jsonify
from torchvision import models
from torchvision import transforms as T

app = Flask(__name__)   # pass current module's name to Flask constructor

device = "cuda" if torch.cuda.is_available() else "cpu"     # switch to cuda if it is available otherwise use 'cpu'
model = models.densenet121(pretrained=True)     # use pre-trained densenet121 model
model.to(device)    # store model in GPU if it is possible
model.eval()    # set the model into evaluation mode to get output values

def preprocess(img):
    # transform objects
    resize = T.Resize(256) # resize to 256
    centerCrop = T.CenterCrop(224) # crop the input image at the center to size 224
    toTensor = T.ToTensor() # convert image to tensor
    normalization = T.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225]) # normalize a tensor img with mean and std

    # composes transforms above
    transform = T.Compose([resize, centerCrop, toTensor, normalization])    # compose the input image and unsqueeze to get tensor

    tensor = transform(img).unsqueeze_(0) #transform the input img and add an extra dimension in the tensor (currently 3-dimensional) to be 4-dimension.
    return tensor # return preprocessed tensor

def get_classification(img):
    tensor = preprocess(img)    # get thee preprocessed tensor
    tensor.to(device)   # store this tensor on gpu if possible
    output = model.forward(tensor)  # get output with the model
    imagenet_class_index = json.load(open('imagenet_class_index.json'))     # get the list of categories from imagenet_class
    values, indices = torch.max(output, 1)  # get soft argmax from the output
    return imagenet_class_index[str(indices.item())]    # get the classification from the list

@app.route('/')
def run():
    # main page
    return 'Server is Running!'

@app.route('/upload', methods=['GET','POST'])
def upload():
    # if the server get 'POST' request
    if request.method == 'POST':
        img = Image.open(request.files['file']) # open the input image from the project folder
        pred_y = get_classification(img)    # get the classification
        # return jsonify(imagenet_id=pred_y[0], classification=pred_y[1])   # send the result in json format
        return "Imagenet_id : %s , Classification : %s " %(str(pred_y[0]),pred_y[1])    # print the output

if __name__=="__main__":
    app.run(host='0.0.0.0')
