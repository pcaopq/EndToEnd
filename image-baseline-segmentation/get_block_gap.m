function [avh, hgap, vgap] = get_block_gap(patterns)
    num_patterns = size(patterns, 1);
%     avh = 0;
    num_texts = 0;
    height = [];
    for i = 1:num_patterns
        if patterns(i).type == 1 || patterns(i).type == 2
%             avh = avh + patterns(i).para.height;
            num_texts = num_texts + 1;
            height = [height; patterns(i).para.height];
        end
    end
%     avh = avh/num_texts;
    [value, ~] = sort(height, 'ascend');
    start = ceil(1/4*num_texts);
    End = ceil(3/4*num_texts);
    avh = sum(value(start:End))/(End-start+1);
    hgap = 1.1*avh;
    vgap = 0.8*avh;
end