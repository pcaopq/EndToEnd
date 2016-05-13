function [vline, hline, index_vline, index_hline] = get_lineblk(blocks)
    num_blocks = size(blocks, 1);
    hline = [];
    vline = [];
    index_hline = [];
    index_vline = [];
%     title_avh = 0;
%     txt_avh = 0;
    for i = 1:num_blocks
        if blocks(i).type == 6 %vline
            hline = [hline; blocks(i)];
%             txt_avh = txt_avh + blocks(i).para.height;
            index_hline = [index_hline; i];
        elseif blocks(i).type == 7 %hline
            vline = [vline; blocks(i)];
%             title_avh = title_avh + blocks(i).para.height;
            index_vline = [index_vline; i];
        end
    end
end