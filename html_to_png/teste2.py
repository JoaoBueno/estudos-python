import imgkit

options = {
    'format': 'png',
    'enable-local-file-access': None,
    'crop-w': '300',
    'encoding': "UTF-8"
}

imgkit.from_file('sandra.html', 'sandra.png', options=options)
# imgkit.from_string('Hello!', 'sandra.jpg')