function blockA = merge_blocks(blockA, blockB)
    num_patterns = size(blockB.patterns, 2);
    for i = 1:num_patterns
        blockA.patterns = [blockA.patterns blockB.patterns(i)];
    end
    blockA = get_block_para(blockA);
end