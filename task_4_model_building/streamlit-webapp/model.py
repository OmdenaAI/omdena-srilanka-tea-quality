# Import libraries
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.models import Sequential
from keras.layers import Dropout, Dense
from keras.optimizers import Adam

# build fresh model
def fresh_model():
    model = Sequential()
    model.add(VGG16(weights = "imagenet", include_top=False, pooling = 'avg'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(units=3, activation='softmax'))
    adam_opt = Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-5)
    
    model.layers[0].trainable = True
    model.load_weights('/home/busayor/Shiii/Omdena/Sri-Lanka/web-app/VGG16-tea-fresh-Weights(v1).h5')
    return model

# build withered model
def withered_model():

    adam_opt = Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-5)
    model = Sequential()
    
    model.add(VGG19(weights = "/home/busayor/Shiii/Omdena/Sri-Lanka/web-app/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5", include_top=False, pooling = 'avg'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(units=3, activation='softmax'))
    
    model.layers[0].trainable = True
    model.load_weights('/home/busayor/Shiii/Omdena/Sri-Lanka/web-app/VGG19-tea-Withered-model(v1).h5')
    return model