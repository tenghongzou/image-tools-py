from flask import Flask, request, Response, render_template, make_response
from PIL import Image
import io


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jpgtopng")
def jpgtopng():
    return render_template("jpgtopng.html")

@app.route("/pngtojpg")
def pngtojpg():
    return render_template("pngtojpg.html")

@app.route("/webptopng")
def webptopng():
    return render_template("webptopng.html")

@app.route("/bmptopng")
def bmptopng():
    return render_template("bmptopng.html")

@app.route("/pngtopdf")
def pngtopdf():
    return render_template("pngtopdf.html")


@app.route('/api/jpgtopng', methods=['POST'])
def convert_jpg_to_png():
    # check if image file exists in request
    if 'image' not in request.files:
        return "No image selected", 400

    image = request.files['image']

    # check if file is JPEG format
    if not image.filename.endswith('.jpg') and not image.filename.endswith('.jpeg'):
        return "Image format must be JPEG", 400

    # check if file size is less than 5 MB
    if len(image.read()) > 5 * 1024 * 1024:
        return "File size must be less than 5 MB", 400

    # reset file pointer to start
    image.seek(0)

    # convert JPEG image to PNG
    with Image.open(image) as img:
        png_image = io.BytesIO()
        img.save(png_image, 'PNG')
        png_image.seek(0)

    # create response object with PNG image as attachment
    response = Response(png_image.getvalue(), mimetype='image/png')
    response.headers.set('Content-Disposition', 'attachment', filename='converted.png')

    return response

@app.route('/api/pngtojpg', methods=['POST'])
def convert_png_to_jpg():
    # Check if image is present in request
    if 'image' not in request.files:
        return Response("No image found", status=400)
    
    # Get the image from request
    image_file = request.files['image']
    
    # Check if the file is a PNG image
    if not image_file.filename.lower().endswith('.png'):
        return Response("Only PNG images are supported", status=400)
    
    # Open the image file in Pillow
    image = Image.open(image_file)
    
    # Convert the image to JPEG format
    png_image = io.BytesIO()
    image.convert('RGB').save(png_image, format='JPEG')
    
    # Create a response object with the converted image as an attachment
    response = Response(png_image.getvalue(), mimetype='image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='converted.jpg')
    return response

@app.route('/api/webptopng', methods=['POST'])
def convert_webp_to_png():
    # check if request contains a file
    if 'image' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['image']
    
    # check if file is of webp format
    if file.filename.split('.')[-1].lower() != 'webp':
        return 'File format not supported', 400
    
    # convert webp image to png format
    try:
        img = Image.open(io.BytesIO(file.read()))
        png_img = io.BytesIO()
        img.save(png_img, 'png')
        png_img.seek(0)
    except Exception as e:
        return 'Error converting image', 500
    
    # send png image as downloadable attachment
    response = Response(png_img, mimetype='image/png')
    response.headers.set('Content-Disposition', 'attachment', filename='converted.png')
    return response

@app.route('/api/bmptopng', methods=['POST'])
def convert_bmp_to_png():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    file = request.files['image']
    if file.filename == '':
        return 'No file selected', 400
    if file and file.filename.lower().endswith('.bmp'):
        img = Image.open(file)
        with io.BytesIO() as output:
            img.save(output, format='PNG')
            output.seek(0)
            
            response = Response(output.getvalue(), mimetype='image/png')
            response.headers.set('Content-Disposition', 'attachment', filename='converted.png')
            return response
    else:
        return 'Invalid file type. Please select a BMP image.', 400

@app.route('/api/pngtopdf', methods=['POST'])
def convert_png_to_pdf():
    # Check if request contains a file
    if 'image' not in request.files:
        return 'No file found', 400
    
    # Get the file from the request
    file = request.files['image']
    
    # Check if the file is a PNG image
    if file.mimetype != 'image/png':
        return 'File must be a PNG image', 400
    
    # Open the image and convert to PDF
    with Image.open(file) as img:
        # Create an in-memory file object for the PDF
        pdf_buffer = io.BytesIO()
        
        # Convert the image to PDF and save to in-memory file object
        img.save(pdf_buffer, format='PDF')
        
        # Set the position of the buffer to the start
        pdf_buffer.seek(0)
        
        # Create a response with the PDF file as attachment
        response = Response(pdf_buffer.getvalue(), mimetype='application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='converted.pdf')
        return response

if __name__ == "__main__":
    app.run(debug=True)