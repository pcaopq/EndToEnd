function flag = insideblk(blockA, blockB, threshold, strict)
    flag = 0;
%     right = max(blockA.para.right, blockB.para.right);
%     left = min(blockA.para.left, blockB.para.left);
%     bottom = max(blockA.para.bottom, blockB.para.bottom);
%     top = min(blockA.para.top, blockB.para.top);
%     width = blockA.para.width + blockB.para.width - (right - left);
%     height = blockA.para.height + blockB.para.height - (bottom - top);
%     area = width * height;
%     if area >= min(blockA.para.area, blockB.para.area)*1/2 && width > 0 && height > 0
%        flag = 1; 
%     end
    if ~strict
        if (blockA.para.right<=blockB.para.right + threshold && blockA.para.left>=blockB.para.left - threshold &&...
                blockA.para.top>=blockB.para.top - threshold && blockA.para.bottom<=blockB.para.bottom+threshold)
            flag = 1;
        end
    else
        if (blockA.para.right<blockB.para.right + threshold && blockA.para.left>blockB.para.left - threshold &&...
                blockA.para.top>blockB.para.top - threshold && blockA.para.bottom<blockB.para.bottom+threshold)
            flag = 1;
        end        
    end
end