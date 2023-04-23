"""SDO AIA sender."""

from .common import cq_send_message, load_config


SDO_VIDEOS = [
    {
        "name": "SDO AIA 193",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0193.mp4",
        "description": """Where: Corona and hot flare plasma
Wavelength: 193 angstroms (0.0000000193 m) = Extreme Ultraviolet
Primary ions seen: 11 times ionized iron (Fe XII)
Characteristic temperature: 1.25 million K (2.25 million F)"""
    },
    {
        "name": "SDO AIA 171",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0171.mp4",
        "description": """Where: Quiet corona and upper transition region
Wavelength: 171 angstroms (0.0000000171 m) = Extreme Ultraviolet
Primary ions seen: 8 times ionized iron (Fe IX)
Characteristic temperature: 1 million K (1.8 million F)"""
    },
    {
        "name": "SDO AIA 304",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0304.mp4",
        "description": """Where: Upper chromosphere and lower transition region
Wavelength: 304 angstroms (0.0000000304 m) = Extreme Ultraviolet
Primary ions seen: singly ionized helium (He II)
Characteristic temperature: 50,000 K (90,000 F)"""
    },
]


def send_sdo():
    config = load_config()
    image_msg = "[CQ:image," \
                "file=https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_0193.jpg," \
                "cache=0]"
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], image_msg)
