function draw_patterns(pattern, color, linewidth, type)
    num_patterns = size(pattern, 1);
    if nargin == 1
        color = [0 0 1];
        draw_patterns(pattern, color, 1);
    elseif nargin == 4
        for i = 1:num_patterns
            if pattern(i).type == type
                tmp_rect = struct('left', [], 'top', [], 'right', [], 'bottom', []);
                tmp_rect.left = pattern(i).para.left;
                tmp_rect.top = pattern(i).para.top;
                tmp_rect.right = pattern(i).para.right;
                tmp_rect.bottom = pattern(i).para.bottom;
                draw_rects(tmp_rect, color, linewidth);
            end
        end
    elseif nargin == 3 || nargin == 2
            color1 = [0 0 1];
            color2 = [1 0 0];
            color3 = [1 0.5 0.05];
            color4 = [1 0.5 0.05];
            color5 = [1 0.5 0.05];
            color6 = [0 0 0];
            color7 = [0 0 0];
            
        if nargin == 2
            linewidth = 3;
            if pattern(1).type == 6 || pattern(1).type == 7
                linewidth = 2;
            elseif pattern(1).type ~= 4 && pattern(1).type ~= 5
                linewidth = 1;
            end
            color1 = color;
            color2 = color;
            color3 = color;
            color4 = color;
            color5 = color;
            color6 = color;
            color7 = color;
        end
        
        for i = 1:num_patterns
            tmp_rect = struct('left', [], 'top', [], 'right', [], 'bottom', []);
            tmp_rect.left = pattern(i).para.left;
            tmp_rect.top = pattern(i).para.top;
            tmp_rect.right = pattern(i).para.right;
            tmp_rect.bottom = pattern(i).para.bottom;
%             if pattern(i).para.area > 11000
                if pattern(i).type == 1
                    draw_rects(tmp_rect, color1, linewidth);
                end
                if pattern(i).type == 2
                    draw_rects(tmp_rect, color2, linewidth);
                end
                if pattern(i).type == 3
                    draw_rects(tmp_rect, color3, linewidth);
                end
                if pattern(i).type == 4
                    draw_rects(tmp_rect, color4, linewidth);
                end
                if pattern(i).type == 5
                    draw_rects(tmp_rect, color5, linewidth);
                end
                if pattern(i).type == 6
                    draw_rects(tmp_rect, color6, linewidth);
                end
                if pattern(i).type == 7
                    draw_rects(tmp_rect, color7, linewidth);
                end      
            end
%         end
    end
end

% for j=1:size(pattern(i).rects, 2)
%     draw_rectangle(pattern(i).rects(j), color);
% end
% hold on,