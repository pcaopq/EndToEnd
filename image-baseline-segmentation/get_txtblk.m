function [titleblk, index_title, txtblk, index_txt, title_avh, txt_avh] = get_txtblk(blocks)
    num_blocks = size(blocks, 1);
    txt_height = [];
    title_height = [];
    txtblk = [];
    titleblk = [];
    index_txt = [];
    index_title = [];
%     title_avh = 0;
%     txt_avh = 0;
    for i = 1:num_blocks
        if blocks(i).type == 1
            txtblk = [txtblk; blocks(i)];
%             txt_avh = txt_avh + blocks(i).para.height;
            txt_height = [txt_height; blocks(i).para.height];
            index_txt = [index_txt; i];
        elseif blocks(i).type == 2
            titleblk = [titleblk; blocks(i)];
%             title_avh = title_avh + blocks(i).para.height;
            title_height = [title_height; blocks(i).para.height];
            index_title = [index_title; i];
        end
    end
%     title_avh = title_avh/size(index_title, 1);
%     txt_avh = txt_avh/size(index_txt, 1);
    [value_txt, ~] = sort(txt_height, 'ascend');
    start = ceil(1/4*size(index_txt, 1));
    End = ceil(3/4*size(index_txt, 1));
    
    txt_avh = sum(value_txt(start:End))/(End-start+1);
    
    [value_title, ~] = sort(title_height, 'ascend');
    start = ceil(1/4*size(index_title, 1));
    End = ceil(3/4*size(index_title, 1));
    title_avh = sum(value_title(start:End))/(End-start+1);
end