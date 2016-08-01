//
//  main.cpp
//  imageSeg
//
//  Created by Panfeng Cao on 16/6/14.
//  Copyright © 2016年 Panfeng Cao. All rights reserved.
//
#include "imageseg.h"
#include "tinyxml2.cpp"
using namespace cv;

string imgname = "0281";
cv::Mat image_ori0 = cv::imread(imgname+".jpg", 0);
cv::Mat image_ori;
cv::Mat image;
cv::Mat imageBGR;
int height;
int width;

int search_right(int x, int y, int xstep){
    for(int j = y;j<=min(y+2, height);j++){
        for(int i = min(x+2, width);i >= x + 3 - xstep; i--){
            if(!(int)image.at<uchar>(j-1, i-1)){
                return i-x+1;
            }
        }
    }
    return 0;
}

int lowest_row(rect R){
    for(int i = min(R.top+2, height);i>=R.top;i--){
        for(int j = R.left;j<=min(R.right, width);j++)
            if(!(int)image.at<uchar>(i-1, j-1))
                return i - R.top + 1;
    }
    return 0;
}

bool checksquare(int i, int j){
//    sum(sum(img(i:i+2,j:j+2).*ones(3,3))) == 9
    if((int)image.at<uchar>(i, j) && (int)image.at<uchar>(i+1, j) && (int)image.at<uchar>(i+2, j) && (int)image.at<uchar>(i, j+1) && (int)image.at<uchar>(i, j+2) && (int)image.at<uchar>(i+1, j+1) && (int)image.at<uchar>(i+1, j+2) && (int)image.at<uchar>(i+2, j+1) && (int)image.at<uchar>(i+2, j+2))
        return true;
    else
        return false;
}

int search_below(rect R, int ry, int ystep){
    for(int i = ry + 2;i>=ry+3-ystep;i--){
        for(int j = R.left;j<=min(R.right, width)-2;j++)
            if(i+2>height || checksquare(i-1, j-1))
                return 0;
    }
    R.top = ry;
    return lowest_row(R);
}

vector<rect> locate_rects(){
    int x = 1, y = 1, xstep = 3;
    int ystep, ry;
    vector<rect> ret;
    while(y <= height && x <= width){
        if(xstep == search_right(x, y, xstep)){
            rect tmp;
            tmp.left = x;
            tmp.top = y;
            x = x+xstep;
            while(xstep == search_right(x, y, xstep))
                x = x+xstep;
            tmp.right = min(x, width);
            ystep = lowest_row(tmp);
            ry = y + ystep;
            while(ystep == search_below(tmp, ry, ystep))
                ry += ystep;
            tmp.bottom = min(ry, height);
            ret.push_back(tmp);
        }
        else
            x += 3;
        if(x >= width){
            x = 1;
            y += 3;
        }
    }
    cout<<"The total number of rects is: "<<ret.size()<<endl;
    cout<<"The estimated time for generating the patterns is: "<<(float)ret.size()/650<<"s"<<endl;
    return ret;
}

bool check_near(rect rectA, vector<rect> rects, int wthreshold, int hthreshold){
    long num_rects = rects.size();
    int width, height;
    for(int i = 0;i < num_rects;i++){
        width = max(rectA.right, rects[i].right)-min(rectA.left, rects[i].left);
        height = max(rectA.bottom, rects[i].bottom)-min(rectA.top, rects[i].top);
        if(width <= rectA.right-rectA.left+rects[i].right-rects[i].left+wthreshold && height <= rectA.bottom-rectA.top+rects[i].bottom-rects[i].top+hthreshold)
            return true;
    }
    return false;
}

vector<pattern> generate_patterns(vector<rect> rects){
    vector<pattern> ret;
    pattern tmp;
    long num_patterns;
    long num_rects = rects.size();
    tmp.rects.push_back(rects[0]);
    ret.push_back(tmp);
    vector<int> todel;
    int rects_count = 1;
    while(rects_count < num_rects){
        num_patterns = ret.size();
        for(int i = 1;i<=num_patterns;i++){
            if(check_near(rects[rects_count], ret[i-1].rects, 1, 1))
                todel.push_back(i - 1);
        }
        if(todel.size() == 1)
            ret[todel.front()].rects.push_back(rects[rects_count]);
        else if(todel.size() > 1){
            pattern tmp;
            tmp.rects.push_back(rects[rects_count]);
            for(auto i = todel.rbegin();i!=todel.rend();i++){
                for(auto j:ret[*i].rects)
                    tmp.rects.push_back(j);
                ret.erase(ret.begin() + *i);
            }
            ret.push_back(tmp);
        }
        else{
            pattern tmp;
            tmp.rects.push_back(rects[rects_count]);
            ret.push_back(tmp);
        }
        rects_count++;
        cout<<rects_count<<endl;
        todel.clear();
    }
    cout<<"The total number of patterns is "<<ret.size()<<endl;
    cout<<"The estimated time for generating the blocks is "<<(float)ret.size()/250<<"s"<<endl;
    return ret;
}

void mbprl(int left, int right, int top, int bottom, int& mbrl, int& nbr, float& vbrl){
    int start, p;
    int len;
    int tmp_width = right-left+1;
    int tmp_height = bottom-top+1;
    vector<vector<int>> length(tmp_height, vector<int>(tmp_width, 0));
//    int length[tmp_height][tmp_width];
    for(int i = top;i <= bottom;i++){
        start = left;
        while(start <= right){
            if(!(int)image.at<uchar>(i-1, start-1)){
                len = 1;
                p = start + 1;
                if(p <= right){
                    while(!(int)image.at<uchar>(i-1, p-1)){
                        len++;
                        p++;
                        if(p > right)
                            break;
                    }
                }
                length[i-top][start-left] = len;
                start += len;
            }else
                start++;
        }
    }
    
    mbrl = INT_MIN;
    nbr = 0;
    vector<int> calcstd;
    float summation = 0;
    float sumtmp = 0;
    for(int i = 0;i < tmp_height;i++){
        for(int j = 0;j< tmp_width;j++){
            int tmp = length[i][j];
            if(tmp > mbrl)
                mbrl = tmp;
            if(tmp != 0){
                nbr++;
                summation += tmp;
                calcstd.push_back(tmp);
            }
        }
    }
    long num_tmp = calcstd.size();
    summation /= num_tmp;
    for(auto i:calcstd)
        sumtmp += pow((i - summation), 2);
    vbrl = sqrt(sumtmp/num_tmp);
}

