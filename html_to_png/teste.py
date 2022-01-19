import pdfcrowd
import sys

try:
    # create the API client instance
    client = pdfcrowd.HtmlToImageClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')

    # configure the conversion
    client.setOutputFormat('png')

    # run the conversion and write the result to a file
    client.convertUrlToFile('file://./sandra.html', 'sandra.png')
except pdfcrowd.Error as why:
    # report the error
    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

    # rethrow or handle the exception
    raise