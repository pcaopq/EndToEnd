function rst = check_near(rectA, rects, threshold)
    num_rects = size(rects, 2);
    rst = 0;
    for i=1:num_rects
        width = max(rectA.right, rects(i).right)-min(rectA.left, rects(i).left);
        height = max(rectA.bottom, rects(i).bottom)-min(rectA.top, rects(i).top);
        if width <= rectA.right-rectA.left+rects(i).right-rects(i).left+threshold &&...
                height <= rectA.bottom-rectA.top+rects(i).bottom-rects(i).top+threshold
            rst = 1;
            return;
        end
    end
end