void get_pattern_para(vector<pattern> &patterns, bool line){
    long num_patterns = patterns.size();
    for(int i = 0;i<num_patterns;i++){
        patterns[i].left = INT_MAX;
        patterns[i].top = INT_MAX;
        patterns[i].right = INT_MIN;
        patterns[i].bottom = INT_MIN;
        for(auto j:patterns[i].rects){
            if(j.left < patterns[i].left)
                patterns[i].left = j.left;
            if(j.top < patterns[i].top)
                patterns[i].top = j.top;
            if(j.right > patterns[i].right)
                patterns[i].right = j.right;
            if(j.bottom > patterns[i].bottom)
                patterns[i].bottom = j.bottom;
        }
        patterns[i].right = min(patterns[i].right, width);
        patterns[i].bottom = min(patterns[i].bottom, height);
        patterns[i].width = patterns[i].right - patterns[i].left;
        patterns[i].height = patterns[i].bottom - patterns[i].top;
        patterns[i].area = patterns[i].height * patterns[i].width;
        if(!line){
            patterns[i].num_bp = 0;
            for(int k1 = patterns[i].top;k1<=patterns[i].bottom;k1++)
                for(int k2 = patterns[i].left;k2<=patterns[i].right;k2++)
                    if(!(int)image.at<uchar>(k1-1, k2-1))
                        patterns[i].num_bp++;
            patterns[i].bp_density = float(patterns[i].num_bp)/(patterns[i].area - patterns[i].num_bp);
            mbprl(patterns[i].left, patterns[i].right, patterns[i].top, patterns[i].bottom, patterns[i].mbrl, patterns[i].nbr, patterns[i].vbrl);
            patterns[i].sp = (float(patterns[i].nbr)/patterns[i].num_bp)*(pow(min(patterns[i].width, patterns[i].height), 2));
        }
    }
}

