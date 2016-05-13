function blocks = cleanregion(blocks, threshold, strict)
    num_blocks = size(blocks, 1);
    flag = zeros(num_blocks, 1);
    delete = [];
    
    for i = 1:num_blocks
        if flag(i)
            continue;
        end
        for j = 1:num_blocks    
            
            if flag(j) || j == i
                continue;
            end
            
            if insideblk(blocks(j), blocks(i), threshold, strict)
                flag(j) = 1;
                delete = [delete; j];
            end
            
            if insideblk(blocks(i), blocks(j), threshold, strict)
                flag(i) = 1;
                delete = [delete; i];
            end
            
        end
    end
    blocks(delete) = [];
end