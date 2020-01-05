# pix2pix

#### Title
[Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)

#### Abstract
We investigate conditional adversarial networks as a general-purpose solution to image-to-image translation problems. These networks not only learn the mapping from input image to output image, but also learn a loss function to train this mapping. This makes it possible to apply the same generic approach to problems that traditionally would require very different loss formulations. We demonstrate that this approach is effective at synthesizing photos from label maps, reconstructing objects from edge maps, and colorizing images, among other tasks. Indeed, since the release of the pix2pix software associated with this paper, a large number of internet users (many of them artists) have posted their own experiments with our system, further demonstrating its wide applicability and ease of adoption without the need for parameter tweaking. As a community, we no longer hand-engineer our mapping functions, and this work suggests we can achieve reasonable results without hand-engineering our loss functions either.

## Result
![alt text](./img/generated_images.png "Generated Images by pix2pix")

    1. 1st row: Input-segmentation
    2. 2nd row: label-photo
    3. 3rd row: result-pix2pix

* The results are generated by trained network using **facades** dataset during **200 epochs**.

## Train
    $ python main.py --mode train --scope [scope name]

* Set **[scope name]** uniquely.


## Test
    $ python main.py --mode test --scope [scope name]

* Set **[scope name]** to test using scoped network
* In **result** folder, generated images are saved under the **images** subfolder.
* In addition, **index.html** is created to illustrate the generated images.  


## Tensorboard
    $ tensorboard --logdir log/[scope] --port [(optional) 4 digit port number]

Then, click **http://localhost:6006**

* You can change **[(optional) 4 digit port number]**
* 4 digit port number = 6006 (default)
