function pattern = generate_patterns(rects, save_flag, name)
%     clear, clc
%     load('0033.mat');    
    pattern = [];
    num_rects = size(rects, 2);
%     remain_rects = num_rects;
    
    %initialize patterns
    new_pattern = struct(...
        'rects', struct('left', [], 'top', [], 'right', [], 'bottom', []),...
        'para', struct('left', [], 'top', [], 'right', [], 'bottom', [], 'width', [], 'height', [], 'area', [], 'bp_density', [], 'num_bp', [], 'nbr', [], 'mbrl', [],'sp', [], 'vbrl', []),...
        'type', []);
    
    new_pattern.rects = rects(1);
    pattern = [pattern; new_pattern];
    rects_count = 2;
    
    while rects_count < num_rects
        num_pattern = size(pattern, 1);
        rst = [];
        for i = 1:num_pattern
            if(check_near(rects(rects_count), pattern(i).rects, 1))
                rst = [rst; i];
            end
        end
        
        if size(rst, 1) == 1
            pattern(rst).rects = [pattern(rst).rects rects(rects_count)]; 
        elseif size(rst, 1)>1
            merged_pattern = merge_patterns(pattern(rst));
            merged_pattern.rects = [merged_pattern.rects rects(rects_count)];
            pattern(rst) = [];
            pattern = [pattern; merged_pattern];   
        else
            new_pattern = struct(...
                'rects', struct('left', [], 'top', [], 'right', [], 'bottom', []),...
                'para', struct('left', [], 'top', [], 'right', [], 'bottom', [], 'width', [], 'height', [], 'area', [], 'bp_density', [], 'num_bp', [], 'nbr', [], 'mbrl', [],'sp', [], 'vbrl', []),...
                'type', []);
            new_pattern.rects = rects(rects_count);
            pattern = [pattern; new_pattern];
        end
        
        rects_count = rects_count + 1
    end
    if nargin > 1
        save(name, 'pattern');
    end
end