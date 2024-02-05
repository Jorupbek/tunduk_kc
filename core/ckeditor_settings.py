CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'skin': 'moono-lisa',
        'height': 300,
        'width': 800,
    }
}


CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads'
CKEDITOR_FILENAME_GENERATOR = '../utils/utils/get_filename'
