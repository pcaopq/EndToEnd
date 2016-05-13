function lineblk = changeline2blk(line)
    num_lines = size(line, 1);
    lineblk = [];
    for i = 1:num_lines
        b = struct('patterns',struct(...
                'rects', struct('left', [], 'top', [], 'right', [], 'bottom', []),...
                'para', struct('left', [], 'top', [], 'right', [], 'bottom', [], 'width', [], 'height', [], 'area', [], 'bp_density', [], 'num_bp', [], 'nbr', [], 'mbrl', [],'sp', [], 'vbrl', []),...
                'type', []), 'para',struct('left', [], 'right', [], 'bottom', [], 'top', [], 'width', [], 'height', [], 'area', []), 'type', []);    
        b.patterns.rects = line(i).rects;
        b.patterns.para = line(i).para;
        b.patterns.type = line(i).type;
        b.para = line(i).para;
        b.type = line(i).type;
        lineblk = [lineblk; b];
    end
end