function [rst, bid] = getblocks(blocks, type)
    num_blocks = size(blocks, 1);
    bid = [];
    for i = 1:num_blocks
        if blocks(i).type == type
            bid = [bid; i];
        end
    end
    rst = blocks(bid);
end

