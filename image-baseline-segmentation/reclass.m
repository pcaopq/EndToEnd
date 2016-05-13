function [pattern, new_line]= reclass(pattern, line_patterns, img, rects)
    num_lines = size(line_patterns, 1);
    num_patterns = size(pattern, 1);
    if nargin < 4
        rects = get_rects_from_pattern(pattern);
    end
    flag = zeros(num_lines, 1);
    factor = 2;
    new_line = [];
    
    for i = 1:num_lines
        if flag(i)
            continue;
        end
        flag(i) = 1;
        
        switch line_patterns(i).type
            case 6 %vertical lines
                align_range = [line_patterns(i).para.left - line_patterns(i).para.width line_patterns(i).para.right + line_patterns(i).para.width];
                merge_range = factor*line_patterns(i).para.width;
                for j = i+1:num_lines
                    if flag(j)
                        continue;
                    end
                    if min([abs(line_patterns(i).para.top - line_patterns(j).para.bottom) abs(line_patterns(i).para.top - line_patterns(j).para.top) abs(line_patterns(i).para.bottom - line_patterns(j).para.top) abs(line_patterns(i).para.bottom - line_patterns(j).para.bottom)]) < merge_range &&...
                            line_patterns(j).para.left > align_range(1) && line_patterns(j).para.right < align_range(2)
                        flag(j) = 1;
                        line_patterns(i) = get_pattern_para(merge_patterns([line_patterns(i); line_patterns(j)]));                        
                    end
                end
                
                    merge_range = factor*line_patterns(i).para.width;
                    delete = [];
                    for k = 1:size(rects, 2)
                        if min([abs(line_patterns(i).para.top - rects(k).bottom) abs(line_patterns(i).para.top - rects(k).top) abs(line_patterns(i).para.bottom - rects(k).top) abs(line_patterns(i).para.bottom - rects(k).bottom)]) < merge_range &&...
                            rects(k).left > align_range(1) && rects(k).right < align_range(2)
                            delete = [delete; k];
                            line_patterns(i).rects = [line_patterns(i).rects rects(k)];
                            line_patterns(i) = get_pattern_para(line_patterns(i));                    
                        end
                    end
                    new_line = [new_line; line_patterns(i)];
                    rects(delete) = [];        
                    
            case 7 %horizontal lines
                align_range = [line_patterns(i).para.top - line_patterns(i).para.height line_patterns(i).para.bottom + line_patterns(i).para.height];
                merge_range = factor*line_patterns(i).para.height;
                for j = i+1:num_lines
                    if flag(j)
                        continue;
                    end
                    if min([abs(line_patterns(i).para.left - line_patterns(j).para.left) abs(line_patterns(i).para.left - line_patterns(j).para.right) abs(line_patterns(i).para.right - line_patterns(j).para.left) abs(line_patterns(i).para.right - line_patterns(j).para.right)]) < merge_range &&...
                            line_patterns(j).para.top > align_range(1) && line_patterns(j).para.bottom < align_range(2)
                        flag(j) = 1;
                        line_patterns(i) = get_pattern_para(merge_patterns([line_patterns(i); line_patterns(j)]));
                    end
                end
                    merge_range = factor*line_patterns(i).para.height;
                    delete = [];
                    for k = 1:size(rects, 2)
                        if min([abs(line_patterns(i).para.left - rects(k).left) abs(line_patterns(i).para.left - rects(k).right) abs(line_patterns(i).para.right - rects(k).left) abs(line_patterns(i).para.right - rects(k).right)]) < merge_range &&...
                            rects(k).top > align_range(1) && rects(k).bottom < align_range(2)
                            delete = [delete; k];
                            line_patterns(i).rects = [line_patterns(i).rects rects(k)];
                            line_patterns(i) = get_pattern_para(line_patterns(i));                    
                        end
                    end
                    new_line = [new_line; line_patterns(i)];
                    rects(delete) = [];                
        end
    end
%     pattern = generate_patterns(rects);
%     pattern = [pattern; new_line];
%     pattern = pattern_classify(pattern, img);
end