void pattern_classfy(vector<pattern>& patterns, vector<pattern>& text, vector<pattern>& title, vector<pattern>& lines){
    get_pattern_para(patterns, false);
    //estimate he
    vector<int> index;
    float he = 0;
    for(int i = 0;i<patterns.size();i++){
        if(patterns[i].height<25){
            index.push_back(i);
            he += patterns[i].height;
        }
    }
    he = he/index.size();
    
//    cout<<"he: "<<he<<endl;
    
    //parameter definition
    //DD                            DI                      Ratios
    float A1 = 400*he*he;      float A2 = 32;         float alpha = 0.75;
    float A3 = 80*he*he;       float B = 16;          float beta = 0.04;
    float A4 = 64*he*he;       float S1 = 350;        float kapa = 1.4;
    float D = 5*he;            float S2 = 500;        float lambda1 = 0.16;
    float H = 0.7*he;          float V = 5.5;         float lambda2 = 0.1;
    float L = 3.0*he;                                 float lambda3 = 0.13;
    float W1 = 1.5*he;                                float rho0 = 0.3;
    float W2 = 10*he;                                 float rho1 = 0.72;
                                                      float rho2 = 0.5;
                                                      float rho3 = 1.65;
    //type 1:1 Text 2 Title 3 Inverse text 4 Photograph 5 Graphic/drawing 6 Vertical line 7 Horizontal line 8 Small
    
    //Rule A Large Patterns
    vector<int> index_large_patterns;
    for(int i = 0;i<patterns.size();i++){
        if(patterns[i].area > A1 && patterns[i].width>D && patterns[i].height>D)
            index_large_patterns.push_back(i);
    }
//    cout<<"size: "<<index_large_patterns.size()<<endl;
//    for(auto i:index_large_patterns)
//        cout<<"index_large_patterns: "<<i<<endl;
    
    //Rule B Photograph or Graphic
    vector<int> index_photograph;
    vector<int> index_graph;
    for(int i = 0;i<index_large_patterns.size();i++)                        //added constraint besides paper
        if(patterns[index_large_patterns[i]].bp_density > rho0 && patterns[index_large_patterns[i]].num_bp > 30000){
            patterns[index_large_patterns[i]].type = 4;
            index_photograph.push_back(index_large_patterns[i]);
        }
        else{
            patterns[index_large_patterns[i]].type = 5;
            index_graph.push_back(index_large_patterns[i]);
        }
//    cout<<"size: "<<index_photograph.size()<<endl;
//    for(auto i:index_photograph)
//        cout<<"index_photograph: "<<i<<endl;
//    cout<<"size: "<<index_graph.size()<<endl;
//    for(auto i:index_graph)
//        cout<<"index_graph: "<<i<<endl;
    
    //Rule C Small Patterns
    index.clear();
    for(int i = 0;i<patterns.size();i++)
        index.push_back(i);
    for(auto i = index_large_patterns.rbegin();i!=index_large_patterns.rend();i++)
        index.erase(index.begin() + *i);
    
    vector<int> index_small_patterns;
    vector<int> todel;
    for(int i = 0;i<index.size();i++)
        if(patterns[index[i]].num_bp < B && patterns[index[i]].area < A2){
            patterns[index[i]].type = 8;
            index_small_patterns.push_back(index[i]);
            todel.push_back(i);
        }
    
//    cout<<"size: "<<index_small_patterns.size()<<endl;
//    for(auto i:index_small_patterns)
//        cout<<"index_small_patterns: "<<i<<endl;
    
    //Rule D Vertical Lines
    vector<int> index_vertical_lines;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float h = (float)patterns[index[i]].height;
        if(h > L && patterns[index[i]].width < min(lambda1*h, W1)){
            patterns[index[i]].type = 6;
            index_vertical_lines.push_back(index[i]);
            lines.push_back(patterns[index[i]]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_vertical_lines.size()<<endl;
//    for(auto i:index_vertical_lines)
//        cout<<"index_vertical_lines: "<<i<<endl;
    
    //Rule E Vertical long thick lines
    vector<int> index_vlt_lines;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float w = (float)patterns[index[i]].width;
        float h = (float)patterns[index[i]].height;
        if(w >= W1 && w < lambda2*h){
            patterns[index[i]].type = 6;
            index_vlt_lines.push_back(index[i]);
//            lines.push_back(patterns[index[i]]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_vlt_lines.size()<<endl;
//    for(auto i:index_vlt_lines)
//        cout<<"index_vlt_lines: "<<i<<endl;
    
    //Rule F Horizontal Lines
    vector<int> index_horizontal_lines;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float w = (float)patterns[index[i]].width;
        float h = (float)patterns[index[i]].height;
        float d = patterns[index[i]].bp_density;
        float m = patterns[index[i]].mbrl;
        if(w>L && h<min(lambda1*w, W1)){
            if(h < H || h < lambda3*w || m > 2*h || d > rho1){
                patterns[index[i]].type = 7;
                index_horizontal_lines.push_back(index[i]);
                lines.push_back(patterns[index[i]]);
                todel.push_back(i);
            }
        }
    }
//    cout<<"size: "<<index_horizontal_lines.size()<<endl;
//    for(auto i:index_horizontal_lines)
//        cout<<"index_horizontal_lines: "<<i+1<<endl;
    
    //Rule G Thick Horizontal Lines
    vector<int> index_th_lines;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float w = (float)patterns[index[i]].width;
        float h = (float)patterns[index[i]].height;
        if(h >= W1 && h < lambda2*w){
            patterns[index[i]].type = 7;
            index_th_lines.push_back(index[i]);
//            lines.push_back(patterns[index[i]]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_th_lines.size()<<endl;
//    for(auto i:index_th_lines)
//        cout<<"index_th_lines: "<<i<<endl;
    
    //Rule H Photographs
    vector<int> index_ps;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float a = (float)patterns[index[i]].area;
        float n = (float)patterns[index[i]].nbr;
        if(a > A3 && n > beta*a){
            patterns[index[i]].type = 4;
            index_ps.push_back(index[i]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_ps.size()<<endl;
//    for(auto i:index_ps)
//        cout<<"index_ps: "<<i<<endl;
    
    //Rule I Graphics
    vector<int> index_gs;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float a = (float)patterns[index[i]].area;
        float s = (float)patterns[index[i]].sp;
        float v = (float)patterns[index[i]].vbrl;
        if(a < A4 && s > S1 && v > V){
            patterns[index[i]].type = 5;
            index_gs.push_back(index[i]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_gs.size()<<endl;
//    for(auto i:index_gs)
//        cout<<"index_gs: "<<i<<endl;
    
    //Rule J Graphics in larger patterns
    vector<int> index_gslp;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float a = (float)patterns[index[i]].area;
        float s = (float)patterns[index[i]].sp;
        float d = (float)patterns[index[i]].bp_density;
        if(a >= A4 && s > S2 && d < rho2){
            patterns[index[i]].type = 5;
            index_gslp.push_back(index[i]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_gslp.size()<<endl;
//    for(auto i:index_gslp)
//        cout<<"index_gslp: "<<i<<endl;
    
    //Rule K Inverse Text
    vector<int> index_it;
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    todel.clear();
    
    for(int i = 0;i<index.size();i++){
        float w = (float)patterns[index[i]].width;
        float m = (float)patterns[index[i]].mbrl;
        float d = (float)patterns[index[i]].bp_density;
        if(w > W2 && d > rho3 && m > alpha*w){
            patterns[index[i]].type = 3;
            index_it.push_back(index[i]);
            todel.push_back(i);
        }
    }
//    cout<<"size: "<<index_it.size()<<endl;
//    for(auto i:index_it)
//        cout<<"index_it: "<<i<<endl;
    
    //recalculate ht
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    
    float ht = 0;
    for(int i = 0;i<index.size();i++)
        ht = ht + patterns[index[i]].height;
    
    ht = ht/index.size();
    
    //Rule L Text or Title
    vector<int> index_tt;
    todel.clear();

    for(int i = 0;i<index.size();i++){
        float h = (float)patterns[index[i]].height;
        float w = (float)patterns[index[i]].width;
    //     if h > kapa*ht && patterns[index[i-1]].bp_density > 0.5 && w > 20
        if(h > kapa*ht && patterns[index[i]].bp_density > 0.5 && w > 10){
            patterns[index[i]].type = 2;
            title.push_back(patterns[index[i]]);
            index_tt.push_back(index[i]);
            todel.push_back(i);
        }
        }
    
    //the remains are all texts
    //index works for texts now
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        index.erase(index.begin() + *i);
    for(int i = 0;i<index.size();i++){
        patterns[index[i]].type = 1;
        text.push_back(patterns[index[i]]);
    }
}

vector<pattern> generate_boxes(vector<pattern>& patterns){
    vector<pattern> boxes;
    long num_patterns = patterns.size();
    float ht = 11.848122162608338;//optimize*************************************
    float W1 = 12.2750;
    float delta;
    vector<int> todel;
    bool flag;
    int tmp;
    int w, h, top, left, right, bottom, num_rects;
    
    for(int i = 0;i<num_patterns;i++){
        w = patterns[i].width;
        h = patterns[i].height;
        top = patterns[i].top;
        left = patterns[i].left;
        right = patterns[i].right;
        bottom = patterns[i].bottom;
        num_rects = (int)patterns[i].rects.size();
    
        if(max(w, h) <= 3*ht)
            continue;
        
        delta = min(W1, float(min(w, h))/4);
        flag = true;
    
        for(int j = 0;j<num_rects;j++){
            tmp = min(min(patterns[i].rects[j].bottom - top, bottom - patterns[i].rects[j].top), min(right - patterns[i].rects[j].left, patterns[i].rects[j].right - left));
            if(tmp > delta){
                flag = false;
                break;
            }
        }
    
        if(flag){
            boxes.push_back(patterns[i]);
            todel.push_back(i);
        }
    }
    
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        patterns.erase(patterns.begin() + *i);
    
    return boxes;
}

vector<pattern> extract_line_boxes(vector<pattern>& boxes, int count_threshold){
    long num_boxes = boxes.size();
    vector<pattern> line_patterns;
    int num_rects, w, h, top, left ,right, bottom;
    int tmp;
    pattern top_line;
    pattern left_line;
    pattern bottom_line;
    pattern right_line;
    top_line.type = 7;
    bottom_line.type = 7;
    left_line.type = 6;
    right_line.type = 6;
    
    for(int i = 0;i<num_boxes;i++){
        num_rects = (int)boxes[i].rects.size();
        w = boxes[i].width;
        h = boxes[i].height;
        top = boxes[i].top;
        left = boxes[i].left;
        right = boxes[i].right;
        bottom = boxes[i].bottom;
    
        for(int j = 0;j < num_rects;j++){
            tmp = min(min(boxes[i].rects[j].bottom - top, bottom - boxes[i].rects[j].top), min(boxes[i].rects[j].right - left, right - boxes[i].rects[j].left));
            if(boxes[i].rects[j].bottom - top == tmp)
                top_line.rects.push_back(boxes[i].rects[j]);
            if(bottom - boxes[i].rects[j].top == tmp)
                bottom_line.rects.push_back(boxes[i].rects[j]);
            if(boxes[i].rects[j].right - left == tmp)
                left_line.rects.push_back(boxes[i].rects[j]);
            if(right - boxes[i].rects[j].left == tmp)
                right_line.rects.push_back(boxes[i].rects[j]);
            }
        
        if(top_line.rects.size() >= count_threshold)
            line_patterns.push_back(top_line);
        if(left_line.rects.size() >= count_threshold)
            line_patterns.push_back(left_line);
        if(bottom_line.rects.size() >= count_threshold)
            line_patterns.push_back(bottom_line);
        if(right_line.rects.size() >= count_threshold)
            line_patterns.push_back(right_line);
        
        top_line.rects.clear();
        left_line.rects.clear();
        bottom_line.rects.clear();
        right_line.rects.clear();
    }
    get_pattern_para(line_patterns, true);
    return line_patterns;
}

vector<pattern> reclass(vector<pattern>& patterns, vector<pattern>& line_patterns){
    long num_lines = line_patterns.size();
    vector<rect> Rects;
    for(auto im:patterns)
        for(auto jq:im.rects)
            Rects.push_back(jq);
    
//    int sum = 0;
//        for(auto j:patterns){
//            cout<<j.rects.size()<<endl;
//            sum+=j.rects.size();
//        }
//    cout<<sum<<endl;
    
    vector<bool> flag = vector<bool>(num_lines, false);
    vector<pattern> new_line;
    vector<int> todel;
    
    int factor = 2;
    int align_range[2];
    int merge_range;
    
    for(int i = 0;i < num_lines;i++){
        if(flag[i])
            continue;
        
        flag[i] = true;
    
        switch(line_patterns[i].type){
            case 6: {//vertical lines
                align_range[0] = line_patterns[i].left - line_patterns[i].width;
                align_range[1] = line_patterns[i].right + line_patterns[i].width;
                merge_range = factor*line_patterns[i].width;
                for(int j = i+1;j < num_lines;j++){
                    if(flag[j])
                        continue;
                    if((min(min(abs(line_patterns[i].top - line_patterns[j].bottom), abs(line_patterns[i].top - line_patterns[j].top)), min(abs(line_patterns[i].bottom - line_patterns[j].top), abs(line_patterns[i].bottom - line_patterns[j].bottom))) < merge_range) && (line_patterns[j].left > align_range[0]) && (line_patterns[j].right < align_range[1])){
                        
                        flag[j] = true;
                        for(auto p:line_patterns[j].rects)
                            line_patterns[i].rects.push_back(p);
        
                        line_patterns[i].right = max(line_patterns[i].right, line_patterns[j].right);
                        line_patterns[i].left = min(line_patterns[i].left, line_patterns[j].left);
                        line_patterns[i].top = min(line_patterns[i].top, line_patterns[j].top);
                        line_patterns[i].bottom = max(line_patterns[i].bottom, line_patterns[j].bottom);
                        line_patterns[i].right = min(line_patterns[i].right, width);
                        line_patterns[i].bottom = min(line_patterns[i].bottom, height);
                        line_patterns[i].width = line_patterns[i].right - line_patterns[i].left;
                        line_patterns[i].height = line_patterns[i].bottom - line_patterns[i].top;
                        line_patterns[i].area = line_patterns[i].height * line_patterns[i].width;
                    }
                }
                merge_range = factor*line_patterns[i].width;
                todel.clear();
                for(int k = 0;k < Rects.size();k++){
                    if((min(min(abs(line_patterns[i].top - Rects[k].bottom), abs(line_patterns[i].top - Rects[k].top)), min(abs(line_patterns[i].bottom - Rects[k].top), abs(line_patterns[i].bottom - Rects[k].bottom))) < merge_range) && (Rects[k].left > align_range[0]) && (Rects[k].right < align_range[1])){
                        
                        todel.push_back(k);
                        line_patterns[i].rects.push_back(Rects[k]);
                
                        line_patterns[i].right = max(line_patterns[i].right, Rects[k].right);
                        line_patterns[i].left = min(line_patterns[i].left, Rects[k].left);
                        line_patterns[i].top = min(line_patterns[i].top, Rects[k].top);
                        line_patterns[i].bottom = max(line_patterns[i].bottom, Rects[k].bottom);
                        line_patterns[i].right = min(line_patterns[i].right, width);
                        line_patterns[i].bottom = min(line_patterns[i].bottom, height);
                        line_patterns[i].width = line_patterns[i].right - line_patterns[i].left;
                        line_patterns[i].height = line_patterns[i].bottom - line_patterns[i].top;
                        line_patterns[i].area = line_patterns[i].height * line_patterns[i].width;
            }
                }
            new_line.push_back(line_patterns[i]);
            for(auto q = todel.rbegin();q!=todel.rend();q++)
                Rects.erase(Rects.begin() + *q);
            break;
            }
                
            case 7: {//horizontal lines
                align_range[0] = line_patterns[i].top - line_patterns[i].height;
                align_range[1] = line_patterns[i].bottom + line_patterns[i].height;
                merge_range = factor*line_patterns[i].height;
                for(int j = i+1;j < num_lines;j++){
                    if(flag[j])
                        continue;
                    if((min(min(abs(line_patterns[i].left - line_patterns[j].left), abs(line_patterns[i].left - line_patterns[j].right)), min(abs(line_patterns[i].right - line_patterns[j].left), abs(line_patterns[i].right - line_patterns[j].right))) < merge_range) && (line_patterns[j].top > align_range[0]) && (line_patterns[j].bottom < align_range[1])){
                        
                        flag[j] = true;
                        for(auto p:line_patterns[j].rects)
                            line_patterns[i].rects.push_back(p);
                        
                        line_patterns[i].right = max(line_patterns[i].right, line_patterns[j].right);
                        line_patterns[i].left = min(line_patterns[i].left, line_patterns[j].left);
                        line_patterns[i].top = min(line_patterns[i].top, line_patterns[j].top);
                        line_patterns[i].bottom = max(line_patterns[i].bottom, line_patterns[j].bottom);
                        line_patterns[i].right = min(line_patterns[i].right, width);
                        line_patterns[i].bottom = min(line_patterns[i].bottom, height);
                        line_patterns[i].width = line_patterns[i].right - line_patterns[i].left;
                        line_patterns[i].height = line_patterns[i].bottom - line_patterns[i].top;
                        line_patterns[i].area = line_patterns[i].height * line_patterns[i].width;
                    }
                }
                
                merge_range = factor*line_patterns[i].height;
                todel.clear();
                
                for(int k = 0;k < Rects.size();k++){
                    if((min(min(abs(line_patterns[i].left - Rects[k].left), abs(line_patterns[i].left - Rects[k].right)), min(abs(line_patterns[i].right - Rects[k].left), abs(line_patterns[i].right - Rects[k].right))) < merge_range) && (Rects[k].top > align_range[0]) && (Rects[k].bottom < align_range[1])){
                        todel.push_back(k);
                        
                        line_patterns[i].rects.push_back(Rects[k]);
                        line_patterns[i].right = max(line_patterns[i].right, Rects[k].right);
                        line_patterns[i].left = min(line_patterns[i].left, Rects[k].left);
                        line_patterns[i].top = min(line_patterns[i].top, Rects[k].top);
                        line_patterns[i].bottom = max(line_patterns[i].bottom, Rects[k].bottom);
                        line_patterns[i].right = min(line_patterns[i].right, width);
                        line_patterns[i].bottom = min(line_patterns[i].bottom, height);
                        line_patterns[i].width = line_patterns[i].right - line_patterns[i].left;
                        line_patterns[i].height = line_patterns[i].bottom - line_patterns[i].top;
                        line_patterns[i].area = line_patterns[i].height * line_patterns[i].width;                    }
        }
                new_line.push_back(line_patterns[i]);
                for(auto q = todel.rbegin();q!=todel.rend();q++)
                    Rects.erase(Rects.begin() + *q);
                break;
            }
        }
    }
    //     pattern = generate_patterns(rects);
    //     pattern = [pattern; new_line];
    //     pattern = pattern_classify(pattern, img);
    return new_line;
}

void get_block_para(block& blocks){
    blocks.left = INT_MAX;
    blocks.top = INT_MAX;
    blocks.right = INT_MIN;
    blocks.bottom = INT_MIN;
    for(auto j:blocks.patterns){
        if(j.left < blocks.left)
            blocks.left = j.left;
        if(j.top < blocks.top)
            blocks.top = j.top;
        if(j.right > blocks.right)
            blocks.right = j.right;
        if(j.bottom > blocks.bottom)
            blocks.bottom = j.bottom;
    }
    blocks.right = min(blocks.right, width);
    blocks.bottom = min(blocks.bottom, height);
    blocks.width = blocks.right - blocks.left;
    blocks.height = blocks.bottom - blocks.top;
    blocks.area = blocks.height * blocks.width;
}

template<typename T1, typename T2>
bool near(T1 x, T2 y, float hgap, float vgap){
//    //x: pattern y:block
//    //pattern is on the left of the block
//    if((x.right < y.left)&&(x.bottom<y.bottom)&&(x.top>y.top))
//        if(y.left - x.right <= factor*hgap)
//            return true;
//    //pattern is on the right of the block
//    if((x.left > y.right)&&(x.bottom<y.bottom)&&(x.top>y.top))
//        if(x.left - y.right <= factor*hgap)
//            return true;
//    //pattern is on the top of the block
//    if((x.bottom > y.top)&&(x.left > y.left)&&(x.right < y.right))
//        if(x.bottom - y.top <= factor*vgap)
//            return true;
//    //pattern is on the bottom of the block
//    if((y.bottom > x.top)&&(x.left > y.left)&&(x.right < y.right))
//        if(y.bottom - x.top <= factor*vgap)
//            return true;
    
    rect rectX;
    rect rectY;
    rectX.left = x.left; rectX.right = x.right; rectX.top = x.top; rectX.bottom = x.bottom;
    rectY.left = y.left; rectY.right = y.right; rectY.top = y.top; rectY.bottom = y.bottom;
//
//    if((x.left < y.right + factor*hgap) && (x.right > y.left - factor*hgap))
//        if((x.top < y.bottom + factor*vgap) && (x.bottom > y.top - factor*vgap))
//            return true;
//    
//    if((x.left >= y.left) && (x.right <= y.right) && (x.top >= y.top) && (x.bottom <= y.bottom))
//        return true;
//    
//    if((y.left >= x.left) && (y.right <= x.right) && (y.top >= x.top) && (y.bottom <= x.bottom))
//        return true;
    
    vector<rect> rectsY;
    vector<rect> rectsX;
    rectsY.push_back(rectY);
    rectsX.push_back(rectX);
    
    if(check_near(rectX, rectsY, hgap, vgap))
        return true;
       
    return false;
}

template<typename T>
void get_block_gap(vector<T>& patterns, float& avh, float& hgap, float& vgap){
    float num_texts = 0;
    long num_patterns = patterns.size();
    vector<int> tt_height;
    for(int i = 0;i<num_patterns;i++){
//        if(patterns[i].type == 1 || patterns[i].type == 2){
            num_texts++;
            tt_height.push_back(patterns[i].height);
//        }
    }
    sort(tt_height.begin(), tt_height.end());
    int start = ceil(num_texts/4.0);
    int End = ceil(3*num_texts/4.0);
    float summ = accumulate(tt_height.begin()+start, tt_height.begin()+End, 0);
    avh = summ/(End-start);
    hgap = 0.6*avh;//0.66
    vgap = 1.1*avh;//2.0
}

vector<block> getblocks(vector<block>& blocks, int type, vector<int>& index){
    vector<block> tmp_blk;
    index.clear();
    for(int p = 0;p < blocks.size();p++){
        if(blocks[p].type == type){
            tmp_blk.push_back(blocks[p]);
            index.push_back(p);
        }
    }
    return tmp_blk;
}

template <typename T1, typename T2>
bool insideblk(T1 blockA, T2 blockB, int threshold){
    if(blockA.right<=blockB.right + threshold && blockA.left>=blockB.left - threshold && blockA.top>=blockB.top - threshold && blockA.bottom<=blockB.bottom+threshold)
        return true;
    return false;
}

void cleanregion(vector<block>& blocks, int threshold){
    long num_blocks = blocks.size();
    vector<bool> flag = vector<bool>(num_blocks, 0);
    vector<int> todel;
    bool first_time;
    
    for(int i = 0;i<num_blocks;i++){
        first_time = true;
        if(flag[i])
            continue;
        
        for(int j = 0;j<num_blocks;j++){
            
            if(flag[j] || j == i)
                continue;
            
            if(insideblk(blocks[j], blocks[i], threshold)){
                flag[j] = true;
                todel.push_back(j);
            }
            
            if(insideblk(blocks[i], blocks[j], threshold)){
                flag[i] = true;
                if(first_time){
                    todel.push_back(i);
                    first_time = false;
                }
            }
        }
    }
    sort(todel.begin(), todel.end());
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        blocks.erase(blocks.begin() + *i);
}

void cleanregion2(vector<block>& block1, vector<block> block2, int threshold){
    long num_block1 = block1.size();
    long num_block2 = block2.size();
    for(long i = num_block1 - 1;i >= 0;i--){
        for(int j = 0;j < num_block2;j++){
            if(insideblk(block1[i], block2[j], threshold)){
                block1.erase(block1.begin()+i);
                break;
            }
        }
    }
}

template<typename T1, typename T2>
bool check_tt_near(T1 A, T2 B){
    float width = (float)(max(A.right, B.right)-min(A.left, B.left));
    float height = (float)(max(A.bottom, B.bottom)-min(A.top, B.top));
    if(width <= A.right-A.left+B.right-B.left && height <= A.bottom-A.top+B.bottom-B.top)
        return true;
    return false;
}

template<typename T>
vector<block> regionform(vector<T>& patterns, vector<pattern> lines, vector<block> oblk){
    long num_patterns = patterns.size();
    bool grouped;
    bool found;
    float avh, hgap, vgap;
    int initial_block = 0;
    bool break_flag, initial_flag, tmp_flag;
    get_block_gap(patterns, avh, hgap, vgap);
    vector<int> idx;
    vector<int> todel;
    vector<block> blocks;
    vector<block> tmp_blk;
    
    for(int i = 0;i < num_patterns;i++){
        cout<<i<<endl;
//        cout<<i+1<<" type: "<<patterns[i].type<<" left :"<<patterns[i].left<<" right :"<<patterns[i].right<<" top :"<<patterns[i].top<<" bottom :"<<patterns[i].bottom<<endl;
//        for(auto pp:blocks)
//            cout<<i+1<<":"<<"blocks size: "<<blocks.size()<<" type: "<<pp.type<<" left :"<<pp.left<<endl;
//        cout<<blocks.size()<<endl;
        grouped = false;
        
//6.21 NOTE: Blocks of different types are not mixingly processed any more.
//        tmp_blk = getblocks(blocks, patterns[i].type, idx);
        tmp_blk = blocks;
        for(int j = 0;j < tmp_blk.size();j++){
            found = false;
            break_flag = false;
            initial_flag = false;
            tmp_flag = false;
            for(int k = 0;k < tmp_blk[j].patterns.size();k++){
                if(near(patterns[i], tmp_blk[j].patterns[k], hgap, vgap)){
                    found = true;
                    break;
                }
            }
            
//            if(near(patterns[i], tmp_blk[j], hgap, vgap))
//                found = true;
            
            if(found){
                if(!grouped){
                    tmp_blk[j].patterns.push_back(patterns[i]);
                    get_block_para(tmp_blk[j]);
                    
                    for(auto kk:lines){
                        if(check_tt_near(tmp_blk[j], kk)){
                            tmp_blk[j].patterns.pop_back();
                            get_block_para(tmp_blk[j]);
                            break_flag = true;
                            break;
                        }
                    }
                    
                    if(!break_flag){
                        for(auto kk:oblk){
                            if(check_tt_near(tmp_blk[j], kk)){
                                tmp_blk[j].patterns.pop_back();
                                get_block_para(tmp_blk[j]);
                                initial_flag = true;
                                break;
                            }
                        }
                        if(!initial_flag){
                            initial_block = j;
                            grouped = true;
                        }
                    }
                }else{
                    for(auto m:tmp_blk[j].patterns)
                        tmp_blk[initial_block].patterns.push_back(m);
                    get_block_para(tmp_blk[initial_block]);
                    todel.push_back(j);
                    
                    for(auto kk:lines){
                        if(check_tt_near(tmp_blk[initial_block], kk)){
                            for(int a = 0;a < tmp_blk[j].patterns.size();a++)
                                tmp_blk[initial_block].patterns.pop_back();
                            get_block_para(tmp_blk[initial_block]);
                            todel.pop_back();
                            tmp_flag = true;
                            break;
                        }
                    }
                    
                    if(!tmp_flag){
                        for(auto kk:oblk){
                            if(check_tt_near(tmp_blk[initial_block], kk)){
                                for(int a = 0;a < tmp_blk[j].patterns.size();a++)
                                    tmp_blk[initial_block].patterns.pop_back();
                                get_block_para(tmp_blk[initial_block]);
                                todel.pop_back();
                                break;
                            }
                        }
                    }
                }
                
            }
        }
        
        for(auto jj1 = todel.rbegin();jj1!=todel.rend();jj1++)
            tmp_blk.erase(tmp_blk.begin()+ *jj1);
        
//6.21 NOTE: The idx includes all of the blocks
//        for(auto jj2 = idx.rbegin();jj2!=idx.rend();jj2++)
//            blocks.erase(blocks.begin()+ *jj2);
        blocks.clear();
        
        for(auto jj3:tmp_blk)
            blocks.push_back(jj3);
        
        if(!grouped){
            block new_blk;
            new_blk.patterns.push_back(patterns[i]);
            new_blk.type = patterns[i].type;
            get_block_para(new_blk);
            blocks.push_back(new_blk);
        }
        todel.clear();
        tmp_blk.clear();
    }
    cleanregion(blocks, 2);
    return blocks;
}

vector<pattern> get_line_from_patterns(vector<pattern>& patterns){
    vector<pattern> ret;
    for(int i = (int)patterns.size()-1;i>=0;i--){
        if(patterns[i].type == 6 || patterns[i].type == 7){
            ret.push_back(patterns[i]);
            patterns.erase(patterns.begin()+i);
        }
}
    return ret;
}

template<typename T>
float get_BlockH(vector<T> patterns){
    long num_patterns = patterns.size();
    vector<int> height;
    for(int i = 0;i<num_patterns;i++)
        height.push_back(patterns[i].height);
    long num_heights = height.size();
    sort(height.begin(), height.end());
    int start = ceil(num_heights/4.0);
    int End = ceil(3*num_heights/4.0);
    float summ = accumulate(height.begin()+start, height.begin()+End, 0);
    return summ/(End-start);
}

void cleanonenearanother(vector<block>& one, vector<block>& another, int threshold, int areathreshold, int cpf){
    //clean line in text
    vector<int> todel;
    vector<int> merge;
    int anothertype = another[0].type;
    for(int i = 0;i < another.size();i++){
        for(int j = 0;j<one.size();j++){
            if(near(one[j], another[i], threshold, threshold) && one[j].area < areathreshold){
                todel.push_back(j);
            }
        }
        if(todel.size() >= cpf){ //6.28: todel.size() >= 2 only change the txt blocks
            for(auto k = todel.rbegin();k!=todel.rend();k++){
                if(find(merge.begin(), merge.end(), *k) == merge.end()){
                    one[*k].type = anothertype;
                    merge.push_back(*k);
                }
            }
        }
        todel.clear();
    }
    sort(merge.begin(), merge.end());
    for(auto i = merge.rbegin();i<merge.rend();i++){
        another.push_back(one[*i]);
        one.erase(one.begin()+ *i);
    }
}

//mereg blocks that overlap together
void merge_blocks(vector<block>& blocks, int w, int h, vector<block> oblk, vector<pattern> lines){
    //near && check_tt_near
    long bs = 0;
    vector<int> todel;
    bool break_flag;
    while(blocks.size() != bs){
        bs = blocks.size();
        for(int i = 0;i<blocks.size();i++){
//            if(blocks[i].area < area_threshold){
                for(int j = i+1;j<blocks.size();j++){
                        break_flag = false;
//                    if(blocks[j].area < area_threshold){
                        if(near(blocks[i], blocks[j], w, h)){
                            for(auto p:blocks[j].patterns)
                                blocks[i].patterns.push_back(p);
                            
                            get_block_para(blocks[i]);
                            todel.push_back(j);
                            
                            for(auto q:oblk){
                                if(check_tt_near(blocks[i], q)){
                                    for(int a = 0;a < blocks[j].patterns.size();a++)
                                        blocks[i].patterns.pop_back();
                                    get_block_para(blocks[i]);
                                    todel.pop_back();
                                    break_flag = true;
                                    break;
                                }
                            }
                            if(!break_flag){
                                for(auto q:lines){
                                    if(check_tt_near(blocks[i], q)){
                                        for(int a = 0;a < blocks[j].patterns.size();a++)
                                            blocks[i].patterns.pop_back();
                                        get_block_para(blocks[i]);
                                        todel.pop_back();
                                        break;
                                    }
                                }
                            }
//                        }
//                    }
                }
            }
            for(auto kk = todel.rbegin();kk!=todel.rend();kk++)
                blocks.erase(blocks.begin() + *kk);
            todel.clear();
        }
    }
}

void deletesmallarea(vector<block>& blocks,int threshold){
    vector<int> todel;
    //if the area of text blocks is too small, the type is changed to 2
    for(int i = 0;i < blocks.size();i++){
        if(blocks[i].area < threshold){
            todel.push_back(i);
        }
    }
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        blocks.erase(blocks.begin() + *i);
}

float get_block_threhold(vector<block> blocks){
    vector<float> scores;
    float median;
    for(auto i:blocks)
        scores.push_back((float)i.area);
    
    size_t size = scores.size();
    
    sort(scores.begin(), scores.end());
    
    if (size  % 2 == 0)
    {
        median = (scores[size / 2 - 1] + scores[size / 2]) / 2;
    }
    else
    {
        median = scores[size / 2];
    }
    return median;
}

float get_max_area(vector<block> blocks){
    vector<float> scores;
    for(auto i:blocks)
        scores.push_back((float)i.area);
    return *max_element(scores.begin(), scores.end());
}

float get_min_area(vector<block> blocks){
    vector<float> scores;
    for(auto i:blocks)
        scores.push_back((float)i.area);
    sort(scores.begin(), scores.end());
    return *(scores.begin()+(int)(scores.size()/4.0));
}

template<typename T>
void Draw(vector<T> patterns, bool print_info, string name){
    //    if(print_info){
    //        int count = 1;
    //        for(auto j:patterns){
    //            cout<<"size:"<<j.patterns.size()<<endl;
    //            cout<<count++<<":"<<endl;
    //            for(auto i:j.patterns){
    //                cout<<"left:"<<i.left<<" top:"<<i.top<<" right:"<<i.right<<" bottom:"<<i.bottom<<" "<<i.type<<endl;
    //                cout<<endl;
    //            }
    //        }
    //    }
    for(auto j:patterns){
        
        if(j.type != 8){
            switch(j.type){
                case 1:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(0, 0, 255), 2);
                    break;
                }
                case 2:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(0, 255, 0), 2);
                    break;
                }
                case 3:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(255, 0, 0), 10);
                    break;
                }
                case 4:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(255, 128, 128), 10);
                    break;
                }
                case 5:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(128, 128, 0), 10);
                    break;
                }
                case 6:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(0, 0, 0), 2);
                    break;
                }
                case 7:{
                    rectangle(imageBGR, Point(j.left, j.top), Point(j.right, j.bottom), CV_RGB(0, 0, 0), 2);
                    break;
                }
            }
        }
    }
    namedWindow("window", CV_WINDOW_FREERATIO);
    resizeWindow("window", 1366, 768);
    imshow("window", imageBGR);
    imwrite(name+".jpg", imageBGR);
    waitKey(0);
    destroyWindow("window");
}

