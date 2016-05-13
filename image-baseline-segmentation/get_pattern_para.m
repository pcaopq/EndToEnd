function pattern = get_pattern_para(pattern, img)
    num_pattern = size(pattern, 1);  
    for i = 1:num_pattern
        pattern(i).para.left = min([pattern(i).rects.left]);
        pattern(i).para.top = min([pattern(i).rects.top]);
        pattern(i).para.right = max([pattern(i).rects.right]);
        pattern(i).para.bottom = max([pattern(i).rects.bottom]);
        pattern(i).para.width = pattern(i).para.right - pattern(i).para.left;
        pattern(i).para.height = pattern(i).para.bottom - pattern(i).para.top;
        pattern(i).para.area = pattern(i).para.height * pattern(i).para.width;
        if nargin > 1
            [img_height, img_width] = size(img);
            pattern(i).para.right = min(pattern(i).para.right, img_width);
            pattern(i).para.bottom = min(pattern(i).para.bottom, img_height);
            index = find(img(pattern(i).para.top:pattern(i).para.bottom, pattern(i).para.left:pattern(i).para.right) == 0);
            b = size(index, 1);
            pattern(i).para.num_bp = b;
            pattern(i).para.bp_density = b/(pattern(i).para.area - b);
            tmp_rect = struct('left', pattern(i).para.left, 'right', pattern(i).para.right, 'top', pattern(i).para.top, 'bottom', pattern(i).para.bottom);
            [pattern(i).para.mbrl, pattern(i).para.nbr, pattern(i).para.vbrl]= mbprl(tmp_rect, img);
            pattern(i).para.sp = (pattern(i).para.nbr/b)*(min(pattern(i).para.width, pattern(i).para.height)^2);
        end
    end
end

