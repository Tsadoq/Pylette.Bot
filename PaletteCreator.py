import sys

def image_creator(fileaddr):
    try:
        import colorgram
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("""You need PIL and cologram!
                    install them by using
                    pip install Pillow
                        and
                    pip install cologram.py""")
    width=750
    print('Opening image')
    scene = Image.open(fileaddr,'r')
    print('Resizing image')
    scene = scene.resize((width,int(scene.size[1]*width/scene.size[0])))
    print('Extracting palette')
    colors = [color.rgb for color in colorgram.extract(scene, 7)]
    background_height = scene.size[1]+50+50+101
    y = [scene.size[1]+50, scene.size[1]+101+75]
    x_start = 12
    x_end = 110
    print('Creating background')
    background = Image.new('RGB', (800, background_height), color='black')
    print('Creating visual palette')
    rectangle = ImageDraw.Draw(background)
    for col in colors:
        rectangle.rectangle([(x_start, y[0]), (x_end, y[1])], fill=(col.r, col.g, col.b), outline=None, width=0)
        x_start=x_start+110+3
        x_end=x_end+110+3
    background.paste(scene, (25, 25), mask=None)
    print('Finalizing and saving image')
    background.save(fileaddr+'_palette.jpg')
    print('Done!')