void formetablk(vector<block>& titleblock, vector<block>& txtblock, vector<pattern> lines){
    long bs = 0;
    long ps = 0;
    deletesmallarea(txtblock, 100);
    deletesmallarea(titleblock, 100);
    float titlea, txta;
    int count = -1;
    while(titleblock.size() != bs || txtblock.size() != ps)
//    for(int i = 0;i<20;i++)
    {
        count++;
        bs = titleblock.size();
        ps = txtblock.size();
        
        //median
        //hgap vgap area_gap
        //merge blocks < txta/2.0
        cleanregion2(txtblock, titleblock, 10);
//        txta = get_max_area(txtblock);
        merge_blocks(txtblock, (int)(count/4.0), 10, titleblock, lines);
        cleanregion(txtblock, 10);
        txta = get_min_area(txtblock);
        if(count<3)
            cleanonenearanother(txtblock, titleblock, 10, 10*txta, 2);
        else
            cleanonenearanother(txtblock, titleblock, 30, 10*txta, 1);
        
        cleanregion2(titleblock, txtblock, 10);
//        titlea = get_max_area(titleblock);
        merge_blocks(titleblock, 10+count*2, count, txtblock, lines);
        cleanregion(titleblock, 10);
        titlea = get_min_area(titleblock);
        cleanonenearanother(titleblock, txtblock, 10, 10*titlea, 2);
        cout<<count<<endl;
    }
}

