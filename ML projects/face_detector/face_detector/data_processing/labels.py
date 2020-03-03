import pandas as pd


def get_face_center_coordinates(root_dir, images_dir, face_center_cordinates_filename):
    """
    Function get face center coordinates from file.

    :param str root_dir - images main directory name.
    :param str images_dir - subdir inside main dir containing images
    :param str face_center_cordinates_filename - name of face_center_cordinates_filename file
    :return
        x -  width point of face center
        y -  height point of face center
    """
    face_center = pd.read_csv(
        root_dir + "/" + images_dir + "/" + face_center_cordinates_filename,
        sep=" ",
        header=None,
        dtype="float64",
        names=["x", "y", "z", "none"],
    ).iloc[3, :3]

    face_center_rgb = pd.read_csv(
        root_dir + "/" + images_dir + "/rgb.cal",
        sep=" ",
        header=None,
        error_bad_lines=False,
        warn_bad_lines=False,
        dtype="float64",
    )

    moved_x = face_center["x"] + face_center_rgb.iloc[6, 0]
    moved_y = face_center["y"] + face_center_rgb.iloc[6, 1]

    x_result = (
        moved_x * face_center_rgb.iloc[0, 0] / face_center["z"]
        + face_center_rgb.iloc[0, 2]
    )
    y_result = (
        moved_y * face_center_rgb.iloc[1, 1] / face_center["z"]
        + face_center_rgb.iloc[1, 2]
    )

    return x_result, y_result
