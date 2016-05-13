function H = get_BlockH(patterns)
    num_patterns = size(patterns, 2);
    height = zeros(num_patterns, 1);
    for i = 1:num_patterns
        height(i) = patterns(i).para.height;
    end
    [value, ~] = sort(height, 'ascend');
    start = ceil(1/4*num_patterns);
    End = ceil(3/4*num_patterns);
    H = sum(value(start:End))/(End-start+1);
end