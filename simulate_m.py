import numpy as np
from daltonlens.simulate import Deficiency, convert
import matplotlib.pyplot as plt

def rgb_to_lms() -> np.ndarray:
    """
    Matrix for RGB color-space to LMS color-space transformation.
    """
    return np.array([[17.8824, 43.5161, 4.11935],
                        [3.45565, 27.1554, 3.86714],
                        [0.0299566, 0.184309, 1.46709]]).T


def lms_to_rgb() -> np.ndarray:
    """
    Matrix for LMS colorspace to RGB colorspace transformation.
    """
    return np.array([[0.0809, -0.1305, 0.1167],
                        [-0.0102, 0.0540, -0.1136],
                        [-0.0004, -0.0041, 0.6935]]).T


def lms_protanopia_sim(degree: float = 1.0) -> np.ndarray:
    """
    Matrix for Simulating Protanopia colorblindness from LMS color-space.
    :param degree: Protanopia degree.
    """
    return np.array([[1 - degree, 2.02344 * degree, -2.52581 * degree],
                        [0, 1, 0],
                        [0, 0, 1]]).T


def lms_deutranopia_sim(degree: float = 1.0) -> np.ndarray:
    """
    Matrix for Simulating Deutranopia colorblindness from LMS color-space.
    :param degree: Deutranopia degree.
    """
    return np.array([[1, 0, 0],
                        [0.494207 * degree, 1 - degree, 1.24827 * degree],
                        [0, 0, 1]]).T


def lms_tritanopia_sim(degree: float = 1.0) -> np.ndarray:
    """
    Matrix for Simulating Tritanopia colorblindness from LMS color-space.
    :param degree: Tritanopia degree.
    """
    return np.array([[1, 0, 0],
                        [0, 1, 0],
                        [-0.395913 * degree, 0.801109 * degree, 1 - degree]]).T


def hybrid_protanomaly_deuteranomaly_sim(degree_p: float = 1.0, degree_d: float = 1.0) -> np.ndarray:
    """
    Matrix for Simulating Hybrid Colorblindness (protanomaly + deuteranomaly) from LMS color-space.
    :param degree_p: protanomaly degree.
    :param degree_d: deuteranomaly degree.
    """
    return np.array([[1 - degree_p, 2.02344 * degree_p, -2.52581 * degree_p],
                        [0.494207 * degree_d, 1 - degree_d, 1.24827 * degree_d],
                        [0, 0, 1]]).T

map_p =np.array([[0,0,0],[0.7,1,0],[0.7,0,1]]).T
map_d =np.array([[1,0.7,0],[0,0,0],[0,0.7,1]]).T
map_t =np.array([[1,0,0.7],[0,1,0.7],[0,0,0]]).T


class LMSsim:
    @staticmethod
    def simulate_cvd(img:np.ndarray, deficiency:Deficiency, severity:float=1.0, corr=False):
        mat = np.zeros([3,3])
        mat_c = np.zeros([3,3])
        img = img/255.0
        img = convert.linearRGB_from_sRGB(img)
        if deficiency == Deficiency.PROTAN: 
            mat = lms_protanopia_sim(severity)
            mat_c = map_p
        if deficiency == Deficiency.DEUTAN: 
            mat = lms_deutranopia_sim(severity)
            mat_c = map_d
        if deficiency == Deficiency.TRITAN: 
            mat = lms_tritanopia_sim(severity)
            mat_c = map_t
        img_lms = img @ rgb_to_lms()
        img_sim_lms = img_lms @ mat
        img_sim = img_sim_lms @ lms_to_rgb()
        if corr:
            D = img - img_sim
            img_map = D @ mat_c
            img_corr = img + img_map
            img_sim = convert.sRGB_from_linearRGB(img_sim)
            img_corr = convert.sRGB_from_linearRGB(img_corr)
            return np.uint8(np.clip(img_sim*255.0, 0, 255)), np.uint8(np.clip(img_corr*255.0, 0, 255))
        img_sim = convert.sRGB_from_linearRGB(img_sim)
        return np.uint8(np.clip(img_sim*255.0, 0, 255))