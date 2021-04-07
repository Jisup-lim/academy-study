import tensorflow as tf
import os
import time
from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout, ReLU, concatenate, ZeroPadding2D
from tensorflow.keras.layers import BatchNormalization, Activation, LeakyReLU, UpSampling2D, Conv2D, Conv2DTranspose
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing import image
from IPython import display
import cv2 


# _URL = 'https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/facades.tar.gz'

# path_to_zip = tf.keras.utils.get_file('facades.tar.gz',
#                                       origin=_URL,
#                                       extract=True)

# PATH = os.path.join(os.path.dirname(path_to_zip), 'facades/')

# BUFFER_SIZE = 400
# BATCH_SIZE = 1
# IMG_WIDTH = 256
# IMG_HEIGHT = 256 

# def load(image_file):
#     image = tf.io.read_file(image_file)
#     image = tf.image.decode_jpeg(image)

#     w = tf.shape(image)[1]

#     w = w // 2
#     real_image = image[:, :w, :]
#     input_image = image[:, w:, :]

#     input_image = tf.cast(input_image, tf.float32)
#     real_image = tf.cast(real_image, tf.float32)

#     return input_image, real_image


# inp, re = load(PATH+'train/100.jpg')
# # casting to int for matplotlib to show the image
# plt.figure()
# plt.imshow(inp/255.0)
# plt.figure()
# plt.imshow(re/255.0)

# def resize(input_image, real_image, height, width):
#     input_image = tf.image.resize(input_image, [height, width],
#                                 method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
#     real_image = tf.image.resize(real_image, [height, width],
#                                method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

#     return input_image, real_image

# def random_crop(input_image, real_image):
#   stacked_image = tf.stack([input_image, real_image], axis=0)
#   cropped_image = tf.image.random_crop(
#   stacked_image, size=[2, IMG_HEIGHT, IMG_WIDTH, 3])

#   return cropped_image[0], cropped_image[1]

# # normalizing the images to [-1, 1]

# def normalize(input_image, real_image):
#   input_image = (input_image / 127.5) - 1
#   real_image = (real_image / 127.5) - 1

#   return input_image, real_image

# @tf.function()
# def random_jitter(input_image, real_image):
#   # resizing to 286 x 286 x 3
#   input_image, real_image = resize(input_image, real_image, 286, 286)

#   # randomly cropping to 256 x 256 x 3
#   input_image, real_image = random_crop(input_image, real_image)

#   if tf.random.uniform(()) > 0.5:
#     # random mirroring
#     input_image = tf.image.flip_left_right(input_image)
#     real_image = tf.image.flip_left_right(real_image)

#   return input_image, real_image


# plt.figure(figsize=(6, 6))
# for i in range(4):
#   rj_inp, rj_re = random_jitter(inp, re)
#   plt.subplot(2, 2, i+1)
#   plt.imshow(rj_inp/255.0)
#   plt.axis('off')
# plt.show()

# def load_image_train(image_file):
#   input_image, real_image = load(image_file)
#   input_image, real_image = random_jitter(input_image, real_image)
#   input_image, real_image = normalize(input_image, real_image)

#   return input_image, real_image

# def load_image_test(image_file):
#   input_image, real_image = load(image_file)
#   input_image, real_image = resize(input_image, real_image,
#                                    IMG_HEIGHT, IMG_WIDTH)
#   input_image, real_image = normalize(input_image, real_image)

#   return input_image, real_image

# train_dataset = tf.data.Dataset.list_files(PATH+'train/*.jpg')
# train_dataset = train_dataset.map(load_image_train,
#                                   num_parallel_calls=tf.data.experimental.AUTOTUNE)
# train_dataset = train_dataset.shuffle(BUFFER_SIZE)
# train_dataset = train_dataset.batch(BATCH_SIZE, drop_remainder=True)

# test_dataset = tf.data.Dataset.list_files(PATH+'test/*.jpg')
# test_dataset = test_dataset.map(load_image_test)
# test_dataset = test_dataset.batch(BATCH_SIZE, drop_remainder=True)

# print(train_dataset)
# print(test_dataset)


PATH = 'D:/01_data/'

