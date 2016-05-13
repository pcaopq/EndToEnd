function rects = locate_rects(img)
%     set(gca, 'YDir', 'reverse');
    [height, width] = size(img); %h is the height, w is the width
    rects = [];
    x = 1;
    y = 1;
    xstep = 3;
    
    while y <= height && x <= width
        if xstep == search_right(img, x, y, xstep);
            rect_tmp = struct('left', [], 'top', [], 'right', [], 'bottom', []);
            rect_tmp.left = x;
            rect_tmp.top = y;
            x = x + xstep;
            
        while xstep == search_right(img, x, y, xstep)
            x = x+xstep;
        end
        
        rect_tmp.right = min(x, width);
        ystep = lowest_row(img, rect_tmp);
        ry = y + ystep;
        
        while ystep == search_below(img, rect_tmp, ry, ystep)
            ry = ry+ystep;
        end
        
        rect_tmp.bottom = min(ry, height);
%       3.27¸Ä rect_tmp.bottom = ry - 1;
        rects = [rects rect_tmp];
        
        else
            x = x+3;
        end
        
        if x>=width
            x = 1;
            y = y+3;
        end
        y
    end
end