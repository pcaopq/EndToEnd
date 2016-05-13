function blocks = cleanlineintext(blocks)
    [title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blocks);
    [vline, hline, index_vline, index_hline] = get_lineblk(blocks);
    blocks([titleindex; txtindex; index_vline; index_hline]) = [];
    line = [vline; hline];
    num_ln = size(line, 1);
    num_tb = size(txt_block, 1);
    num_te = size(title_block, 1);
    delete = [];
    
    for i = 1:num_ln
        for j = 1:num_tb    
            if insideblk(line(i), txt_block(j), 0, 1)
                delete = [delete; i];
            end
        end
        
        for j = 1:num_te    
            if insideblk(line(i), title_block(j), 5, 1) && line(i).para.width < 50 && line(i).para.height < 50
                delete = [delete; i];
            end
        end        
    end
    
    line(delete) = [];
    blocks = [blocks; line; title_block; txt_block];
end