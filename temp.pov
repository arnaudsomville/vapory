#include "colors.inc"
light_source {
<10,10,-10>
color
<1,1,1> 
}
sphere {
<0,0,0>
1.0
texture {
pigment {
image_map {
tiff
"/resources/images/earth_color_21K.tif"
map_type
1
interpolate
2 
} 
}
finish {
diffuse
0.8
ambient
0
specular
0.2
roughness
0.05 
} 
} 
}
camera {
location
<0,0,-10>
look_at
<0,0,0>
angle
30
right
<1.3333333333333333,0,0> 
}
global_settings{

}