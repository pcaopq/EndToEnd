function [line_patterns, pattern] = extract_line_boxes(pattern, boxes, delete, count_threshold)  
%     load('pattern_img_0003_classifed.mat');
    ht = 11.848122162608338;
    W1 = 12.2750;
    num_boxes = size(delete, 1);
    boxes = pattern(delete);
    line_patterns = [];
    horizontal_line = struct( 'rects', struct('left', [], 'top', [], 'right', [], 'bottom', []),...
            'para', struct('left', [], 'top', [], 'right', [], 'bottom', [], 'width', [], 'height', [], 'area', [], 'bp_density', [], 'num_bp', [], 'nbr', [], 'mbrl', [],'sp', [], 'vbrl', []),...
            'type', 7);
    vertical_line = struct(...
            'rects', struct('left', [], 'top', [], 'right', [], 'bottom', []),...
            'para', struct('left', [], 'top', [], 'right', [], 'bottom', [], 'width', [], 'height', [], 'area', [], 'bp_density', [], 'num_bp', [], 'nbr', [], 'mbrl', [],'sp', [], 'vbrl', []),...
            'type', 6);
    for i = 1:num_boxes
        num_rects = size(boxes(i).rects, 2);
        w = boxes(i).para.width;
        h = boxes(i).para.height;
        top = boxes(i).para.top;
        left = boxes(i).para.left;
        right = boxes(i).para.right;
        bottom = boxes(i).para.bottom;
        top_line = horizontal_line;        
        left_line = vertical_line;   
        bottom_line = horizontal_line;   
        right_line = vertical_line;    
%         delta = min(W1, min(w, h)/4);
                
        for j = 1:num_rects
            tmp = min([boxes(i).rects(j).bottom - top; bottom - boxes(i).rects(j).top; boxes(i).rects(j).right - left; right - boxes(i).rects(j).left]);
            if boxes(i).rects(j).bottom - top == tmp
                top_line.rects = [top_line.rects boxes(i).rects(j)];
            end
            if bottom - boxes(i).rects(j).top == tmp
                bottom_line.rects = [bottom_line.rects boxes(i).rects(j)];
            end
            if boxes(i).rects(j).right - left == tmp
                left_line.rects = [left_line.rects boxes(i).rects(j)];
            end
            if right - boxes(i).rects(j).left == tmp
                right_line.rects = [right_line.rects boxes(i).rects(j)];
            end            
        end
        top_line.rects(1:end-1) = top_line.rects(2:end); top_line.rects(end) = [];
        left_line.rects(1:end-1) = left_line.rects(2:end); left_line.rects(end) = [];
        right_line.rects(1:end-1) = right_line.rects(2:end); right_line.rects(end) = [];
        bottom_line.rects(1:end-1) = bottom_line.rects(2:end); bottom_line.rects(end) = [];        
        
        if size(top_line.rects, 2) >= count_threshold
            line_patterns = [line_patterns; top_line];
        end
        if size(left_line.rects, 2) >= count_threshold
            line_patterns = [line_patterns; left_line];
        end
        if size(bottom_line.rects, 2) >= count_threshold
            line_patterns = [line_patterns; bottom_line];
        end
        if size(right_line.rects, 2) >= count_threshold
            line_patterns = [line_patterns; right_line];
        end        
    end
    line_patterns = get_pattern_para(line_patterns);
    pattern(delete) = [];
end