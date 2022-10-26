import os
import cv2
import streamlit as st
import albumentations as A

from utils import (
    load_augmentations_config,
    get_arguments,
    get_placeholder_params,
    select_transformations,
    show_random_params,
)
from visuals import (
    select_image,
    # show_credentials,
    show_docstring,
    get_transormations_params,
)


def main():
    # get CLI params: the path to images and image width
    path_to_images, width_original = get_arguments()
    if not os.path.isdir(path_to_images):
        st.title("There is no directory: " + path_to_images)
    else:
        # select interface type
        interface_type = st.sidebar.radio(
            "Select the interface mode", ["Simple", "Professional"]
        )
        
        # select image
        status, image = select_image(path_to_images, interface_type)
        Bbox =  st.sidebar.checkbox('Apply bounding box')
        if Bbox:
            h = int(st.sidebar.number_input('Height'))
            w = int(st.sidebar.number_input('Width'))
            x = int(st.sidebar.number_input('X-coordinate'))
            y = int(st.sidebar. number_input('Y-coordinate'))
            annotated_image = image.copy()
            if h != None and w != None and x != None and y != None:
                annotated_image = cv2.rectangle(annotated_image, (x, y), (x+w, y+h),(0,255,0),-10   )
        zoom = st.sidebar.radio(
            "Select the interface mode", ["Zoom in", "Zoom out", "none"]
        )

        if zoom == "Zoom in":
                    value = st.sidebar.slider('How much do you want to zoom ? ', 0, 1000, 5)
                    width_original=width_original - value
        elif zoom == "Zoom out":
                    value = st.sidebar.slider('How much do you want to zoom ? ', 0, 1000, 5)
                    width_original=width_original +value
        if status == 1:
            st.title("Can't load image")
        if status == 2:
            st.title("Please, upload the image")
        else:
            # image was loaded successfully
            placeholder_params = get_placeholder_params(image)

            # load the config
            augmentations = load_augmentations_config(
                placeholder_params, "configs/augmentations.json"
            )

            # get the list of transformations names
            transform_names = select_transformations(augmentations, interface_type)

            # get parameters for each transform
            transforms = get_transormations_params(transform_names, augmentations)

            try:
                # apply the transformation to the image
                if Bbox:
                    data = A.ReplayCompose(transforms)(image=annotated_image)
                else:
                    data = A.ReplayCompose(transforms)(image=image)
                error = 0
            except ValueError:
                error = 1
                st.title(
                    "The error has occurred. Most probably you have passed wrong set of parameters. \
                Check transforms that change the shape of image."
                )

            # proceed only if everything is ok
            if error == 0:
                augmented_image = data["image"]
                # show title
                st.title("Demo of Albumentations")

                # show the images
                width_transformed = int(
                    width_original / image.shape[1] * augmented_image.shape[1]
                )
                

                st.image(image, caption="Original image", width=width_original)
                st.image(
                    augmented_image,
                    caption="Transformed image",
                    width=width_transformed,
                )

                # comment about refreshing
                st.write("*Press 'R' to refresh*")

                # random values used to get transformations
                show_random_params(data, interface_type)

                # print additional info
                for transform in transforms:
                    show_docstring(transform)
                    st.code(str(transform))
                # show_credentials()

                # adding google analytics pixel
                # only when deployed online. don't collect statistics of local usage
                if "GA" in os.environ:
                    st.image(os.environ["GA"])
                    st.markdown(
                        (
                            # "[Privacy policy]"
                            # + (
                            #     "(https://htmlpreview.github.io/?"
                            #     + "https://github.com/IliaLarchenko/"
                            #     + "albumentations-demo/blob/deploy/docs/privacy.html)"
                            # )
                        )
                    )


if __name__ == "__main__":
    main()
