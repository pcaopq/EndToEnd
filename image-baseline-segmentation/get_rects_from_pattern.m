function rects = get_rects_from_pattern(pattern)
    num_pattern = size(pattern, 1);
    rects = [];
    for i = 1:num_pattern
        fprintf('The current pattern is: %d\n', i);
        num_rects = size(pattern(i).rects, 2);
        for j = 1:num_rects
            rects = [rects pattern(i).rects(j)];
        end
    end
end

