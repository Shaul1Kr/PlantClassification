# PlantClassification

This system uses convolutional neural networks (CNNs) to learn unsupervised feature representations for different plant species. This project introduces a new dataset, Plant Classification, for plant species classification with 2296 images categorized into 23 categories. The dataset contains 23 desert plants species, which can be grown at desert climate and are barely covered by existing datasets. 

This project focuses on the analysis of Plant Classification. We report the results of experiments performed on the new dataset. The experiments aimed at testing the quality of Plant Classification. We explored whether accurate classification models can be trained on Plant Classification. Also, we explored transfer learning with two other datasets: ImageNet, which is a classical choice for pre-training, and Oxford102 - a much smaller dataset but more relevant to plants classification. We also experimented with two-steps transfer learning, where models, pre-trained first on ImageNet and then on Oxford102, were trained and applied on Plant Classification. The results show that although Oxford102 is more related to plants classification, the size and the rich diversity of ImageNet are advantageous for accurate classification.

This Project was created with Python, TensorFlow, Keras, OpenCV and more libraries.

## Project Research
In order to understand the steps and what we did you are welcome to look at the [Project Book]().

## Project Setup and Run
In order to run this project your environment needs to support TensorFlow and all the other dependencies.

### Dependencies of env:
For this project we use **python 3.9.4**,  
make sure you also follow the requirements.txt

### Run on local environment:

<ol>
  <li>Clone this repository.</li>
  <li>Open cmd/shell/terminal and go to application folder: cd PlantClassification/app</li>
  <li>Run the main.py</li>
  <li>Open this link: http://127.0.0.1:5000/</li>
  <li>Enjoy the application.</li>
</ol>

