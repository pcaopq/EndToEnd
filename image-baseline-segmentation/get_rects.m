% function main
clear
clc
img = imread('smaller1.jpg');
img = im2bw(img, 0.7);
imshow(img);
hold on,
rects = locate_rects(img);
draw_rects(rects, [0 1 0]);
save('smaller1', 'rects');
% end