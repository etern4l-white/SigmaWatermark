from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
from django.contrib.staticfiles.storage import staticfiles_storage


def get_padding(string, box_width, font):
    _, _, space_len, _ = font.getbbox(" ")
    _, _, len_of_string_pixels, _ = font.getbbox(string)
    padding = (box_width - len_of_string_pixels)//space_len//2
    return padding

def add_watermark(original_image, format, name, border_color, text_color):
    img_width, img_height = original_image.size
    watermark_layer = Image.new("RGBA" if format=='PNG' else "RGB", original_image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)
    box_width = img_width//5
    box_height = img_height//10
    position = (img_width - box_width - 10, 10)
    border_width = 2
    draw.rectangle([position[0] - border_width, position[1] - border_width,
                    position[0] + box_width + border_width,
                    position[1] + box_height + border_width],
                    outline=border_color, width=border_width)

    font_size = 28
    try:
        font = ImageFont.truetype(staticfiles_storage.path('fonts/Arial.ttf'), font_size)
    except Exception as e:
        font = ImageFont.load_default(size=20)
    padding_name = get_padding(name, box_width, font)
    text = f"{' '*padding_name}{name}{' '*(padding_name-1)}\n"
    draw.text(position, text, font=font, fill=text_color)
    end_result = Image.alpha_composite(original_image.convert("RGBA" if format=='PNG' else "RGB"), watermark_layer)
    if format == "JPEG":
        end_result.convert("RGB")
    result_bytes = BytesIO()
    end_result.save(result_bytes, format=format)
    result_bytes.seek(0)
    return result_bytes

def watermark_image(image_bytes, name):
    img = Image.open(image_bytes)
    
    img_format = img.format
    img_with_watermark = add_watermark(img, img_format, name, "red", 'red')
    return img_with_watermark.read()

def watermark_doc(document_bytes, name):
    with zipfile.ZipFile(document_bytes, 'r') as zipped_doc:
        unzipped_stream = BytesIO()
        with zipfile.ZipFile(unzipped_stream, 'w', zipfile.ZIP_DEFLATED) as unzipped_doc:
            for file in zipped_doc.infolist():
                if file.filename[:len('word/media')] == 'word/media':
                    org_image = BytesIO(zipped_doc.read(file.filename))
                    try:
                        new_image = watermark_image(org_image, name)
                    except Exception as e:
                        print(e)
                        print("Error at", file.filename)
                        org_image.seek(0)
                        new_image = org_image.read()
                    unzipped_doc.writestr(file, new_image)
                else:
                    unzipped_doc.writestr(file, zipped_doc.read(file.filename))
    unzipped_stream.seek(0)
    return unzipped_stream
