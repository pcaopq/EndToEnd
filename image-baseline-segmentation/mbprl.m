function [mbrl nbr vbrl] = mbprl(rect, img)
    seg = img(rect.top:rect.bottom, rect.left:rect.right);
    [height width] = size(seg);
    length = zeros(width, height);
    for i = 1:height
        start = 1;
        while start <= width
            if ~seg(i, start)
                len = 1;
                p = start + 1;
                
                if p<=width
                    while ~seg(i,p)
                        len = len + 1;
                        p = p + 1;
                        if p > width
                            break;
                        end
                    end    
                end
                
                length(i, start) = len;
                start = start + len;
            else
                start = start + 1;
            end
        end
    end
    mbrl = max(max(length));
    nbr = size(find(length ~= 0), 1);
    vbrl = std(length(length~=0));
end

