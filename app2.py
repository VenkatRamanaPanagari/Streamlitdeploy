
import streamlit as st
import PIL
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
def app():
    model_url = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_north_america_V1/1'
    labels = "landmarks_classifier_north_america_V1_label_map.csv"

    df = pd.read_csv(labels)
    labels = dict(zip(df.id, df.name))

    st.title("Landmark Recognition")
    img = PIL.Image.open("logo.jpg")
    img = img.resize((600,300))
    st.image(img)

    img_file = st.file_uploader("Choose your Image", type=['png', 'jpg'])


    def image_processing(img):
        img_shape = (321, 321)
        classifier = tf.keras.Sequential([hub.KerasLayer(model_url, input_shape=img_shape + (3,), output_key="predictions:logits")])
        img = PIL.Image.open(img_file)
        img = img.resize(img_shape)
        img1 = img
        img = np.array(img) / 255.0
        img = img[np.newaxis]
        result = classifier.predict(img)
        return labels[np.argmax(result)],img1


    def get_map(img1):
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(img1)
        return location.address,location.latitude, location.longitude


    def run():
        #img_file = st.file_uploader("Choose your Image", type=['png', 'jpg'])
        if img_file is not None:
            save_image_path = img_file.name
            with open(save_image_path, "wb") as f:
                f.write(img_file.getbuffer())
            prediction,image = image_processing(save_image_path)
            st.image(image)
            st.header("📍 **Predicted Landmark is: " + prediction + '**')
            try:
                address, latitude, longitude = get_map(prediction)
                st.success('Address: '+address )
                loc_dict = {'Latitude':latitude,'Longitude':longitude}
                st.subheader('✅ **Latitude & Longitude of '+prediction+'**')
                st.json(loc_dict)
                data = [[latitude,longitude]]
                df = pd.DataFrame(data, columns=['lat', 'lon'])
                st.subheader('✅ **'+prediction +' on the Map**'+'🗺️')
                st.map(df)
            except Exception as e:
                st.warning("No address found!!")

    run()
