function [boxes, delete] = generate_boxes(pattern)
    num_patterns = size(pattern, 1);
    ht = 11.848122162608338;
    W1 = 12.2750;
    delete = [];
    boxes = [];

for i = 1:num_patterns
    w = pattern(i).para.width;
    h = pattern(i).para.height;
    top = pattern(i).para.top;
    left = pattern(i).para.left;
    right = pattern(i).para.right;
    bottom = pattern(i).para.bottom; 
    num_rects = size(pattern(i).rects, 2);
    
    if max(w, h) <= 3*ht
        continue;
    end
    delta = min(W1, min(w, h)/4);
    flag = 1;
    
    for j = 1:num_rects
        [value, index]= min([pattern(i).rects(j).bottom - top, bottom - pattern(i).rects(j).top, ...
                right - pattern(i).rects(j).left, pattern(i).rects(j).right - left]);  
        if value > delta
            flag = 0;
            break;
        end
    end
    
    if flag
        boxes = [boxes; pattern(i)];
        delete = [delete; i];
    end
end
end