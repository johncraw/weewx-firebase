# installer for Firebase file upload extension

from setup import ExtensionInstaller

def loader():
    return FirebaseUploadInstaller()

class FirebaseUploadInstaller(ExtensionInstaller):
    def __init__(self):
        super(FirebaseUploadInstaller, self).__init__(
            version="0.1",
            name='FirebaseUpload',
            description='Upload files to a Firebase instance',
            author='John Crawford',
            config={
                'StdReport': {
                    'FirebaseUpload': {
                        'skin': 'FirebaseUpload'}}},
            files=[('bin/user', ['bin/user/FirebaseUpload.py']),
                   ('skins/FirebaseUpload', ['skins/FirebaseUpload/skin.conf'])],
            )
