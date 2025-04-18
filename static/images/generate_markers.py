"""
Generate SVG marker icons for the map.
This script creates two marker icons:
1. A green marker for listings (marker-green.svg)
2. A blue marker for the user's location (marker-user.svg)
"""

import os

def generate_marker_svg(color, output_filename):
    """Generate an SVG marker with the specified color."""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="25px" height="41px" viewBox="0 0 25 41" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <path d="M12.5,0 C5.59644063,0 0,5.59644063 0,12.5 C0,21.875 12.5,41 12.5,41 C12.5,41 25,21.875 25,12.5 C25,5.59644063 19.4035594,0 12.5,0 Z M12.5,17 C10.0147186,17 8,14.9852814 8,12.5 C8,10.0147186 10.0147186,8 12.5,8 C14.9852814,8 17,10.0147186 17,12.5 C17,14.9852814 14.9852814,17 12.5,17 Z" fill="{color}" fill-rule="nonzero"></path>
    </g>
</svg>'''
    
    with open(output_filename, 'w') as f:
        f.write(svg_content)
    
    print(f"Generated {output_filename}")

def main():
    # Create the markers
    generate_marker_svg("#335633", "static/images/marker-green.svg")  # Primary green for listings
    generate_marker_svg("#2196F3", "static/images/marker-user.svg")   # Blue for user location
    
    print("Marker SVGs generated successfully.")
    print("Note: For production use, you may want to convert these SVGs to PNGs.")

if __name__ == "__main__":
    main()