void txtToline(vector<block>& blocks, vector<block>& lines){
    vector<int> todel;
    for(int i = 0;i<blocks.size();i++){
        if(blocks[i].width>10*blocks[i].height && blocks[i].height < 10 && blocks[i].width > 50){
            blocks[i].type = 7;
            lines.push_back(blocks[i]);
            todel.push_back(i);
        }
        else if(blocks[i].height>10*blocks[i].width && blocks[i].width < 10 && blocks[i].height > 50){
            blocks[i].type = 6;
            lines.push_back(blocks[i]);
            todel.push_back(i);
        }
    }
    for(auto i = todel.rbegin();i!=todel.rend();i++)
        blocks.erase(blocks.begin() + *i);
}

template<typename T>
void saveInfo(vector<T> patterns, string name){
    ofstream file(name);
    for(auto i:patterns)
        file<<i.left<<" "<<i.right<<" "<<i.top<<" "<<i.bottom<<" "<<i.type<<" "<<i.height<<" "<<i.width<<"\n";
    file.close();
}

template<typename T>
void readInfo(vector<T>& patterns, string name){
    string line;
    ifstream file(name);
    int count;
    while(getline(file, line, '\n')){
        stringstream tmp(line);
        string tmpln;
        T tmpblk;
        count = 0;
        while(getline(tmp, tmpln, ' ')){
            count++;
            switch(count){
                case 1:
                    tmpblk.left = stoi(tmpln);
                    break;
                case 2:
                    tmpblk.right = stoi(tmpln);
                    break;
                case 3:
                    tmpblk.top = stoi(tmpln);
                    break;
                case 4:
                    tmpblk.bottom = stoi(tmpln);
                    break;
                case 5:
                    tmpblk.type = stoi(tmpln);
                    break;
                case 6:
                    tmpblk.height = stoi(tmpln);
                    break;
                case 7:
                    tmpblk.width = stoi(tmpln);
                    break;
            }
        }
        patterns.push_back(tmpblk);
    }
    file.close();
}

