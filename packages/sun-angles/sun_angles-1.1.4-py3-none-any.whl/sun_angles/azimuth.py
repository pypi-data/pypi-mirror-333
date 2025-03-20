import warnings
import numpy as np

def calculate_solar_azimuth(solar_dec_deg: np.ndarray, SZA_deg: np.ndarray, hour: np.ndarray) -> np.ndarray:
    """
    Calculate the solar azimuth angle based on the solar declination, solar zenith angle, and hour of the day.
    
    Parameters:
    solar_dec_deg (np.ndarray): Solar declination in degrees.
    SZA_deg (np.ndarray): Solar zenith angle in degrees.
    hour (np.ndarray): Hour of the day, where 0 corresponds to 00:00 and 23 corresponds to 23:00.
    
    Returns:
    np.ndarray: Solar azimuth angle in degrees.
    
    Note:
    This function ignores any warnings that might be generated during the calculations.
    
    References:
    Muneer, T., & Fairooz, F. (2005). Solar radiation and daylight models: for the energy efficient design of buildings. Architectural Press.
    """
    with warnings.catch_warnings():
        # Ignore warnings that might be generated during the calculations
        warnings.filterwarnings('ignore')
        
        # Convert the solar declination from degrees to radians
        solar_dec_rad = np.radians(solar_dec_deg)
        # Convert the solar zenith angle from degrees to radians
        SZA_rad = np.radians(SZA_deg)
        # Calculate the hour angle in degrees and convert it to radians
        hour_angle_deg = hour * 15.0 - 180.0
        # convert hour angle to radians
        hour_angle_rad = np.radians(hour_angle_deg)
        # Calculate the solar azimuth in radians using the formula provided in the docstring
        solar_azimuth_rad = np.arcsin(-1.0 * np.sin(hour_angle_rad) * np.cos(solar_dec_rad) / np.sin(SZA_rad))
        # Convert the solar azimuth from radians to degrees
        solar_azimuth_deg = np.degrees(solar_azimuth_rad)
    
    return solar_azimuth_deg
