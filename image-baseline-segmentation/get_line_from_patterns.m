function [line, index] = get_line_from_patterns(pattern)
    line = [];
    index = [];
    num_patterns = size(pattern, 1);
    for i = 1:num_patterns
        if pattern(i).type == 6 || pattern(i).type == 7
            line = [line; pattern(i)];
            index = [index; i];
        end
    end
end