
# Random Augmentation
[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/Wook-2/RandomAugmentation)

This project is deploying web demo of ***[IMGAUG]([https://github.com/aleju/imgaug](https://github.com/aleju/imgaug))***  *[option: Random augment]* for who want to augment images easily.

## Description

Random Augmentation helps you with augmenting images for your machine learning projects.
It converts a set of input images into a new, much larger set of slightly altered images.
<img  src="https://github.com/Wook-2/RandomAugmentation/blob/master/static/example_git.png?raw=true"  style="width: 100%"></img>

## Features
- Mix many augmentation techniques.
- affine transformations, gausian noise, dropout, blurring, contrast changes, cropping/padding, ...
- Optimized for high performance.
- Easy to use.
## Run on your Local
#### Using Docker

    $ git clone https://github.com/Wook-2/RandomAugmentation.git
    
    $ cd RandomAugmentation
    
    $ docker build -t {your_image_name} .
    
    $ docker run -it --rm -p 8000:8000 {your_image_name}
then visit : *[localhost:8000](https://localhost:8000)*
#### Using Curl

    $ curl -X POST "https://master-random-augmentation-wook-2.endpoint.ainize.ai/augment" \
    -H "accept: application/octet-stream" -H "Content-Type: multipart/form-data" \
    -F "file=@{your_image_path};type=image/jpeg" \
    -F "number={numbers of augmented images}" -o {output_file_name}.zip
Fill in {your_image_path, numbers of augmented images, output_file_name} to suit your situation.

## REFERENCE

- `IMGAUG` : *[https://github.com/aleju/imgaug](https://github.com/aleju/imgaug)*

- `Ainize` : *[https://ainize.ai/](https://ainize.ai/)*
