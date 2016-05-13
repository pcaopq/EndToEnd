clear, clc
[HPOS VPOS WIDTH HEIGHT] = textread('test.txt', '%f %f %f %f\n');
rects = [];
num_rects = size(HPOS, 1);
HPOS = ceil(7714/30740*HPOS);
VPOS = ceil(7714/30740*VPOS);
WIDTH = ceil(7714/30740*WIDTH);
HEIGHT = ceil(7714/30740*HEIGHT);

for i = 1:num_rects
    tmp_rect = struct('left', HPOS(i), 'right', HPOS(i)+WIDTH(i), 'top', VPOS(i), 'bottom', VPOS(i)+HEIGHT(i));
    rects = [rects tmp_rect];
end
%[7737/29784, 5440/20736]
%[7714/30740, 5472/21472]
save('0033', 'rects');