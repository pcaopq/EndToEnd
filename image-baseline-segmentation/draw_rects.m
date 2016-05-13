function draw_rects(rects, color, linewidth)
    set(gca, 'YDir', 'reverse');
    for i = 1:size(rects, 2)
        rectangle('position', [rects(i).left rects(i).top  rects(i).right-rects(i).left rects(i).bottom-rects(i).top], 'EdgeColor', color,...
            'linewidth', linewidth);
    end
end

