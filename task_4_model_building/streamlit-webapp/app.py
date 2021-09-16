# import libraries
import streamlit as st
from model import fresh_model, withered_model
from PIL import Image
from detector import annotate_leaves, predict_leaves, get_leaves
import subprocess
from pathlib import Path
import atexit



# page icon
st.set_page_config(page_title='Tea-Leaves Classification', page_icon='🌿')

st.set_option('deprecation.showfileUploaderEncoding', False)

# Pull and connect deepstack custom api port to detection model
@st.cache
def pull_image():
    subprocess.run(['docker', 'run', '-d', '--name', 'leaf-detector', '-v', Path(__file__).resolve().parent / 'detector:/modelstore/detection', '-p', '80:5000', 'deepquestai/deepstack'])

# Stop and delect docker container after script is terminated
@atexit.register
def stop_docker_image():
    subprocess.run(['docker', 'stop', 'leaf-detector'])
    subprocess.run(['docker', 'rm', 'leaf-detector'])

# Instatiates neccessary model
@st.cache(allow_output_mutation=True)
def load_fresh_model():
    model_fresh = fresh_model()
    return model_fresh

@st.cache(allow_output_mutation=True)
def load_withered_model():
    model_withered = withered_model()
    return model_withered

pull_image()
fresh_model = load_fresh_model()
withered_model = load_withered_model()





def main():

    """Tea-Leaf Classification"""

    st.title('Tea-Leaf Classification')
    st.write('*Classify tea leaves based on region and category*')

    # select leaf category
    categories = ['Fresh', 'Withered']
    choice = st.sidebar.selectbox('Select Category', categories)

    if choice == 'Fresh':
        
        # input image
        file = st.file_uploader("Please upload tea-leaf image", type=['jpg', 'png', 'jpeg'])

        if file is None:
            st.text('Please upload an image file')
        else:
            # read input image
            image = Image.open(file)
            # get detections
            response, num_leaves = get_leaves(image=file)
            st.info(f'Number of Tea-Leaves found:   {num_leaves}')
            if num_leaves > 0:
                # annotate leaves
                annotated_img = annotate_leaves(image=image, response=response)
                st.image(annotated_img, use_column_width=True)
                if st.button('Predict'):
                    # get classifications
                    annotated_img = predict_leaves(image=image, response=response, model=fresh_model)
                    st.image(annotated_img, use_column_width=True)
                

    elif choice == 'Withered':

        # input image
        file = st.file_uploader("Please upload tea-leaf image", type=['jpg', 'png', 'jpeg'])

        if file is None:
            st.text('Please upload an image file')
        else:
            # read input image
            image = Image.open(file)
            # get detections
            response, num_leaves = get_leaves(image=file)
            st.info(f'Number of Tea-Leaves found:   {num_leaves}')
            if num_leaves > 0:
                # annotate leaves
                annotated_img = annotate_leaves(image=image, response=response)
                st.image(annotated_img, use_column_width=True)
                if st.button('Predict'):
                    # get classifications
                    annotated_img = predict_leaves(image=image, response=response, model=withered_model)
                    st.image(annotated_img, use_column_width=True)



if __name__ == '__main__':
    main()