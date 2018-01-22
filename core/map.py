import math
from PIL import Image, ImageDraw

from django.db.models import Sum, Max

from core.colormap import getVirdis


virdis = getVirdis()

def render_map(jumps, filepath, scale=1):
    jumps = jumps.prefetch_related(
        'origin',
        'destination'
    )

    colour_scale = jumps.aggregate(
        origin=Max('origin_jumps'),
        dest=Max('dest_jumps')
    )
    colour_scale = max(colour_scale['origin'], colour_scale['dest'])
    print(colour_scale)
    colour_scale = 4000
    colour_scale = math.sqrt(256 / colour_scale)

    # Draw image
    base_x = 4800 * scale
    base_y = 4096 * scale
    im = Image.new(
        "RGB",
        (
            int(base_x),
            int(base_y)
        ),
        "#000000"
    )
    draw = ImageDraw.Draw(im)

    for jump in jumps:
        fill = int(
            math.sqrt(
                max(jump.origin_jumps, jump.dest_jumps) * colour_scale
            )
        )
        plot_scale = 0.000000000000004 * scale
        x_offset = int(2680 * scale)
        y_offset = int(2000 * scale)

        draw.line(
            (
                jump.origin.x * plot_scale + x_offset,
                (jump.origin.z * -1) * plot_scale + y_offset,
                jump.destination.x * plot_scale + x_offset,
                (jump.destination.z * -1) * plot_scale + y_offset
            ),
            fill=virdis[
                min(fill, 255)
            ],
            width=int(fill / (24 / scale))
        )
    del draw

    im = im.resize(
        (
            int(base_x / 8),
            int(base_y / 8)
        ),
        Image.LANCZOS
    )
    im.save(filepath, "PNG")