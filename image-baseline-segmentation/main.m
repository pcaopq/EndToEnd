% function main
    clear, clc
    img = imread('post3.jpg');
    img = im2bw(img, 0.7);
%     rects = locate_rects(img);
%     pattern = generate_patterns(rects);
%     pattern = pattern_classify(pattern, img);
    load('post3');
    [boxes, delete] = generate_boxes(pattern);
    [Aline, pattern] = extract_line_boxes(pattern, boxes, delete, 1);
    line = Aline;
    [pattern, line] = reclass(pattern, line, img, rects); %contruct lines from line segments
    [tmp_line, index] = get_line_from_patterns(pattern);
    line = [tmp_line; line];
    
%     pattern(delete) = [];
%     pattern(index) = [];

%     blocks = regionform(pattern);
    load('post3block');
    blocks = cleanregion(blocks, 15, 0);
    blocks = dealwithblocks(blocks);
    
    lineblk = changeline2blk(line);
    blocks = [blocks; lineblk];
    
    %clear the line in the text blocks    
    blocks = cleanlineintext(blocks);
    imshow(img), hold on,
    draw_patterns(blocks, [0 0 0], 2);