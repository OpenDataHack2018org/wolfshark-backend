from Magics.macro import *
import os
import sys
from .areas import Areas

dark_background = mcoast(
    map_coastline_sea_shade="on",
    map_coastline_land_shade_colour="rgb(12,63,106)",
    map_grid="off",
    map_coastline_land_shade="on",
    map_coastline_sea_shade_colour="rgb(0,3,60)",
    map_label="off",
    map_coastline_colour="rgb(12,63,106)",
)
light_background = mcoast(
    map_coastline_colour="black",
    map_coastline_land_shade="on",
    map_coastline_land_shade_colour="rgb(0.85,0.85,0.85)",
    map_coastline_sea_shade="on",
    map_coastline_sea_shade_colour="white",
    map_grid="off",
    map_label="off",
)

www_foreground = mcoast(
    map_disputed_boundaries="off",
    map_coastline_resolution="high",
    map_coastline_land_shade_colour="rgba(1,1,1, 0.2)",
    map_grid="on",
    map_grid_line_style="solid",
    map_grid_colour="rgba(0,0,0,0.5)",
    map_boundaries="on",
    map_boundaries_colour="rgba(255,255,255, 0.5)",
    map_administrative_boundaries_style="dot",
    map_administrative_boundaries_colour="rgba(255,255,255, 0.5)",
    map_coastline_land_shade="off",
    map_coastline_sea_shade="off",
    map_administrative_boundaries="off",
    map_label="off",
    map_coastline_colour="rgba(1,1,1, 0.8)",
)


def grib_to_png(filename, text, area=Areas.WORLD, width=4000, dark=True):
    print("grib_to_png called")
    print(filename)
    my_cont = mcont(contour_automatic_setting="web")

    if dark:
        background = dark_background
    else:
        background = light_background

    outfile = filename.split(".grib")[0]

    out = output(
        output_formats=["png"],
        output_name=outfile,
        output_width=width,
        subpage_x_position=0.,
        subpage_y_position=0.,
        subpage_x_length=120.,
        subpage_y_length=60.,
        page_x_position=0.,
        page_y_position=0.,
        page_x_length=120.,
        page_y_length=60.,
        super_page_x_length=120.,
        super_page_y_length=60.,
        page_id_line="off",
        output_name_first_page_number="off",
    )

    data = mgrib(grib_input_file_name=filename)

    my_title = mtext(
        text_box_y_position=28.5,
        text_box_x_position=28,
        text_mode="positional",
        text_line_1="Sea ice ERA 5 reanalysis",
        text_line_2=text,
        text_line_3="<grib_info key='valid-date' format='%d %B %Y' />",
        text_line_count=3,
        text_character_colour="navy",
        text_colour="navy",
        text_border="off",
        text_border_colour="black",
        text_font_size=1.5,
    )

    plot(out, area.value, background, data, my_cont, www_foreground, my_title)


if __name__ == "__main__":
    grib_to_png(sys.argv[1], "test", area=Areas.EUROPE)
