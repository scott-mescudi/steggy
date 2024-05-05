import exifread
from datetime import datetime

def get_geotag_info(image_path):
    """Extracts geotag information from an image."""
    with open(image_path, 'rb') as file:
        tags = exifread.process_file(file)
    
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        lat_components = tags['GPS GPSLatitude'].values
        lon_components = tags['GPS GPSLongitude'].values
        
        lat_degrees = float(lat_components[0].num) / float(lat_components[0].den)
        lat_minutes = float(lat_components[1].num) / float(lat_components[1].den)
        lat_seconds = float(lat_components[2].num) / float(lat_components[2].den)
        lon_degrees = float(lon_components[0].num) / float(lon_components[0].den)
        lon_minutes = float(lon_components[1].num) / float(lon_components[1].den)
        lon_seconds = float(lon_components[2].num) / float(lon_components[2].den)
        
        lat_direction = str(tags['GPS GPSLatitudeRef'])
        lon_direction = str(tags['GPS GPSLongitudeRef'])
        
        latitude = (lat_degrees + (lat_minutes / 60.0) + (lat_seconds / 3600.0)) * (-1 if lat_direction == 'S' else 1)
        longitude = (lon_degrees + (lon_minutes / 60.0) + (lon_seconds / 3600.0)) * (-1 if lon_direction == 'W' else 1)
        
        datetime_obj = datetime.strptime(str(tags.get('EXIF DateTimeOriginal', '')), '%Y:%m:%d %H:%M:%S') if 'EXIF DateTimeOriginal' in tags else None
        
        device = f"{tags.get('Image Make', '')} {tags.get('Image Model', '')}" if 'Image Make' in tags and 'Image Model' in tags else None
            
        return latitude, longitude, datetime_obj, device




