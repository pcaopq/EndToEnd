function pattern = pattern_classify(pattern, img, show_patterns, save_flag, name)
    % clear, clc
    % load('pattern_img_0033_classifed.mat');
%     img = imread('smaller1.jpg');
%     img = imread(related_img);
%     img = im2bw(img, 0.7);
    pattern = get_pattern_para(pattern, img);

    %estimate he
    index = [];
    he = 0;
    for i = 1:size(pattern, 1)
        tmp_height = pattern(i).para.bottom - pattern(i).para.top;
        if tmp_height<25
            index = [index; i];
            he = he + tmp_height;
        end
    end
    he = he/size(index, 1);

    %parameter definition
    %DD                  %DI               %Ratios
    A1 = 400*he*he;      A2 = 32;          alpha = 0.75;
    A3 = 80*he*he;       B = 16;           beta = 0.04;
    A4 = 64*he*he;       S1 = 350;         kapa = 1.4;
    D = 5*he;            S2 = 500;         lambda1 = 0.16;
    H = 0.7*he;          V = 5.5;          lambda2 = 0.1;
    L = 3.0*he;                            lambda3 = 0.13;
    W1 = 1.5*he;                           rho0 = 0.3;
    W2 = 10*he;                            rho1 = 0.72;
                                           rho2 = 0.5;
                                           rho3 = 1.65;
    %type 1:1 Text 2 Title 3 Inverse text 4 Photograph 5 Graphic/drawing 6 Vertical line 7 Horizontal line 8 Small

    %Rule A Large Patterns
    index_large_patterns = [];
    for i = 1:size(pattern, 1)
        if pattern(i).para.area > A1 && pattern(i).para.width>D && pattern(i).para.height>D
            index_large_patterns = [index_large_patterns; i];
        end
    end

    %Rule B Photograph or Graphic
    index_photograph = [];
    index_graph = [];
    for i = 1:size(index_large_patterns, 1)                        %added constraint besides paper
        if pattern(index_large_patterns(i)).para.bp_density > rho0 && pattern(index_large_patterns(i)).para.num_bp > 30000
            pattern(index_large_patterns(i)).type = 4;
            index_photograph = [index_photograph; index_large_patterns(i)];
        else
            pattern(index_large_patterns(i)).type = 5;
            index_graph = [index_graph; index_large_patterns(i)];
        end
    end

    %Rule C Small Patterns
    index = (1:size(pattern, 1))';
    index(index_large_patterns) = [];
    index_small_patterns = [];
    delete = [];
    for i = 1:size(index, 1)
        if pattern(index(i)).para.num_bp < B && pattern(index(i)).para.area < A2
            pattern(index(i)).type = 8;
            index_small_patterns = [index_small_patterns; index(i)];
            delete = [delete; i];
        end
    end

    %Rule D Vertical Lines
    index_vertical_lines = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        h = pattern(index(i)).para.height;
        if h > L && pattern(index(i)).para.width < min(lambda1*h, W1)
            pattern(index(i)).type = 6;
            index_vertical_lines = [index_vertical_lines; index(i)];
            delete = [delete; i];
        end
    end

    %Rule E Vertical long thick lines
    index_vlt_lines = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        w = pattern(index(i)).para.width;
        h = pattern(index(i)).para.height;
        if w >= W1 && w < lambda2*h
            pattern(index(i)).type = 6;
            index_vlt_lines = [index_vlt_lines; index(i)];
            delete = [delete; i];
        end
    end

    %Rule F Horizontal Lines
    index_horizontal_lines = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        w = pattern(index(i)).para.width;
        h = pattern(index(i)).para.height;
        d = pattern(index(i)).para.bp_density;
        m = pattern(index(i)).para.mbrl;
        if w>L && h<min(lambda1*w, W1)
            if h < H || h < lambda3*w || m > 2*h || d > rho1
                pattern(index(i)).type = 7;
                index_horizontal_lines = [index_horizontal_lines; index(i)];
                delete = [delete i];
            end
        end
    end

    %Rule G Thick Horizontal Lines
    index_th_lines = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        w = pattern(index(i)).para.width;
        h = pattern(index(i)).para.height;
        if h >= W1 && h < lambda2*w
            pattern(index(i)).type = 7;
            index_th_lines = [index_th_lines; index(i)];
            delete = [delete; i];
        end
    end

    %Rule H Photographs
    index_ps = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        a = pattern(index(i)).para.area;
        n = pattern(index(i)).para.nbr;
        if a > A3 && n > beta*a
            pattern(index(i)).type = 4;
            index_ps = [index_ps index(i)];
            delete = [delete; i];
        end
    end

    %Rule I Graphics
    index_gs = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        a = pattern(index(i)).para.area;
        s = pattern(index(i)).para.sp;
        v = pattern(index(i)).para.vbrl;
        if a < A4 && s > S1 && v > V
            pattern(index(i)).type = 5;
            index_gs = [index_gs; index(i)];
            delete = [delete; i];
        end
    end

    %Rule J Graphics in larger patterns
    index_gslp = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        a = pattern(index(i)).para.area;
        s = pattern(index(i)).para.sp;
        d = pattern(index(i)).para.bp_density;
        if a >= A4 && s > S2 && d < rho2
            pattern(index(i)).type = 5;
            index_gslp = [index_gslp; index(i)];
            delete = [delete; i];
        end
    end

    %Rule K Inverse Text
    index_it = [];
    index(delete) = [];
    delete = [];
    for i = 1:size(index, 1)
        w = pattern(index(i)).para.width;
        m = pattern(index(i)).para.mbrl;
        d = pattern(index(i)).para.bp_density;
        if w > W2 && d > rho3 && m > alpha*w
            pattern(index(i)).type = 3;
            index_it = [index_it; index(i)];
            delete = [delete; i];
        end
    end

    %recalculate ht
    index(delete) = [];
    ht = 0;
    for i = 1:size(index, 1)
        ht = ht + pattern(index(i)).para.height;
    end
    ht = ht/size(index, 1);

    %Rule L Text or Title
    index_tt = [];
    delete = [];
    for i = 1:size(index, 1)
        h = pattern(index(i)).para.height;
        w = pattern(index(i)).para.width;
    %     if h > kapa*ht && pattern(index(i)).para.bp_density > 0.5 && w > 20
        if h > kapa*ht && pattern(index(i)).para.bp_density > 0.5 && w > 10
            pattern(index(i)).type = 2;
            index_tt = [index_tt; index(i)];
            delete = [delete; i];
        end
    end

    %the remains are all texts 
    %index works for texts now
    index(delete) = [];
    for i = 1:size(index, 1)
        pattern(index(i)).type = 1;
    end
    if nargin == 3
%         save('pattern_img_0033_classifed', 'pattern');
          save(name, 'pattern');
    end
    if nargin == 5
        imshow(img), hold on;
        for type = 2:2
            draw_patterns(pattern, [rand(1) rand(1) rand(1)], type);
        end
    end
end