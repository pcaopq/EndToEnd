function rst = near(x, y, hgap, vgap, factor)
    rst = false;
    rectX = struct('top', [], 'bottom', [], 'right', [], 'left', []);
    rectY = struct('top', [], 'bottom', [], 'right', [], 'left', []);    
    rectX.left = x.left; rectX.right = x.right; rectX.top = x.top; rectX.bottom = x.bottom;
    rectY.left = y.left; rectY.right = y.right; rectY.top = y.top; rectY.bottom = y.bottom;
    if x.left < y.right + factor*hgap && x.right > y.left - factor*hgap
        if x.top < y.bottom + factor*vgap && x.bottom > y.top - factor*vgap
            rst = true;
            return;
        end
    end
    if x.left >= y.left && x.right <= y.right && x.top >= y.top && x.bottom <= y.bottom
        rst = true;
        return;
    end
    if y.left >= x.left && y.right <= x.right && y.top >= x.top && y.bottom <= x.bottom
        rst = true;
        return;
    end    
    if check_near(rectX, rectY, hgap) || check_near(rectY, rectX, vgap)
        rst = true;
        return;
    end
end

