function ystep = lowest_row(img, rect)
    ystep = 0;
    [height, width] = size(img);
    %i is the height, j is the width
    for i = min(rect.top+2,height):-1:rect.top
        for j = rect.left:min(rect.right,width)
            if img(i, j) == 0
                ystep = i-rect.top+1;
                break;
            end
        end
        if ystep
            break;
        end
    end
end