template<typename T>
void createXML(vector<T> patterns, const char* name){
    tinyxml2::XMLDocument ImageXML;
    tinyxml2::XMLNode *alto = ImageXML.NewElement("alto");
    ImageXML.InsertFirstChild(alto);
    
    tinyxml2::XMLNode *Layout = ImageXML.NewElement("Layout");
    alto->InsertFirstChild(Layout);
    
    tinyxml2::XMLElement *Page = ImageXML.NewElement("Page");
    Page->SetAttribute("HEIGHT", height);
    Page->SetAttribute("WIDTH", width);
    Layout->InsertFirstChild(Page);
    
    tinyxml2::XMLNode *PrintSpace = ImageXML.NewElement("PrintSpace");
    Page->InsertFirstChild(PrintSpace);
    
    tinyxml2::XMLNode *TextBlock = ImageXML.NewElement("TextBlock");
    PrintSpace->InsertFirstChild(TextBlock);
    
    tinyxml2::XMLNode *TextLine = ImageXML.NewElement("TextLine");
    TextBlock->InsertFirstChild(TextLine);
    
    //Child = Depth
    for(auto i:patterns){
        tinyxml2::XMLElement *String = ImageXML.NewElement("String");
        String->SetAttribute("HEIGHT", i.bottom - i.top);
        String->SetAttribute("WIDTH", i.right - i.left);
        String->SetAttribute("CONTENT", "NULL");
        String->SetAttribute("HPOS", i.left);
        String->SetAttribute("VPOS", i.top);
        TextLine->InsertEndChild(String);
    }
    ImageXML.SaveFile(name);
}

