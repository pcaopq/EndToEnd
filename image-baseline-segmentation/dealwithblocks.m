function blocks = dealwithblocks(blocks)
    [titleblk, txtblk, blocks] = formetablk(blocks);
    titleblk1 = merge_titles(titleblk);
    titleblk1 = cleanregion(titleblk1, 15, 0);
    
    for i = 1:10
        titleblk1 = merge_titles(titleblk1);
    end
    
    blk = cleanregion([titleblk1; txtblk], 15, 0);
%     [titleblk, txtblk] = mergett(blk);
    
    
    delete = [];
    [title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blk);
    for i = 1:size(titleindex)    
        if size(title_block(i).patterns, 2) < 5
            delete = [delete; i];
            title_block(i).type = 1;
            txt_block = [txt_block; title_block(i)];
        end
    end
    title_block(delete) = [];
    
    num_tb = size(txt_block, 1);
    num_te = size(title_block ,1);
    delete = [];
    for i = 1:num_tb
        count = 0;
        for j = 1:num_te
            if check_near(txt_block(i).para, title_block(j).para, 20)
                count = count + 1;
            end
        end
        if count >= 2
            delete  = [delete; i];
            txt_block(i).type = 2;
            title_block = [title_block; txt_block(i)];
        end
    end
    txt_block(delete) = [];
    for i = 1:5
        title_block = merge_titles(title_block);
    end
    
    blocks = [blocks; title_block; txt_block;];
    
    blocks = cleanregion(blocks, 15, 0);
    
    
    num_blks = size(blocks, 1);
    for i = 1:num_blks
        if blocks(i).para.width>10*blocks(i).para.height && blocks(i).para.height < 10 && blocks(i).para.width > 50
            blocks(i).type = 7;
        end
        if blocks(i).para.height>10*blocks(i).para.width && blocks(i).para.width < 10 && blocks(i).para.height > 50
            blocks(i).type = 6;
        end
    end
end