#!/usr/bin/env python3
from PIL import Image, ImageDraw

def draw_const_r(values, scale, image_width, image_height, line_width, draw, fill=None):
    for r in values:
        radius = scale * (1 / (1 + r))
        x_center = scale * (r / (1 + r))
        y_t = - radius + (image_height/2)
        y_b = + radius + (image_height/2)
        x_t = x_center - radius + (image_width/2)
        x_b = x_center + radius + (image_width/2)

        if fill is not None:
            draw.ellipse([x_t, y_t, x_b, y_b], fill=fill)
        else:
            draw.ellipse([x_t, y_t, x_b, y_b], outline=(0,0,0), width=line_width)


def draw_const_x(values, scale, image_width, image_height, line_width, draw):
    for X in values:
        radius = scale * (1 / X)
        y_center = radius
        x_center = scale
        y_t = y_center - radius + (image_height/2)
        y_b = y_center + radius + (image_height/2)
        x_t = x_center - radius + (image_width/2)
        x_b = x_center + radius + (image_width/2)

        draw.ellipse([x_t, y_t, x_b, y_b], outline=(0,0,0), width=line_width)

    # -ve
    for X in values:
        radius = scale * (1 / -X)
        y_center = radius
        x_center = scale
        y_t = y_center + radius + (image_height/2)
        y_b = y_center - radius + (image_height/2)
        x_t = x_center + radius + (image_width/2)
        x_b = x_center - radius + (image_width/2)

        draw.ellipse([x_t, y_t, x_b, y_b], outline=(0,0,0), width=line_width)


def draw_chart(image_width, image_height):
    LINE_WIDTH = 10
    SCALE = image_width/2
    const_r = [0, 0.25, 0.7, 1.7]
    const_x_outer = [0.25, 0.55, 0.95, 1.6]
    const_x_inner = const_x_outer[1::2]

    im_inner = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    draw_inner = ImageDraw.Draw(im_inner)
    draw_const_r(const_r, SCALE, image_width, image_height, LINE_WIDTH, draw_inner)
    draw_const_x(const_x_inner, SCALE, image_width, image_height, LINE_WIDTH, draw_inner)

    im_outer = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    draw_outer = ImageDraw.Draw(im_outer)
    draw_const_r(const_r, SCALE, image_width, image_height, LINE_WIDTH, draw_outer)
    draw_const_x(const_x_outer, SCALE, image_width, image_height, LINE_WIDTH, draw_outer)

    inner_outer_mask = Image.new("1", (image_width, image_height), 0)
    inner_outer_mask_draw = ImageDraw.Draw(inner_outer_mask)
    draw_const_r([const_r[2]], SCALE, image_width, image_height, LINE_WIDTH, inner_outer_mask_draw, 1)


    inner_outer_comp = Image.composite(im_inner, im_outer, inner_outer_mask)
    inner_outer_comp_draw = ImageDraw.Draw(inner_outer_comp)

    # Central Line
    inner_outer_comp_draw.line([0, image_height/2, image_width, image_height/2], fill=(0,0,0), width=LINE_WIDTH)

    im_background = Image.new("RGB", (image_width, image_height), (255, 255, 255))

    background_mask = Image.new("1", (image_width, image_height), 0)
    background_mask_draw = ImageDraw.Draw(background_mask)

    background_mask_draw.ellipse([0, 0, image_width, image_height], fill=1)

    background_composite = Image.composite(inner_outer_comp, im_background, background_mask)
    return background_composite

def main():
    dimension = 1024
    super_sample_factor = 2
    image = draw_chart(dimension * super_sample_factor, dimension * super_sample_factor)
    anti_aliased = image.resize((dimension, dimension), resample=Image.Resampling.LANCZOS)
    #anti_aliased.show()
    anti_aliased.save("smith_chart.png")


if __name__ == "__main__":
    main()
