function  [title_block, txt_block, blocks] = formetablk(blocks)
    [title_block, titleindex, txt_block, txtindex, title_avh, txt_avh] = get_txtblk(blocks);
    [lineblk] = get_lineblk(blocks);
    blocks([titleindex;txtindex]) = [];
    
    title_hgap = 1.1*title_avh;
    title_vgap = 0.8*title_avh;
    txt_hgap = 1.1*txt_avh;
    txt_vgap = 0.8*txt_avh;
    num_tb = size(txt_block, 1);
    num_te = size(title_block, 1);
    delete = [];
    
    for i = 1:num_tb
        if txt_block(i).para.area < 1000
            txt_block(i).type = 2;
            title_block = [title_block; txt_block(i)];
            delete = [delete; i];
        end
    end
        txt_block(delete) = [];
    
        delete = [];
        num_te = size(title_block, 1);
        for i = 1:num_te
            count = 0;
            for j = 1:num_te
                if j == i
                    continue;
                end
                if check_tt_near(title_block(i).para, title_block(j).para, title_hgap, title_vgap)
                    count = count + 1;
                end
            end
            if ~count
                title_block(i).type = 1;
                txt_block = [txt_block; title_block(i)];
                delete = [delete; i];
            end
        end
        title_block(delete) = [];
        
% %     metablock = [];
%     rst = [];
%     hgap = txt_hgap;
% %     hgap = 100;
%     vgap = txt_vgap;
%     flag = zeros(num_tb, 1);
%     similar = 0;
%     delete = [];
%     for i = 1:num_te
%         i
%         patterni = title_block(i).patterns;
%         for j = 1:num_tb       
%             
% %             if flag(j)
% %                 continue;
% %             end
%             
%             patternj = txt_block(j).patterns;
%             break_flag = 0;
%             
%             for m = 1:size(patterni, 2)
%                 for n = 1:size(patternj, 2)
%                   if abs(1/2*(patterni(m).para.top + patterni(m).para.bottom) - 1/2*(patternj(n).para.top + patternj(n).para.bottom)) < txt_avh                   
%                     if abs(patterni(m).para.left - patternj(n).para.right) < hgap || abs(patterni(m).para.right - patternj(n).para.left) < hgap
% %                         flag(j) = 1;
%                         similar = similar + 1;
%                     end
%                   end
%                 end
%             end
%             
% %              if flag(j)
%                 if similar > 11 || title_block(i).para.width * title_block(i).para.height < 1500
%                     title_block(i).type = 1;
%                     delete = [delete; i];
%                     break;
%                 end
% %              end 
%              similar = 0;
%              
%         end    
%     end
%     
%     txt_block = [txt_block; title_block(delete)];
%     title_block(delete) = [];
%     
%     %text在标题里
%     [title_block, ~, txt_block, ~, title_avh, txt_avh] = get_txtblk([txt_block; title_block]);
%     title_hgap = 1.1*title_avh;
%     title_vgap = 0.8*title_avh;
%     txt_hgap = 1.1*txt_avh;
%     txt_vgap = 0.8*txt_avh;
%     num_tb = size(txt_block, 1);
%     num_te = size(title_block, 1);
%     flag = zeros(num_tb, 1);
% %     hgap = title_hgap;
%     hgap = 20;
% %     hgap = 100;
%     vgap = title_vgap;
%     
%     flag = zeros(num_te, 1);
%     similar = 0;
%     
%     delete = [];
%     for i = 1:num_tb
%         i
%         patterni = txt_block(i).patterns;
%         for j = 1:num_te       
%             
% %             if flag(j)
% %                 continue;
% %             end
%             
%             patternj = title_block(j).patterns;
%             for m = 1:size(patterni, 2)
%                 for n = 1:size(patternj, 2)
%                   if  abs(1/2*(patterni(m).para.top + patterni(m).para.bottom) - 1/2*(patternj(n).para.top + patternj(n).para.bottom)) < 5
%                     if abs(patterni(m).para.left - patternj(n).para.right) < hgap || abs(patterni(m).para.right - patternj(n).para.left) < hgap
% %                         flag(j) = 1;
%                         similar = similar + 1;
%                     end
%                   end
%                 end
%             end
%         if similar > 10
%             txt_block(i).type = 2;
%             delete = [delete; i];
%             break;
%         end
%         similar = 0;
%         end
%     end
%     
%     title_block = [title_block; txt_block(delete)];
%     txt_block(delete) = [];
end