template<typename T>
float average_pixel_value(T R){
    float sum = 0;
    float count = 0;
    for(int i = R.left;i <= R.right;i++)
        for(int j = R.top;j <= R.bottom;j++){
            if((int)image_ori.at<uchar>(j-1, i-1)!=0){
                sum+=(int)image_ori.at<uchar>(j-1, i-1);
                count++;
            }
        }
    return sum/count;
}

void generate_json(vector<block> blocks, float scale){
    ofstream file(imgname+"json", ofstream::out|ofstream::app);
    long num_blocks = blocks.size();
    file << "[\n\t{\n\t\t" << "annotations:" << "\n\t\t[\n";
    for(int i = 0;i < num_blocks;i++){
        switch(blocks[i].type){
            case 1:{
                file<<"\t\t\t{\n\t\t\t\t"<<"class:";
                file<<"article"<<"\n\t\t\t\t";
                file<<"height:"<<blocks[i].height*scale<<"\n\t\t\t\t";
                file<<"id:"<<i+1<<"\n\t\t\t\t";
                file<<"type:rect"<<"\n\t\t\t\t";
                file<<"width:"<<blocks[i].width*scale<<"\n\t\t\t\t";
                file<<"x:"<<blocks[i].left*scale<<"\n\t\t\t\t";
                if(i+1 < num_blocks)
                    file<<"y:"<<blocks[i].top*scale<<"\n\t\t\t},\n";
                else{
                    file<<"y:"<<blocks[i].top*scale<<"\n\t\t\t}\n\t\t],\n\t\t";
                    file<<"class:"<<"image"<<"\n\t\t";
                    file<<"filename:"<<imgname+".jpg";
                    file<<"\n\t}\n]";
                }
                break;
            }
            case 2:{
                file<<"\t\t\t{\n\t\t\t\t"<<"class:";
                file<<"text"<<"\n\t\t\t\t";
                file<<"height:"<<blocks[i].height*scale<<"\n\t\t\t\t";
                file<<"id:"<<i+1<<"\n\t\t\t\t";
                file<<"type:rect"<<"\n\t\t\t\t";
                file<<"width:"<<blocks[i].width*scale<<"\n\t\t\t\t";
                file<<"x:"<<blocks[i].left*scale<<"\n\t\t\t\t";
                if(i+1 < num_blocks)
                    file<<"y:"<<blocks[i].top*scale<<"\n\t\t\t},\n";
                else{
                    file<<"y:"<<blocks[i].top*scale<<"\n\t\t\t}\n\t\t],\n\t\t";
                    file<<"class:"<<"image"<<"\n\t\t";
                    file<<"filename:"<<imgname+".jpg";
                    file<<"\n\t}\n]";
                }
                break;
            }
        }
    }
    file.close();
}

