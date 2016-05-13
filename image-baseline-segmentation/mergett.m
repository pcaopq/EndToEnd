function [title_block, txt_block] = mergett(blocks)
    [title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blocks);
    num_tb = size(txtindex, 1);
    num_te = size(titleindex, 1);

    delete = [];
    for i = 1:num_te
        for j = 1:num_tb
            if check_near(title_block(i).para, txt_block(j).para, 10)
                delete = [delete; i];
                title_block(i).type = 1;
                txt_block = [txt_block; title_block(i)];
            end
        end
    end
    title_block(delete) = [];
end