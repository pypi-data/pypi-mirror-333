from typing import Dict, Tuple
import datetime
import json
import numpy as np
from .Snowpack import Snowpack
import warnings

def read_json_profile(json_file: str) -> Tuple[Snowpack, Dict]:
    """
    Read a snowpack profile from a JSON file and convert it to a Snowpack object.
    
    Args:
        json_file (str): Path to the JSON file containing the snowpack profile
        
    Returns:
        Tuple[Snowpack, Dict]: A tuple containing:
            - Snowpack object with the profile data
            - Dictionary with station metadata
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract station metadata
    metadata = {
        "StationName": data["name"],
        "Latitude": data["position"]["latitude"],
        "Longitude": data["position"]["longitude"],
        "Altitude": data["position"]["altitude"],
        "SlopeAngle": data["position"]["angle"],
        "SlopeAzi": data["position"]["_azimuth"]
    }
    
    # Create Snowpack object
    snowpack = Snowpack()
    
    # Get the first profile (assuming single date)
    profile = data["profiles"][0]
    
    # Get profile date
    profile_date = datetime.datetime.fromisoformat(profile["date"])
    
    # Process layer data
    layers = []
    
    # Extract layers from hardness data (which contains the layer structure)
    hardness_data = profile["hardness"]["elements"][0]["layers"]
    
    # Sort layers by bottom height to ensure correct ordering
    hardness_data.sort(key=lambda x: x["bottom"])
    
    # Convert layer boundaries to format needed by Snowpack
    boundaries = []
    for layer in hardness_data:
        if not boundaries:  # First layer
            boundaries.append(layer["bottom"])
        boundaries.append(layer["top"])
    
    # Convert hardness values to Newton scale if needed (assuming values > 6 indicate Newton scale)
    hardness_values = []
    is_newton = any(layer["value"] > 6 for layer in hardness_data)
    snowpack.isNewton = is_newton
    for layer in hardness_data:
        hardness_values.append(layer["value"])
    
    # Set layer boundaries
    snowpack.set_param("0501", np.array(boundaries), len(boundaries))
    
    # Set hardness values
    snowpack.set_param("0534", np.array(hardness_values), len(hardness_values))
    
    # Process temperature data
    if "temperature" in profile:
        temp_data = profile["temperature"]["elements"][0]["layers"]
        temp_values = []
        temp_pos = []
        for layer in temp_data:
            temp_values.append(layer["value"])
            temp_pos.append(layer["bottom"])
        bottom_temp = temp_values[0]
        top_temp = temp_values[-1]
        # linearly interpolate temperature values to the middle of the layers
        layer_middles = [boundaries[i] + (boundaries[i+1] - boundaries[i]) / 2 for i in range(len(boundaries) - 1)]
        temp_values = np.interp(layer_middles, temp_pos, temp_values)
        snowpack.set_param("0503", np.array(temp_values), len(temp_values))
    
    # Process density data
    if "density" in profile:
        density_data = profile["density"]["elements"][0]["layers"]
        density_values = []
        for layer in density_data:
            if "value" in layer:
                density_values.append(layer["value"])
        if density_values:
            snowpack.set_param("0502", np.array(density_values), len(density_values))
    
    # Process grain shape data
    if "grainshape" in profile:
        grain_data = profile["grainshape"]["elements"][0]["layers"]
        grain_codes = []
        for layer in grain_data:
            # Convert grain shape codes to numeric format
            primary = layer["value"]["primary"]
            secondary = layer["value"].get("secondary", "")
            # Combine primary and secondary into Swiss Code format
            if primary == "MFcr":
                code = int(772)
            else:
                primary_code = TYPES_TO_CODE.get(primary, 0)
                secondary_code = TYPES_TO_CODE.get(secondary, 0)
                code = int(f"{primary_code}{secondary_code}{0}")
            grain_codes.append(code)
        if grain_codes:
            snowpack.set_param("0513", np.array(grain_codes), len(grain_codes))
            
    # Process grain size data
    if "grainsize" in profile:
        size_data = profile["grainsize"]["elements"][0]["layers"]
        size_values = []
        for layer in size_data:
            if "value" in layer and layer["value"] is not None:
                size_values.append(layer["value"]["avg"])
            else:
                size_values.append(0.0)  # Default value for missing data
        if size_values:
            snowpack.set_param("0512", np.array(size_values), len(size_values))
            
    if "wetness" in profile:
        wetness_data = profile["wetness"]["elements"][0]["layers"]
        wetness_values = []
        for layer in wetness_data:
            if "value" in layer and layer["value"] is not None:
                wetness_values.append(layer["value"])
            else:
                wetness_values.append(0.0)  # Default value for missing data
        if wetness_values:
            snowpack.set_param("0506", np.array(wetness_values), len(wetness_values))
        
    # stability index  
    snowpack._parse_data(False)

    snowpack._parsed = True
    
    # Calculate stability indices
    try:
        stability_indices = snowpack.calculate_stability_indices()
        snowpack.weak_layer = stability_indices
    except Exception as e:
        warnings.warn(f"Could not calculate stability indices: {str(e)}")
    
    return snowpack, metadata, profile_date, bottom_temp, top_temp

TYPES_TO_CODE: Dict[str, int] = {
    "PP" : 1,
    "DF" : 2,
    "RG" : 3,
    "FC" : 4,
    "DH" : 5,
    "SH" : 6,
    "MF" : 7,
    "IF" : 8,
    "FCxr" : 9}