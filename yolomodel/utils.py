def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png'))

def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.mov', '.avi'))