def load_xy():
    input_image_path = PATH + 'padding_img/'
    target_image_path = PATH + 'resize_img/'
    
    for i in range(30):
        if i==0:
            input_image = cv2.imread(input_image_path+'{}.jpg'.format(str(i)))
            target_image = cv2.imread(target_image_path+'{}.jpg'.format(str(i)))
            input_images = input_image.reshape(1,input_image.shape[0],input_image.shape[1],3)
            target_images = target_image.reshape(1,target_image.shape[0],target_image.shape[1],3)
        else:
            try:
                input_image = cv2.imread(input_image_path+'{}.jpg'.format(str(i)))
                target_image = cv2.imread(target_image_path+'{}.jpg'.format(str(i)))
                input_image = input_image.reshape(1,input_image.shape[0],input_image.shape[1],3)
                target_image = target_image.reshape(1,target_image.shape[0],target_image.shape[1],3)
                input_images = np.concatenate([input_images,input_image])
                target_images = np.concatenate([target_images,target_image])
            except:
                continue
    
    return input_images,target_images

# normalizing the images to [-1, 1]

def normalize(input_image, target_image):
    # 전처리
    for i in range(len(input_image)):
        if i==0:
            input_images = (input_image[i]/ 127.5) - 1
            target_images = (target_image[i]/ 127.5) - 1
            input_images,target_images = input_images.reshape(1,input_images.shape[0],input_images.shape[1],3),target_images.reshape(1,target_images.shape[0],target_images.shape[1],3)
        
        else:
            temp_1 = input_image[i].reshape(1,input_image.shape[1],input_image.shape[2],3)/127.5 - 1
            temp_2 = target_image[i].reshape(1,target_image.shape[1],target_image.shape[2],3)/127.5 - 1
            input_images = np.concatenate([input_images,temp_1])
            target_images = np.concatenate([target_images,temp_2])

    return input_images, target_images

input_images, target_images = load_xy()
print(input_images.shape, target_images.shape)
input_images, target_images = normalize(input_images, target_images)

