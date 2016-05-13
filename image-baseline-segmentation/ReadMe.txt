%The function locate_rects and pattern_classify needs large amount of time(about 30 %minutes), so I ran them in advance and store the matrices in post3. So you can simply %load them to get the results. You can also run them manually by: 

clear, clc
img = imread('post3.jpg');
img = im2bw(img, 0.7);
rects = locate_rects(img);
pattern = generate_patterns(rects);
pattern = pattern_classify(pattern, img);
%The results are three matrices which are rects, img and classified pattern.

%Prepocessing
clear, clc
img = imread('post3.jpg');
img = im2bw(img, 0.7);

%The figures are in ReadMe.doc
%get figure 4 
load('post3'); imshow(img), hold on, draw_rects(rects, [0 0 1], 1);

%get figure 6
load('post3'); imshow(img), hold on, draw_patterns(pattern, [0 0 1]); 

%get figure 7
load('post3'); imshow(img), hold on, draw_patterns(pattern); 

%get lines
load('post3');    
[boxes, delete] = generate_boxes(pattern);    
[Aline, pattern] = extract_line_boxes(pattern, boxes, delete, 1);    
line = Aline;
[pattern, line] = reclass(pattern, line, img, rects);    
[tmp_line, index] = get_line_from_patterns(pattern);
line = [tmp_line; line];
imshow(img), hold on, draw_patterns(boxes, [1 0 0]);
hold on, draw_patterns(line, [0 1 0]);

%I also run the region formation part in advance to save time for checking and store the %results in the matrix post3block. You can also run the following code to get the same %result:
load('post3');    
[boxes, delete] = generate_boxes(pattern);
[Aline, pattern] = extract_line_boxes(pattern, boxes, delete, 1);
line = Aline;
[pattern, line] = reclass(pattern, line, img, rects);
blocks = regionform(pattern);

%get figure 8
load('post3block');
blocks = cleanregion(blocks, 15, 0);
blocks = dealwithblocks(blocks);
lineblk = changeline2blk(line);
blocks = [blocks; lineblk];
blocks = cleanlineintext(blocks);
[title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blocks);
imshow(img), hold on, draw_patterns(title_block, [0 0 0], 2);
draw_patterns(txt_block, [0 0 0], 2);

%get figure 9
load('post3block');
blocks = cleanregion(blocks, 15, 0);
blocks = dealwithblocks(blocks);
lineblk = changeline2blk(line);
blocks = [blocks; lineblk];
blocks = cleanlineintext(blocks);
imshow(img), hold on, draw_patterns(blocks, [0 0 0], 2);


Main Function Introduction:
0. The function main.m could directly run to produce the final results of the newspaper ’To Bama’. It should take less than 2 minutes.
1. rects = locate_rects(img) can find most of the black pixels in the original binary newspaper image and generate rects around the black pixels. The input argument img is a binary image. The output argument is a set of rects.
2. patterns = generate_patterns(rects) can group adjacent rects into patterns, the input argument is rects, and the output argument is a set of patterns.
3. patterns = pattern_classify(pattern, img) can classify the patterns based on the criteria descried in the approach and return the classified patterns.
3. generate_boxes(pattern) can find the boxes from the input argument pattern, and the output argument is a set of boxes.
4. [Aline, pattern] = extract_line_boxes(pattern, boxes, delete,  1) can extract the edge lines from the boxes and replace the original boxes with new line patterns. The input argument delete is the index for the boxes in the patterns, and the input argument 1 is the threshold to discard the edge lines of boxes which has less threshold number of rects.
5. [pattern, line] = reclass(pattern, line, img, rects) can do the line reconstruction. The input argument line is what we got after pattern classification. The output argument line is the lines reconstructed from the input lines and the pattern is the reclassification of the rects that are not from the reconstructed lines.
6. blocks = cleanregions(blocks, 15, 0) can deal with the misclassification of different types of blocks. If one block is found near over a threshold number of blocks with the same type or within another block, the type of this block will switch to the majority or the outside block. 15 is the threshold to determine whether two blocks is far away enough. 0 represents strict less than(<), 1 means less or equal than(<=).
7. blocks = dealwithblocks(blocks) simply combine the function cleanregions and other functions to get a satisfactory result.
8. blocks = cleanlineintext(blocks) is similar to cleanregions. It is used to remove lines from title blocks and text blocks.
