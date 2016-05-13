function rst = merge_titles(blocks)
    num_titles = size(blocks, 1);
    flag = zeros(num_titles, 1);
    IWF = 1.05;
    ILF = 0.75;
    delete = [];
    
    for i = 1:num_titles
        if flag(i)
            continue;
        end
        
        hA = get_BlockH(blocks(i).patterns);
        patterni = blocks(i).patterns;
        
        for j = i+1:num_titles
            if flag(j)
                continue;
            end
            hB = get_BlockH(blocks(j).patterns);
            hgap = 20*IWF * min(hA, hB) * min(hA, hB)/max(hA, hB); 
            vgap = 1.5*ILF * min(hA, hB) * min(hA, hB)/max(hA, hB);
            patternj = blocks(j).patterns;
            break_flag = 0;
            
            for m = 1:size(patterni, 2)
                for n = 1:size(patternj, 2)
                    if abs(patterni(m).para.right - patternj(n).para.left) <= hgap || abs(patterni(m).para.left - patternj(n).para.right) <= hgap || abs(patterni(m).para.left - patternj(n).para.right) <= 10
                        if abs(patterni(m).para.bottom - patternj(n).para.top) <= vgap || abs(patterni(m).para.top - patternj(n).para.bottom) <= vgap || abs(patterni(m).para.top - patternj(n).para.bottom) <= 10
                            blocks(i) = merge_blocks(blocks(i), blocks(j));
                            flag(j) = 1;
                            flag(i) = 1;
                            break_flag = 1;
                            delete = [delete; j];
                            break;
                        end
                    end
                    if break_flag
                        break;
                    end
                end
                if break_flag
                    break;
                end
            end
        end
    end
        blocks(delete) = [];
        rst = blocks;    
end