inputs = Input(shape=[256,256,3])
down_stack0 = Conv2D(64, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(inputs)# (bs, 128, 128, 64)
down_stack1 = Conv2D(128, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack0)# (bs, 128, 128, 64)
down_stack2 = BatchNormalization()(down_stack1)
down_stack3 = LeakyReLU()(down_stack2)
down_stack4 = Conv2D(256, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack3)
down_stack5 = BatchNormalization()(down_stack4)
down_stack6 = LeakyReLU()(down_stack5)
down_stack7 = Conv2D(512, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack6)
down_stack8 = BatchNormalization()(down_stack7)
down_stack9 = LeakyReLU()(down_stack8)
down_stack10 = Conv2D(512, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack9)
down_stack11 = BatchNormalization()(down_stack10)
down_stack12 = LeakyReLU()(down_stack11)
down_stack13 = Conv2D(512, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack12)
down_stack14 = BatchNormalization()(down_stack13)
down_stack15 = LeakyReLU()(down_stack14)
down_stack16 = Conv2D(512, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack15)
down_stack17 = BatchNormalization()(down_stack16)
down_stack18 = LeakyReLU()(down_stack17)
down_stack19 = Conv2D(512, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(down_stack18)
down_stack20 = BatchNormalization()(down_stack19)
down_stack21 = LeakyReLU()(down_stack20)

up_stack1 = Conv2DTranspose(512, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(down_stack21)
up_stack2 = Dropout(0.5)(up_stack1)
up_stack3 = ReLU()(up_stack2)
merge1 = concatenate([down_stack18, up_stack3])
up_stack4 = Conv2DTranspose(512, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge1)
up_stack5 = Dropout(0.5)(up_stack4)
up_stack6 = ReLU()(up_stack5)
merge2 = concatenate([down_stack15, up_stack6])
up_stack7 = Conv2DTranspose(512, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge2)
up_stack8 = Dropout(0.5)(up_stack7)
up_stack9 = ReLU()(up_stack8)
merge3 = concatenate([down_stack12, up_stack9])
up_stack10 = Conv2DTranspose(512, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge3)
merge4 = concatenate([down_stack9, up_stack10])
up_stack11 = Conv2DTranspose(256, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge4)
merge5 = concatenate([down_stack6, up_stack11]) 
up_stack12 = Conv2DTranspose(128, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge5)
merge6 = concatenate([down_stack3, up_stack12])
up_stack13 = Conv2DTranspose(64, 4, strides=2,padding='same',kernel_initializer= tf.random_normal_initializer(0., 0.02),use_bias=False)(merge6)
merge7 = concatenate([down_stack0, up_stack13])
g_out_put = Conv2DTranspose(3, 4,strides=2,padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02),activation='tanh')(merge7) # (bs, 256, 256, 3)

generator = Model(inputs = inputs, outputs = g_out_put)
generator.summary()

inp = Input(shape=[256,256,3], name='input_image')
tar = Input(shape=[256, 256, 3], name='target_image')

merge1 = concatenate([inp, tar])# (bs, 256, 256, channels*2)
discriminator1 = Conv2D(64, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(merge1)
discriminator2 = Conv2D(128, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(discriminator1)
discriminator3 = BatchNormalization()(discriminator2)
discriminator4 = LeakyReLU()(discriminator3)
discriminator5 = Conv2D(256, 4, strides=2, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(discriminator4)
discriminator6 = BatchNormalization()(discriminator5)
discriminator7 = LeakyReLU()(discriminator6)
discriminator8 = ZeroPadding2D()(discriminator7)
discriminator9 = Conv2D(512, 4, strides=1, padding='same',kernel_initializer=tf.random_normal_initializer(0., 0.02), use_bias=False)(discriminator8)
discriminator10 = BatchNormalization()(discriminator9)
discriminator11 = LeakyReLU()(discriminator10)
discriminator12 = ZeroPadding2D()(discriminator11)
d_out_put = Conv2D(1, 4, strides=1,kernel_initializer=tf.random_normal_initializer(0., 0.02),activation='sigmoid')(discriminator12)

discriminator = Model(inputs = [inp, tar], outputs = d_out_put)

discriminator.compile(loss = 'binary_crossentropy', optimizer=Adam(learning_rate=0.0002,beta_1=0.5))
discriminator.trainable = False
discriminator.summary()

# dis_output = discriminator([generator([input_images, target_images]),target_images])
# gen_in = generator([input_images, target_images])
dis_output = [discriminator([generator(target_images),target_images]), generator(target_images)]
gen_in = [input_images, target_images]
gan = Model(gen_in, dis_output)
gan.compile(loss=['binary_crossentropy','mae'], optimizer=Adam(learning_rate=0.0002,beta_1=0.5))
gan.summary()

accuracies = []
losses = []


def train(epochs, batch_size, sample_interval):


    # Labels for real images: all ones
    real = np.ones((1,)+(int(256/2**4),int(256/2**4),1))

    # Labels for fake images: all zeros
    fake = np.zeros((1,)+(int(256/2**4),int(256/2**4),1))

    for epochs in range(epochs):

        # -------------------------
        #  Train the Discriminator
        # -------------------------

        # Get a random batch of real images and their labels
        idx = np.random.randint(0, (len(input_images))-1)
        imgsA = input_images[idx : (idx + 1)]
        imgsB = input_images[idx : (idx + 1)]
        
        imgs1 = np.delete(imgsA, range(idx,(idx+1)),0)
        imgs2 = np.delete(imgsB, range(idx,(idx+1)),0)
        
        batchA = imgsA.reshape(1,256,256,3)
        batchB = imgsB.reshape(1,256,256,3)

        tars = target_images[idx : (idx+1)]

        # Generate a batch of fake images
        gen_imgs = generator.predict(batchB)

        # Train the Discriminator
        d_loss_real = discriminator.train_on_batch([batchA, batchB], real) [0]
        d_loss_fake = discriminator.train_on_batch([gen_imgs, batchB], fake) [0]
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # ---------------------
        #  Train the Generator
        # ---------------------

        # Train the Generator
        g_loss = gan.train_on_batch([batchA, batchB], [real, batchA])

        if (epochs + 1) % sample_interval == 0:

            # Output training progress
            print("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" %
                  (epochs + 1, d_loss[0], 100 * d_loss[1], g_loss))

            # Save losses and accuracies so they can be plotted after training
            losses.append((d_loss[0], g_loss))
            accuracies.append(100 * d_loss[1])

            # Output sample of generated images
            sample_images()

def sample_images(image_grid_rows=2, image_grid_columns=5):
    
    # Sample random noise
    z = np.random.normal(0, 1, (image_grid_rows * image_grid_columns, z_dim))

    # Get image labels 0-9
    labels = np.arange(0, 10).reshape(-1, 1)

    # Generate images from random noise
    gen_imgs = generator.predict([z, labels])

    # Rescale image pixel values to [0, 1]
    gen_imgs = 0.5 * gen_imgs + 0.5

    # Set image grid
    fig, axs = plt.subplots(image_grid_rows,
                            image_grid_columns,
                            figsize=(10, 4),
                            sharey=True,
                            sharex=True)

    cnt = 0
    for i in range(image_grid_rows):
        for j in range(image_grid_columns):
            # Output a grid of images
            axs[i, j].imshow(gen_imgs[cnt, :, :, 0], cmap='gray')
            axs[i, j].axis('off')
            axs[i, j].set_title("Digit: %d" % labels[cnt])
            cnt += 1

# Set hyperparameters
epochs = 12000
batch_size = 32
sample_interval = 1000

train(epochs, batch_size, sample_interval)

loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def generator_loss(disc_generated_output, gen_output, target):
  gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)

  # mean absolute error
  l1_loss = tf.reduce_mean(tf.abs(target - gen_output))

  total_gen_loss = gan_loss + (100 * l1_loss)

  return total_gen_loss, gan_loss, l1_loss

def discriminator_loss(disc_real_output, disc_generated_output):
  real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)

  generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)

  total_disc_loss = real_loss + generated_loss

  return total_disc_loss

# def generate_images(model, test_input, tar):
#   prediction = model(test_input, training=True)
#   plt.figure(figsize=(15,15))

#   display_list = [test_input[0], tar[0], prediction[0]]
#   title = ['Input Image', 'Ground Truth', 'Predicted Image']

#   fig, axs = plt.subplots(5, 5)

#   for i in range(3):
#     plt.subplot(1, 3, i+1)
#     plt.title(title[i])
#     # # getting the pixel values between [0, 1] to plot it.
#     gen_imgs = display_list[i] * 0.5 + 0.5
#     plt.imshow(gen_imgs)
#     # plt.axis('off')
#     for j in range(3):
#             # 이미지 그리드 출력
#             axs[i, j].imshow(gen_imgs[cnt, :, :, ])
#             axs[i, j].axis('off')
#   count = count + 1
#   fig.savefig("D:/gain/gan_" + str(count) + ".png" )
#   # plt.show()


# for example_input, example_target in test_dataset.take(1):
#   generate_images(generator, example_input, example_target)

# EPOCHS = 5000

# import datetime
# log_dir="logs/"

# summary_writer = tf.summary.create_file_writer(
#   log_dir + "fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

# @tf.function
# def train_step(input_image, target, epoch):
#   with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
#     gen_output = generator(input_image, training=True)

#     disc_real_output = discriminator([input_image, target], training=True)
#     disc_generated_output = discriminator([input_image, gen_output], training=True)

#     gen_total_loss, gen_gan_loss, gen_l1_loss = generator_loss(disc_generated_output, gen_output, target)
#     disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

#   generator_gradients = gen_tape.gradient(gen_total_loss,
#                                           generator.trainable_variables)
#   discriminator_gradients = disc_tape.gradient(disc_loss,
#                                                discriminator.trainable_variables)

#   generator_optimizer.apply_gradients(zip(generator_gradients,
#                                           generator.trainable_variables))
#   discriminator_optimizer.apply_gradients(zip(discriminator_gradients,
#                                               discriminator.trainable_variables))

#   with summary_writer.as_default():
#     tf.summary.scalar('gen_total_loss', gen_total_loss, step=epoch)
#     tf.summary.scalar('gen_gan_loss', gen_gan_loss, step=epoch)
#     tf.summary.scalar('gen_l1_loss', gen_l1_loss, step=epoch)
#     tf.summary.scalar('disc_loss', disc_loss, step=epoch)


# def fit(train_ds, epochs, test_ds):
#     for epoch in range(epochs):
#         start = time.time()

#         display.clear_output(wait=True)

#         for example_input, example_target in test_ds.take(1):
#             generate_images(generator, example_input, example_target)
#         print("Epoch: ", epoch)

#         # Train
#         for n, (input_image, target) in train_ds.enumerate():
#             print('.', end='')
#             if (n+1) % 100 == 0:
#                 print()
#             train_step(input_image, target, epoch)
#         print()

#         # saving (checkpoint) the model every 20 epochs
#         if (epoch + 1) % 20 == 0:
#             checkpoint.save(file_prefix = checkpoint_prefix)

#         print ('Time taken for epoch {} is {} sec\n'.format(epoch + 1,
#                                                             time.time()-start))
#     checkpoint.save(file_prefix = checkpoint_prefix)

# fit(input_images, EPOCHS, test_dataset)