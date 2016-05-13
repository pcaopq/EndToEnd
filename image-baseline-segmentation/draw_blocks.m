function draw_blocks(block, type, full)
    num_blocks = size(block, 1);
    color1 = [rand(1) rand(1) rand(1)];
    color2 = [rand(1) rand(1) rand(1)];
    color3 = [rand(1) rand(1) rand(1)];
    color4 = [rand(1) rand(1) rand(1)];
    color5 = [rand(1) rand(1) rand(1)];
    color6 = [rand(1) rand(1) rand(1)];
    color7 = [rand(1) rand(1) rand(1)];
    color8 = [0 0 0];
    
    if nargin == 1
        for i = 1:num_blocks
            for j = 1:size(block(i).patterns, 2)
                if block(i).type == 1
                    draw_patterns(block(i).patterns(j), color1);
                end
                if block(i).type == 2
                    draw_patterns(block(i).patterns(j), color2);
                end
                if block(i).type == 3
                    draw_patterns(block(i).patterns(j), color3);
                end
                if block(i).type == 4
                    draw_patterns(block(i).patterns(j), color4);
                end
                if block(i).type == 5
                    draw_patterns(block(i).patterns(j), color5);
                end
                if block(i).type == 6
                    draw_patterns(block(i).patterns(j), color6);
                end
                if block(i).type == 7
                    draw_patterns(block(i).patterns(j), color7);
                end
                if block(i).type == 8
                    draw_patterns(block(i).patterns(j), color8);
                end                
            end
        end
    elseif nargin == 2
        for i = 1:num_blocks
            for j = 1:size(block(i).patterns, 2)
                if block(i).type == type
                    draw_patterns(block(i).patterns(j), [0 0 1]);
                end
            end
        end
    elseif nargin == 3
        for i = 1:num_blocks
            draw_patterns(block(i));
        end
    end
end