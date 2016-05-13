function block = get_block_para(block)
    num_patterns = size(block.patterns, 2);
    left = [];
    right = [];
    top = [];
    bottom = [];
    for i = 1:num_patterns
        left = [left; min(block.patterns(i).para.left)];
        right = [right; min(block.patterns(i).para.right)];
        top = [top; min(block.patterns(i).para.top)];
        bottom = [bottom; min(block.patterns(i).para.bottom)];        
    end
    block.para.left = min(left);
    block.para.top = min(top);
    block.para.right = max(right);
    block.para.bottom = max(bottom);
    block.para.width = block.para.right - block.para.left;
    block.para.height = block.para.bottom - block.para.top;
    block.para.area = block.para.height * block.para.width;
end