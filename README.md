# dot_matrix_img
Just a simple python notenook (and a python command line script) to convert an image into a svg img made up dots.<br> As the name suggest this project was inspired by dot matrix pattern of ink printing. Though this version only creates a greyscale image.

### How to use
* Open this notebook in Google Colab OR clone this repo and install requirements `pip install numpy opencv-python`. (I prefer google colab method)
    * If, on google colab upload your image the compute instance from the side pane
* Set the image file location in `img_path`
* `rows` is the height of the resultant svg (not pixel height, just the number of column of dots.)
* `depth` is the different and distinct radii dots can have. (Basically different level of greyscale values)