{\rtf1\ansi\ansicpg936\cocoartf1404\cocoasubrtf130
{\fonttbl\f0\fmodern\fcharset0 Courier;\f1\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red255\green0\blue0;\red160\green32\blue240;\red0\green0\blue255;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs20 \cf2 %The function locate_rects and pattern_classify needs large amount of time(about 30 %minutes), so I ran them in advance and store the matrices in post3. So you can simply %load them to get the results. You can also run them manually by: \
\cf0 \
clear, clc
\fs24 \

\fs20 img = imread(\cf3 'post3.jpg'\cf0 );
\fs24 \

\fs20 img = im2bw(img, 0.7);
\fs24 \

\fs20 rects = locate_rects(img);
\fs24 \

\fs20 pattern = generate_patterns(rects);
\fs24 \

\fs20 pattern = pattern_classify(pattern, img);
\fs24 \

\fs20 %The results are three matrices which are rects, img and classified pattern.\
\
\cf2 %Prepocessing\
\cf0 clear, clc
\fs24 \

\fs20 img = imread(\cf3 'post3.jpg'\cf0 );
\fs24 \

\fs20 img = im2bw(img, 0.7);\

\fs24 \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardeftab720\pardirnatural\partightenfactor0

\fs20 \cf2 %The figures are in ReadMe.doc
\f1\fs24 \cf0 \

\f0\fs20 \cf2 %get figure 4 \
\cf0 load(\cf3 'post3'\cf0 ); imshow(img), hold on, draw_rects(rects, [0 0 1], 1);\

\fs24 \

\fs20 \cf2 %get figure 6\
\cf0 load(\cf3 'post3'\cf0 ); imshow(img), hold on, draw_patterns(pattern, [0 0 1]); \
\
\cf2 %get figure 7\
\cf0 load(\cf3 'post3'\cf0 ); imshow(img), hold on, draw_patterns(pattern); \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardeftab720\pardirnatural\partightenfactor0

\f1\fs24 \cf0 \
\pard\pardeftab720\partightenfactor0

\f0\fs20 \cf2 %get lines\
\cf0 load(\cf3 'post3'\cf0 );    
\fs24 \

\fs20 [boxes, delete] = generate_boxes(pattern);    
\fs24 \

\fs20 [Aline, pattern] = extract_line_boxes(pattern, boxes, delete, 1);    
\fs24 \

\fs20 line = Aline;
\fs24 \

\fs20 [pattern, line] = reclass(pattern, line, img, rects);    
\fs24 \

\fs20 [tmp_line, index] = get_line_from_patterns(pattern);
\fs24 \

\fs20 line = [tmp_line; line];\
imshow(img), hold on, draw_patterns(boxes, [1 0 0]);\
hold on, draw_patterns(line, [0 1 0]);
\fs24 \
\

\fs20 \cf2 %I also run the region formation part in advance to save time for checking and store the %results in the matrix post3block. You can also run the following code to get the same %result:\cf0 \
load(\cf3 'post3'\cf0 );    \
[boxes, delete] = generate_boxes(pattern);
\fs24 \

\fs20 [Aline, pattern] = extract_line_boxes(pattern, boxes, delete, 1);
\fs24 \

\fs20 line = Aline;
\fs24 \

\fs20 [pattern, line] = reclass(pattern, line, img, rects);
\fs24 \

\fs20 blocks = regionform(pattern);
\fs24 \

\fs20 \
\cf2 %get figure 8\
\cf0 load(\cf3 'post3block'\cf0 );\
blocks = cleanregion(blocks, 15, 0);
\fs24 \

\fs20 blocks = dealwithblocks(blocks);\
lineblk = changeline2blk(line);
\fs24 \

\fs20 blocks = [blocks; lineblk];
\fs24 \

\fs20 blocks = cleanlineintext(blocks);\
[title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blocks);
\fs24 \

\fs20 imshow(img), hold on, draw_patterns(title_block, [0 0 0], 2);\
draw_patterns(txt_block, [0 0 0], 2);
\fs24 \
\

\fs20 \cf2 %get figure 9\
\cf0 load(\cf3 'post3block'\cf0 );
\fs24 \

\fs20 blocks = cleanregion(blocks, 15, 0);
\fs24 \

\fs20 blocks = dealwithblocks(blocks);\
lineblk = changeline2blk(line);
\fs24 \

\fs20 blocks = [blocks; lineblk];
\fs24 \

\fs20 blocks = cleanlineintext(blocks);\
imshow(img), hold on, draw_patterns(blocks, [0 0 0], 2);
\fs24 \
\
\
\pard\pardeftab720\partightenfactor0
\cf4 Main Function Introduction:\
\cf2 0. The function main.m could directly run to produce the final results of the newspaper \'92To Bama\'92. It should take less than 2 minutes.\
\pard\pardeftab720\partightenfactor0
\cf0 1. rects = locate_rects(img) can find most of the black pixels in the original binary newspaper image and generate rects around the black pixels. The input argument img is a binary image. The output argument is a set of rects.\
2. patterns = generate_patterns(rects) can group adjacent rects into patterns, the input argument is rects, and the output argument is a set of patterns.\
3. patterns = pattern_classify(pattern, img) can classify the patterns based on the criteria descried in the approach and return the classified patterns.\
3. generate_boxes(pattern) can find the boxes from the input argument pattern, and the output argument is a set of boxes.\
4. [Aline, pattern] = extract_line_boxes(pattern, boxes, delete,  1) can extract the edge lines from the boxes and replace the original boxes with new line patterns. The input argument delete is the index for the boxes in the patterns, and the input argument 1 is the threshold to discard the edge lines of boxes which has less threshold number of rects.\
5. [pattern, line] = reclass(pattern, line, img, rects) can do the line reconstruction. The input argument line is what we got after pattern classification. The output argument line is the lines reconstructed from the input lines and the pattern is the reclassification of the rects that are not from the reconstructed lines.\
6. blocks = cleanregions(blocks, 15, 0) can deal with the misclassification of different types of blocks. If one block is found near over a threshold number of blocks with the same type or within another block, the type of this block will switch to the majority or the outside block. 15 is the threshold to determine whether two blocks is far away enough. 0 represents strict less than(<), 1 means less or equal than(<=).\
7. blocks = dealwithblocks(blocks) simply combine the function cleanregions and other functions to get a satisfactory result.\
8. blocks = cleanlineintext(blocks) is similar to cleanregions. It is used to remove lines from title blocks and text blocks.}