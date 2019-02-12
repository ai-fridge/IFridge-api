import base64
import re
import uuid
import os
import logging

import face_recognition
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(['POST'])
def verify_face_recognition(request):
    if request.method == 'POST':
        data = request.data

        if is_base64_image(data['file']):
            b64_string = is_base64_image(data['file'])
        else:
            return Response({"error": "base64 image format is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        dirname = 'upload/face_recognition/'
        filename = str(uuid.uuid1()) + '.jpg'

        if not os.path.exists(dirname):
            create_dir_folder(dirname)

        image_name = convert_and_save(b64_string, dirname, filename)

        return detect_faces_in_image(image_name)


# TODO::waiting for integrating with mysql, matching the encoding from DB
def detect_faces_in_image(file_stream):
    name = 'unknown'
    known_face_names = [
        # "ren",
        "eder",
        # "amber"
    ]
    # Pre-calculated face encoding of face generated with face_recognition.face_encodings(img)
    # will fetch encoding from database
    known_face_encoding = [-1.77358408e-02, 9.67688113e-02, -4.89827618e-02, -7.35863745e-02,
                            -1.88230380e-01,  2.65576318e-02, -7.53998756e-05, -1.10178672e-01,
                            1.75862163e-01, -1.29476085e-01,  2.27695793e-01, -3.79926823e-02,
                            -2.58648515e-01, -1.93849280e-02, -8.37646127e-02,  1.64393917e-01,
                            -1.58211350e-01, -1.38035819e-01, -5.56099415e-02, -3.39336693e-05,
                            3.04973945e-02,  3.78315449e-02, -6.05039150e-02,  6.46504238e-02,
                            -9.02237073e-02, -2.96050906e-01, -7.43663907e-02, -7.06249997e-02,
                            5.61024062e-02, -7.02097341e-02, -2.30524074e-02,  9.14832950e-02,
                            -1.04952872e-01, -1.37530360e-02,  4.44991104e-02, -2.09207460e-02,
                            -4.87841628e-02, -6.01644143e-02,  2.34680623e-01,  4.95870747e-02,
                            -2.98882335e-01,  1.45597653e-02,  7.75221363e-02,  2.37353519e-01,
                            1.24703519e-01,  2.17206888e-02,  8.33039358e-03, -1.64922357e-01,
                            1.58199236e-01, -1.40282884e-01,  1.62452031e-02,  1.57956168e-01,
                            1.32955328e-01,  2.48773172e-02, -2.56301593e-02, -1.47200450e-01,
                            -1.23191327e-02,  1.05455667e-01, -1.86661974e-01,  1.53097995e-02,
                            8.08515623e-02, -8.56958479e-02, -4.40116711e-02, -8.61731693e-02,
                            2.11846873e-01,  4.54880446e-02, -1.23828895e-01, -1.66817650e-01,
                            1.86105654e-01, -1.91672489e-01, -1.32878736e-01,  7.16022030e-02,
                            -1.04251489e-01, -1.70452997e-01, -2.47299895e-01,  1.19198393e-02,
                            4.24209595e-01,  1.13241673e-01, -1.34031624e-01,  4.75920290e-02,
                            -1.68776028e-02, -8.93306285e-02,  1.04007408e-01,  1.88026562e-01,
                            -6.58218712e-02, -4.64066863e-02, -3.15672792e-02, -2.33672000e-02,
                            2.63520569e-01, -6.89241812e-02, -1.19860228e-02,  2.23205015e-01,
                            2.50756051e-02,  9.80346724e-02, -3.51974089e-03,  2.28089988e-02,
                            -8.76517743e-02,  3.76223177e-02, -7.26981908e-02, -5.08186407e-04,
                            2.24310309e-02, -6.43566698e-02,  1.57502256e-02,  1.18910640e-01,
                            -1.62456423e-01,  1.53269425e-01,  2.08797622e-02,  1.87477972e-02,
                            5.62761314e-02,  2.49780640e-02, -7.60575682e-02, -8.59230980e-02,
                            1.48817748e-01, -2.11746782e-01,  2.02927351e-01,  1.01261444e-01,
                            1.09727681e-01,  8.28519911e-02,  1.46399364e-01,  4.49204221e-02,
                            3.95170897e-02, -6.78628907e-02, -2.33617261e-01, -5.87060861e-02,
                            1.44976929e-01, -1.25408739e-01,  8.16230774e-02, -2.22558025e-02]
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    # app.logger.info(unknown_face_encodings)
    face_found = False
    is_authentication = False

    if len(unknown_face_encodings) > 0:
        face_found = True

        # See if the first face in the uploaded image matches the known face of the database
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0], tolerance=0.5)
        # match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0], tolerance=0.45)
        if match_results[0]:
            is_authentication = True
            name = known_face_names[0]

    # Return the result as json
    result = {
        "is_face_found": face_found,
        "is_authentication": is_authentication,
        "name": name
    }

    return Response(result)


def convert_and_save(b64_string, dirname, filename):
    if filename is None:
        logger.warning('Filename cannot be null')
        return False

    if dirname is None:
        dirname = 'upload/tmp/'

    image_name = dirname + filename
    with open(image_name, "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
        return image_name


def create_dir_folder(dirname):
    try:
        # Create target Directory
        os.makedirs(dirname)
        logger.info("Directory ", dirname,  " Created ")
    except FileExistsError:
        logger.info("Directory ", dirname,  " already exists")


def is_base64_image(base64_string):
    if 'data:image' not in base64_string:
        logger.warning('it is not image.')
        return False
    elif 'base64' not in base64_string:
        logger.warning('it is not base64.')
        return False

    return re.sub('^data:image/.+;base64,', '', base64_string)