bool checkline(int x, int y, vector<pattern> lines, int threshold){
    for(int i = 0;i < lines.size();i++){
        if(x<=lines[i].bottom+threshold && x>=lines[i].top-threshold && y>=lines[i].left-threshold && y<=lines[i].right+threshold)
            return true;
    }
    return false;
}

void top_extend(pattern& line, vector<pattern>& lines){
    int tmp_top;
    int ps;
    bool break_flag;
    while(true){
        ps = line.top;
        for(int i = line.left;i <= line.right;i++){
            tmp_top = ps - 1 > 1?ps - 1:1;
            break_flag = false;
            for(int j = tmp_top;j >= tmp_top - 10 && j >= 1;j--){
                if(!(int)image.at<uchar>(j-1, i-1) && !checkline(j, i, lines, 1)){
                    line.top = tmp_top;
                    break_flag = true;
                    break;
                }
            }
            if(break_flag)
                break;
        }
        if(line.top == ps)
            break;
    }
}

void left_extend(pattern& line, vector<pattern>& lines){
    int tmp_left;
    int ps;
    bool break_flag;
    while(true){
        ps = line.left;
        for(int i = line.top;i <= line.bottom;i++){
            tmp_left = ps - 1 > 1?ps - 1:1;
            break_flag = false;
            for(int j = tmp_left;j >= tmp_left - 3 && j >= 1;j--){
                if(!(int)image.at<uchar>(i-1, j-1) && !checkline(j, i, lines, 1)){
                    line.left = tmp_left;
                    break_flag = true;
                    break;
                }
            }
            if(break_flag)
                break;
        }
        if(line.left == ps)
            break;
    }
}

void bottom_extend(pattern& line, vector<pattern>& lines){
    int tmp_bottom;
    int ps;
    bool break_flag;
    while(true){
        ps = line.bottom;
        for(int i = line.left;i <= line.right;i++){
            tmp_bottom = ps + 1 < height?ps + 1:height;
            break_flag = false;
            for(int j = tmp_bottom;j <= tmp_bottom+10 && j <= height;j++){
                if(!(int)image.at<uchar>(j-1, i-1) && !checkline(j, i, lines, 1)){
                    line.bottom = tmp_bottom;
                    break_flag = true;
                    break;
                }
            }
            if(break_flag)
                break;
        }
        if(line.bottom == ps)
            break;
    }
}

void right_extend(pattern& line, vector<pattern>& lines){
    int tmp_right;
    int ps;
    bool break_flag;
    while(true){
        ps = line.right;
        for(int i = line.top;i <= line.bottom;i++){
            tmp_right = ps + 1 < width?ps + 1:width;
            break_flag = false;
            for(int j = tmp_right;j >= tmp_right + 3 && j <= width;j--){
                if(!(int)image.at<uchar>(i-1, j-1) && !checkline(j, i, lines , 1)){
                    line.right = tmp_right;
                    break_flag = true;
                    break;
                }
            }
            if(break_flag)
                break;
        }
        if(line.right == ps)
            break;
    }
}

void extend_lines(vector<pattern>& lines){
    pattern tmp_line;
    for(long i = lines.size()-1;i >= 0;i--){
        tmp_line = lines[i];
        switch(lines[i].type){
            case 6:{
                lines.erase(lines.begin()+i);
                top_extend(tmp_line, lines);
                bottom_extend(tmp_line, lines);
                lines.push_back(tmp_line);
                break;
            }
            case 7:{
                lines.erase(lines.begin()+i);
                left_extend(tmp_line, lines);
                right_extend(tmp_line, lines);
                lines.push_back(tmp_line);
                break;
            }
        }
    }
}

template<typename T>
void clean(vector<pattern>& lines, vector<T> blocks){
    for(long i = lines.size()-1;i >= 0;i--){
        for(auto j:blocks){
            if(insideblk(lines[i], j, 20)){// parameters: 10
                lines.erase(lines.begin()+i);
                break;
            }
        }
    }
}

// 1.改四分位数
// 2.
int main(int argc, const char * argv[]) {
//    resize
    Size size1(2300, 3200);
    cv::resize(image_ori0, image_ori, size1);
    
    //the original size
//    image_ori = image_ori0;
    
    height = image_ori.size().height;
    width = image_ori.cols;
//timer for the program
//    clock_t begin = clock();
    
//Binarize the image
    cvtColor(image_ori, imageBGR, CV_GRAY2BGR);
    threshold(image_ori, image, 200, 255.0, THRESH_BINARY);
//image baseline algorithm
    vector<rect> Rects;
    int count = -1;
    while(1){
        count++;
        if(Rects.size() < 60000){
            threshold(image_ori, image, 160+count*10, 255.0, THRESH_BINARY);
            Rects = locate_rects();
        }else
            break;
    }
    
    vector<pattern> patterns = generate_patterns(Rects);
    vector<pattern> plines;
    vector<pattern> text;
    vector<pattern> title;
    pattern_classfy(patterns, text, title, plines);
    
//get and extend the lines in the patterns
//6.21 NOTES: some large patterns could be boxes which should be deleted
    vector<pattern> boxes = generate_boxes(patterns);
    vector<pattern> lines = extract_line_boxes(boxes, 1);
//    vector<pattern> new_lines = reclass(patterns, lines);
    for(auto i:plines)
        lines.push_back(i);

      saveInfo(text, imgname+"txt.txt");
      saveInfo(title, imgname+"title.txt");
      saveInfo(lines, imgname+"pats.txt");

//    read in the block information
//    vector<pattern> text;
//    readInfo(text, imgname+"txt.txt");
//    vector<pattern> title;
//    readInfo(title, imgname+"title.txt");
//    vector<pattern> lines;
//    readInfo(lines, imgname+"pats.txt");
    extend_lines(lines);
    
//      vector<pattern> patterns;
//      readInfo(patterns, imgname+"pats.txt");
    
//    createXML(patterns, "blocks0033patterns.xml");
    
//    readInfo(patterns, "blocks0033newlines.txt");
    vector<block> textblocks;
    vector<block> titleblocks;
    clean(lines, text);
    clean(lines, title);
    textblocks = regionform(text, lines, titleblocks);
    titleblocks = regionform(title, lines, textblocks);
    formetablk(titleblocks, textblocks, lines);
    
//    generate_json(textblocks, 1);
    
//      clock_t end = clock();
//      double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//      cout<<"The real running time in total is: "<<elapsed_secs<<"s"<<endl;
    
      Draw(textblocks, false, imgname+"txtblks");//false: do not print the blocks info
      Draw(titleblocks, false, imgname+"titleblks2");
      Draw(lines, false, imgname+"titleblks2");
    return 0;
}
           
           
           
           
           
           
           
           
           
           
           
           
           
           
