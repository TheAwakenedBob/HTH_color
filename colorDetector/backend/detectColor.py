def detectProperties(path):
    from google.cloud import vision
    import io
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/ericy/HTH_color/colorDetector/backend/eighth-azimuth-379620-9f35143e3248.json"

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as imageFile:
        content = imageFile.read()

    image = vision.Image(content=content)
    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    def rgb_to_hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

    colors = sorted(props.dominant_colors.colors,
                    key=lambda c: c.pixel_fraction, reverse=True)

    colorList = []
    for color in colors:
        r = color.color.red
        g = color.color.green
        b = color.color.blue
        fraction = color.pixel_fraction
        hexCode = rgb_to_hex(r, g, b)
        colorList.append({"fraction": fraction, "hex": hexCode})

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return colorList
