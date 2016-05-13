function pattern = merge_patterns(patterns)
    num_patterns = size(patterns, 1);
    pattern = patterns(1);
    for i= 2:num_patterns
        pattern.rects = [pattern.rects patterns(i).rects];
    end
end

