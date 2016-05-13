function  [rst, delete] = formetablk2(title_block, txt_block, title_hgap, title_vgap, txt_hgap, txt_vgap)
    %text is misclassified as title
    num_tb = size(txt_block, 1);
    num_te = size(title_block, 1);
    metablock = [];
%     flag = zeros(num_tb, 1);
    rst = [];
    hgap = title_hgap;
    vgap = title_vgap;
    flag = zeros(num_te, 1);
    similar = 0;
    delete = [];
    for i = 1:num_tb
         i
%         if flag(i)
%             continue;
%         end
        
        patterni = txt_block(i).patterns;

        metablock = [metablock; txt_block(i)];
        for j = 1:num_te   
            
            if flag(j)
                continue;
            end
            
            patternj = title_block(j).patterns;
%             break_flag = 0;
            
            for m = 1:size(patterni, 2)
                for n = 1:size(patternj, 2)
%                     if patterni(m).para.top < patternj(n).para.bottom && patterni(m).para.bottom > patternj(n).para.top
                        if abs(patterni(m).para.left - patternj(n).para.right) < hgap || abs(patterni(m).para.right - patternj(n).para.left) < hgap
%                             flag(i) = 1;
                            flag(j) = 1;
                            similar = similar + 1;
                        end
%                     end
                end
            end
        end
        
        if flag(j)
            metablock = [metablock; title_block(j)];
            if similar > 5
               metablock(1).type = 2;
            end
            delete = [delete; i];
        end
        
        rst = [rst; metablock];
        metablock = [];
        similar = 0;
     end
end
