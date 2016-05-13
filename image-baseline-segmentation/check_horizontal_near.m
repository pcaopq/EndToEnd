function rst = check_horizontal_near(rectA, rects, threshold)
    num_rects = size(rects, 2);
    rst = 0;
    for i=1:num_rects
        width = max(rectA.right, rects(i).right)-min(rectA.left, rects(i).left);
        if width <= rectA.right-rectA.left+rects(i).right-rects(i).left+threshold
            rst = 1;
            return;
        end
    end
end