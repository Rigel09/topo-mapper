import numpy as np


def lla2mercxya(lla: np.ndarray, in_degrees: bool = True) -> np.ndarray:
    """
    Converts latitude longitude altitude to a mercator projection

    Reference: https://wiki.openstreetmap.org/wiki/Mercator

    Args:
        lla (np.ndarray): array of shape (N, 3) columns are lat, long, alt
        in_degrees (bool, optional): True if lat an long are in degrees. Defaults to True.

    Returns:
        np.ndarray: returns a mercator projection of the input lla in the shape of (N, 3).
                    Columns are X, Y, altitude. N is the number of points
    """
    xya = np.ones(lla.shape)
    xya[:, 2] = lla[:, 2]

    earth_radius_m = 6378137.0

    if in_degrees:
        lla[:, 0] = np.deg2rad(lla[:, 0])
        lla[:, 1] = np.deg2rad(lla[:, 1])

    xya[:, 0] = earth_radius_m * lla[:, 1]

    xya[:, 1] = np.log(np.tan(lla[:, 0] / 2 + np.pi / 4)) * earth_radius_m

    return xya
