//
//  main.cpp
//  imageSeg
//
//  Created by Panfeng Cao on 16/6/14.
//  Copyright © 2016年 Panfeng Cao. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
using namespace std;
using namespace cv;

struct rect{
    int left;
    int right;
    int top;
    int bottom;
};

struct pattern{
    vector<rect> rects;
    float bp_density;   //!< black pixel density
    float vbrl;         //!< the variations of the black pixel run length
    float sp;           //!< nbr/num_bp
    int mbrl;           //!< maximum black pixel run length
    int nbr;            //!< number of black pixel runs
    int left;
    int right;
    int top;
    int bottom;
    int width;
    int height;
    int area;
    int num_bp;         //!< number of the black pixels
    int type;
    int min_grayvalue;  //!< minimum gray values of the pixels in the pattern
};

struct block{
    vector<pattern> patterns;
    int left;
    int right;
    int top;
    int bottom;
    int width;
    int height;
    int area;
    int type;
};

string imgname;
Mat image_ori0;
Mat image_ori;
Mat image_roi;
Mat image;
Mat imageBGR;
int height;
int width;

int search_right(int x, int y, int xstep){
    /**Search the black pixels from the right of (x, y)**/
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
    /**Return the lowest row that has black pixel of the rect 'R'**/
    for(int i = min(R.top+2, height);i>=R.top;i--){
        for(int j = R.left;j<=min(R.right, width);j++)
            if(!(int)image.at<uchar>(i-1, j-1))
                return i - R.top + 1;
    }
    return 0;
}

bool checksquare(int i, int j){
    /**Check whether there is black pixel in the 8-neighbour of (i, j)**/
//    sum(sum(img(i:i+2,j:j+2).*ones(3,3))) == 9
    if((int)image.at<uchar>(i, j) && (int)image.at<uchar>(i+1, j) && (int)image.at<uchar>(i+2, j) && (int)image.at<uchar>(i, j+1) && (int)image.at<uchar>(i, j+2) && (int)image.at<uchar>(i+1, j+1) && (int)image.at<uchar>(i+1, j+2) && (int)image.at<uchar>(i+2, j+1) && (int)image.at<uchar>(i+2, j+2))
        return true;
    else
        return false;
}

int search_below(rect R, int ry, int ystep){
    /**Search the black pixels under the current rect 'R'**/
    for(int i = ry + 2;i>=ry+3-ystep;i--){
        for(int j = R.left;j<=min(R.right, width)-2;j++)
            if(i+2>height || checksquare(i-1, j-1))
                return 0;
    }
    R.top = ry;
    return lowest_row(R);
}

vector<rect> locate_rects(){
    /**Get the rects in the image**/
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

template<typename T1, typename T2>
bool check_near(T1 rectA, T2 rectB, int wthreshold, int hthreshold){
    /**Check whether 'rectA' and 'rectB' are close enough**/
    int width = max(rectA.right, rectB.right)-min(rectA.left, rectB.left);
    int height = max(rectA.bottom, rectB.bottom)-min(rectA.top, rectB.top);
    if(width <= rectA.right-rectA.left+rectB.right-rectB.left+wthreshold && height <= rectA.bottom-rectA.top+rectB.bottom-rectB.top+hthreshold)
        return true;
    return false;
}

void mbprl(int left, int right, int top, int bottom, int& mbrl, int& nbr, float& vbrl){
    /**Get the maximum black pixels run length of a pattern**/
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
    /**Get the parameters of the patterns**/
    long num_patterns = patterns.size();
    bool first_time;
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
            patterns[i].min_grayvalue = 0;
            patterns[i].num_bp = 0;
            first_time = false;
            patterns[i].min_grayvalue = 100;
            for(int k1 = patterns[i].top;k1<=patterns[i].bottom;k1++)
                for(int k2 = patterns[i].left;k2<=patterns[i].right;k2++)
                    if(!(int)image.at<uchar>(k1-1, k2-1)){
                        patterns[i].num_bp++;
                        if(!first_time){
                        if((int)image_roi.at<uchar>(k1-1, k2-1)<10){
                            patterns[i].min_grayvalue = (int)image_roi.at<uchar>(k1-1, k2-1);
//                            cout<<patterns[i].min_grayvalue<<endl;
                            first_time = true;
                        }
                        }
                    }
            patterns[i].bp_density = float(patterns[i].num_bp)/(patterns[i].area - patterns[i].num_bp);
            mbprl(patterns[i].left, patterns[i].right, patterns[i].top, patterns[i].bottom, patterns[i].mbrl, patterns[i].nbr, patterns[i].vbrl);
            patterns[i].sp = (float(patterns[i].nbr)/patterns[i].num_bp)*(pow(min(patterns[i].width, patterns[i].height), 2));
        }
    }
}

template<typename T1, typename T2>
bool near(T1 x, T2 y, float hgap, float vgap){
    /**equal to check_near**/
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
    
    if(check_near(x, y, hgap, vgap))
        return true;
    
    return false;
}

vector<pattern> generate_patterns(vector<rect> rects){
    /**Group the adjacent 'rects' into patterns**/
    vector<pattern> ret;
//    pattern tmp;
    long num_patterns;
    long num_rects = rects.size();
//    tmp.rects.push_back(rects[0]);
//    ret.push_back(tmp);
    vector<int> todel;
    for(int rects_count = 0;rects_count < num_rects;rects_count++){
        if(rects[rects_count].right - rects[rects_count].left >= (float)width/2.0 || rects[rects_count].bottom - rects[rects_count].top >= (float)height/2.0)
            continue;
        num_patterns = ret.size();
        
        for(int i = 0;i<num_patterns;i++){
            for(int k = 0;k<ret[i].rects.size();k++)
                if(check_near(rects[rects_count], ret[i].rects[k], 1, 1)){
                    todel.push_back(i);
                    break;
                }
        }
        
//        for(int i = 0;i<num_patterns;i++){
//            if(check_near(rects[rects_count], ret[i], 0, 0)){
//                todel.push_back(i);
//                break;
//            }
//        }
        
        if(todel.size() == 1){
            ret[todel[0]].rects.push_back(rects[rects_count]);
        }
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
        get_pattern_para(ret, true);
//        cout<<rects_count<<endl;
        todel.clear();
    }
    cout<<"The total number of patterns is "<<ret.size()<<endl;
    cout<<"The estimated time for generating the blocks is "<<(float)ret.size()/250<<"s"<<endl;
    return ret;
}

void pattern_classfy(vector<pattern>& patterns, vector<pattern>& text, vector<pattern>& title, vector<pattern>& lines, vector<pattern>& graph){
    /**Classify the patterns**/
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
    float A4 = 64*he*he;       float S1 = 350;        //float kapa = 1.4;
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
        if(patterns[i].area > A1 && patterns[i].width>D && patterns[i].height>D){
            graph.push_back(patterns[i]);
            index_large_patterns.push_back(i);
        }
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
    cout<<"ht:"<<ht<<endl;
    //Rule L Text or Title
    vector<int> index_tt;
    todel.clear();

    for(int i = 0;i<index.size();i++){
        float h = (float)patterns[index[i]].height;
//        float w = (float)patterns[index[i]].width;
        int area = patterns[index[i]].area;
    //     if h > kapa*ht && patterns[index[i-1]].bp_density > 0.5 && w > 20
//        if(h > kapa*ht && patterns[index[i]].bp_density > 0.5 && w > 10){
        
        if(h > 1.5*ht && patterns[index[i]].min_grayvalue<10 && area > ht*ht){
            patterns[index[i]].type = 2;
//            cout<<"title:"<<patterns[index[i]].min_grayvalue<<endl;
//            cout<<"title:"<<"h:"<<h<<"w:"<<w<<"area:"<<area<<endl;
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
//        float h = (float)patterns[index[i]].height;
//        float w = (float)patterns[index[i]].width;
//        int area = patterns[index[i]].area;
        patterns[index[i]].type = 1;
//        cout<<"text:"<<patterns[index[i]].min_grayvalue<<endl;
//        cout<<"text:"<<"h:"<<h<<"w:"<<w<<"area:"<<area<<endl;
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
    /**The edges of the boxes are usually the boundaries of the blocks**/
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
    /**The detail is in the paper.
     *In general, after extending the lines, some patterns need to be assigned to another patterns.
     **/
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
    /**Get the parameters for 'blocks'**/
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

template<typename T>
void get_block_gap(vector<T>& patterns, float& avh, float& hgap, float& vgap, float hf, float vf){
    /**Get the gap used to determine whether two blocks are close enough to merge**/
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
    hgap = hf*avh;//0.66
    vgap = vf*avh;//2.0
}

vector<block> getblocks(vector<block>& blocks, int type, vector<int>& index){
    /**Get the blocks whose type is 'type' in 'blocks', and their indexes are saved in 'index'**/
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
    /**Check if 'blockA' is in 'blockB'**/
    if(blockA.right<=blockB.right + threshold && blockA.left>=blockB.left - threshold && blockA.top>=blockB.top - threshold && blockA.bottom<=blockB.bottom+threshold)
        return true;
    return false;
}

void cleanregion(vector<block>& blocks, int threshold){
    /**If the block in 'blocks' is in another block in 'blocks', it will be deleted**/
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

template<typename T>
void cleanregion2(vector<block>& block1, vector<T> block2, int threshold){
    /**Delete the block in 'block1' if it's in another block in 'block2'**/
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

//template<typename T>
//void cleanregion22(vector<block>& block1, vector<T> block2){
//    long num_block1 = block1.size();
//    long num_block2 = block2.size();
//    for(long i = num_block1 - 1;i >= 0;i--){
//        for(int j = 0;j < num_block2;j++){
//            if(check_near(block1[i], block2[j], 0, 0)){
//                block1.erase(block1.begin()+i);
//                break;
//            }
//        }
//    }
//}

template<typename T1, typename T2>
bool check_tt_near(T1 A, T2 B){
    /**Check if two blocks or patterns are overlapped with each other**/
    float width = (float)(max(A.right, B.right)-min(A.left, B.left));
    float height = (float)(max(A.bottom, B.bottom)-min(A.top, B.top));
    if(width <= A.right-A.left+B.right-B.left && height <= A.bottom-A.top+B.bottom-B.top)
        return true;
    return false;
}

template<typename T>
vector<block> regionform(vector<T>& patterns, vector<pattern> lines, vector<block> oblk, float hf, float vf){
    /**Group nearby patterns into blocks
     *The result block will not overlap with 'lines' and 'oblk'
     **/
    long num_patterns = patterns.size();
    bool grouped;
    bool found;
    float avh, hgap, vgap;
    int initial_block = 0;
    bool break_flag, initial_flag, tmp_flag;
    get_block_gap(patterns, avh, hgap, vgap, hf, vf);
    vector<int> idx;
    vector<int> todel;
    vector<block> blocks;
    vector<block> tmp_blk;
    
    for(int i = 0;i < num_patterns;i++){
//        cout<<i<<endl;
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
//            for(int k = 0;k < tmp_blk[j].patterns.size();k++){
//                if(near(patterns[i], tmp_blk[j].patterns[k], hgap, vgap)){
//                    found = true;
//                    break;
//                }
//            }
            
            if(near(patterns[i], tmp_blk[j], hgap, vgap))
                found = true;
            
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
    cleanregion(blocks, 10);
    return blocks;
}

vector<pattern> get_line_from_patterns(vector<pattern>& patterns){
    /**Get line patterns from the patterns**/
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
    /**Get the average height of the blocks**/
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

//void cleanonenearanother(vector<block>& one, vector<block>& another, int threshold, int areathreshold, int cpf){
//    //clean line in text
//    vector<int> todel;
//    vector<int> merge;
//    int anothertype = another[0].type;
//    for(int i = 0;i < another.size();i++){
//        for(int j = 0;j<one.size();j++){
//            if(check_near(one[j], another[i], threshold, threshold) && one[j].area < areathreshold){
//                todel.push_back(j);
//            }
//        }
//        if(todel.size() >= cpf){ //6.28: todel.size() >= 2 only change the txt blocks
//            for(auto k = todel.rbegin();k!=todel.rend();k++){
//                if(find(merge.begin(), merge.end(), *k) == merge.end()){
//                    one[*k].type = anothertype;
//                    merge.push_back(*k);
//                }
//            }
//        }
//        todel.clear();
//    }
//    sort(merge.begin(), merge.end());
//    for(auto i = merge.rbegin();i<merge.rend();i++){
//        another.push_back(one[*i]);
//        one.erase(one.begin()+ *i);
//    }
//}

//mereg blocks that overlap together
void merge_blocks(vector<block>& blocks, int w, int h, vector<block> oblk, vector<pattern> lines){
    /**Merge the nearby blocks and the merged block will not overlap with 'oblk' and 'lines'**/
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

vector<block> deletesmallarea(vector<block>& blocks,int threshold){
    /**Delete blocks with small area**/
    vector<int> todel;
    vector<block> ret;
    //if the area of text blocks is too small, the type is changed to 2
    for(int i = 0;i < blocks.size();i++){
        if(blocks[i].area < threshold){
            todel.push_back(i);
        }
    }
    for(auto i = todel.rbegin();i!=todel.rend();i++){
        ret.push_back(blocks[*i]);
        blocks.erase(blocks.begin() + *i);
    }
    return ret;
}

float get_median_area(vector<block> blocks){
    /**Get the median area of the blocks**/
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
    /**Get the maximum area of the blocks**/
    vector<float> scores;
    for(auto i:blocks)
        scores.push_back((float)i.area);
    return *max_element(scores.begin(), scores.end());
}

float get_min_area(vector<block> blocks){
    /**Get the minimum area of the blocks**/
    vector<float> scores;
    for(auto i:blocks)
        scores.push_back((float)i.area);
    sort(scores.begin(), scores.end());
    return *(scores.begin()+(int)(scores.size()/4.0));
}

template<typename T>
void Draw(vector<T> patterns, bool print_info, string name, float factorh, float factorw){
    /**Save the segmentation result into a png image**/
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
                    rectangle(imageBGR, Point((j.left+50)*factorw, (j.top+50)*factorh), Point((j.right+50)*factorw, (j.bottom+50)*factorh), CV_RGB(255, 0, 0), 10);
                    break;
                }
                case 2:{
                    rectangle(imageBGR, Point((j.left+50)*factorw, (j.top+50)*factorh), Point((j.right+50)*factorw, (j.bottom+50)*factorh), CV_RGB(0, 255, 0), 10);
                    break;
                }
//                case 3:{
//                    rectangle(imageBGR, Point(j.left*factorw, j.top*factorh), Point(j.right*factorw, j.bottom*factorh), 10);
//                    break;
//                }
//                case 4:{
//                    rectangle(imageBGR, Point(j.left*factorw, j.top*factorh), Point(j.right*factorw, j.bottom*factorh), CV_RGB(255, 128, 128), 10);
//                    break;
//                }
//                case 5:{
//                    rectangle(imageBGR, Point(j.left*factorw, j.top*factorh), Point(j.right*factorw, j.bottom*factorh), CV_RGB(128, 128, 0), 10);
//                    break;
//                }
                case 6:{
                    rectangle(imageBGR, Point((j.left+50)*factorw, (j.top+50)*factorh), Point((j.right+50)*factorw, (j.bottom+50)*factorh), CV_RGB(0, 0, 0), 10);
                    break;
                }
                case 7:{
                    rectangle(imageBGR, Point((j.left+50)*factorw, (j.top+50)*factorh), Point((j.right+50)*factorw, (j.bottom+50)*factorh), CV_RGB(0, 0, 0), 10);
                    break;
                }
//                default:{
//                    rectangle(imageBGR, Point((j.left+50)*factorw, (j.top+50)*factorh), Point((j.right+50)*factorw, (j.bottom+50)*factorh), CV_RGB(255, 0, 0), 10);
//                }
            }
        }
    }
//    namedWindow("window", CV_WINDOW_AUTOSIZE);
//    resizeWindow("window", 1366, 768);
//    imshow("window", imageBGR);
    imwrite(name+".png", imageBGR);
//    waitKey(0);
//    destroyWindow("window");
}

void write_time(double time){
    /**Write the running time of the algorithm into a file**/
    ofstream file("../../output/segment/ImgSeg", ofstream::out|ofstream::app);
    file<<time<<" ";
}

void generate_json(string name, vector<block> blocks, float scaleh, float scalew){
    /**Generate the .json files for the evaluation system**/
    ofstream file(name);
    long num_blocks = blocks.size();
    file << "[\n\t{\n\t\t" << '"'<<"annotations"<<'"'<<":" << "\n\t\t[\n";
    for(int i = 0;i < num_blocks;i++){
        switch(blocks[i].type){
            case 1:{
                file<<"\t\t\t{\n\t\t\t\t"<<'"'<<"class"<<'"'<<":";
                file<<'"'<<"article"<<'"'<<','<<"\n\t\t\t\t";
                file<<'"'<<"height"<<'"'<<":"<<(blocks[i].height+50)*scaleh<<','<<"\n\t\t\t\t";
                file<<'"'<<"id"<<'"'<<":"<<i<<','<<"\n\t\t\t\t";
                file<<'"'<<"type"<<'"'<<":"<<'"'<<"rect"<<'"'<<','<<"\n\t\t\t\t";
                file<<'"'<<"width"<<'"'<<":"<<(blocks[i].width+50)*scalew<<','<<"\n\t\t\t\t";
                file<<'"'<<"x"<<'"'<<":"<<(blocks[i].left+50)*scalew<<','<<"\n\t\t\t\t";
                if(i+1 < num_blocks)
                    file<<'"'<<"y"<<'"'<<":"<<(blocks[i].top+50)*scaleh<<"\n\t\t\t},\n";
                else{
                    file<<'"'<<"y"<<'"'<<":"<<(blocks[i].top+50)*scaleh<<"\n\t\t\t}\n\t\t]\n\t\t";
                    file<<"\n\t}\n]";
                }
                break;
            }
            case 2:{
                file<<"\t\t\t{\n\t\t\t\t"<<'"'<<"class"<<'"'<<":";
                file<<'"'<<"title"<<'"'<<','<<"\n\t\t\t\t";
                file<<'"'<<"height"<<'"'<<":"<<(blocks[i].height+50)*scaleh<<','<<"\n\t\t\t\t";
                file<<'"'<<"id"<<'"'<<":"<<i<<','<<"\n\t\t\t\t";
                file<<'"'<<"type"<<'"'<<":"<<'"'<<"rect"<<'"'<<','<<"\n\t\t\t\t";
                file<<'"'<<"width"<<'"'<<":"<<(blocks[i].width+50)*scalew<<','<<"\n\t\t\t\t";
                file<<'"'<<"x"<<'"'<<":"<<(blocks[i].left+50)*scalew<<','<<"\n\t\t\t\t";
                if(i+1 < num_blocks)
                    file<<'"'<<"y"<<'"'<<":"<<(blocks[i].top+50)*scaleh<<"\n\t\t\t},\n";
                else{
                    file<<'"'<<"y"<<'"'<<":"<<(blocks[i].top+50)*scaleh<<"\n\t\t\t}\n\t\t]\n\t\t";
                    file<<"\n\t}\n]";
                }
                break;
            }
        }
    }
    file.close();
}

bool checkline(int x, int y, vector<pattern> lines, int threshold){
    /**Stop extending the line if the line reaches another line**/
    for(int i = 0;i < lines.size();i++){
        if(x<=lines[i].bottom+threshold && x>=lines[i].top-threshold && y>=lines[i].left-threshold && y<=lines[i].right+threshold)
            return true;
    }
    return false;
}

void top_extend(pattern& line, vector<pattern>& lines){
    /**Extend the vertical lines from the top end**/
    int tmp_top;
    int ps;
    bool break_flag;
    while(true){
        ps = line.top;
        for(int i = line.left - 3;i <= line.right + 3;i++){
            tmp_top = ps - 1 > 1?ps - 1:1;
            break_flag = false;
            for(int j = tmp_top;j >= tmp_top - 5 && j >= 1;j--){
                if(!(int)image.at<uchar>(j-1, i-1) && !checkline(j, i, lines, 0)){
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
    /**Extend the horizontal lines from the left end**/
    int tmp_left;
    int ps;
    bool break_flag;
    while(true){
        ps = line.left;
        for(int i = line.top;i <= line.bottom;i++){
            tmp_left = ps - 1 > 1?ps - 1:1;
            break_flag = false;
            for(int j = tmp_left;j >= tmp_left - 3 && j >= 1;j--){
                if(!(int)image.at<uchar>(i-1, j-1) && !checkline(j, i, lines, 0)){
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
    /**Extend the vertical lines from the bottom end**/
    int tmp_bottom;
    int ps;
    bool break_flag;
    while(true){
        ps = line.bottom;
        for(int i = line.left - 3;i <= line.right + 3;i++){
            tmp_bottom = ps + 1 < height?ps + 1:height;
            break_flag = false;
            for(int j = tmp_bottom;j <= tmp_bottom+5 && j <= height;j++){
                if(!(int)image.at<uchar>(j-1, i-1) && !checkline(j, i, lines, 0)){
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
    /**Extend the horizontal lines from the right end**/
    int tmp_right;
    int ps;
    bool break_flag;
    while(true){
        ps = line.right;
        for(int i = line.top;i <= line.bottom;i++){
            tmp_right = ps + 1 < width?ps + 1:width;
            break_flag = false;
            for(int j = tmp_right;j >= tmp_right + 3 && j <= width;j--){
                if(!(int)image.at<uchar>(i-1, j-1) && !checkline(j, i, lines , 0)){
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
    /**Extend the line patterns in vertical or horizontal directions until no black pixel is in the range**/
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
    /**Delete the line patterns in blocks**/
    for(long i = lines.size()-1;i >= 0;i--){
        for(auto j:blocks){
            if(insideblk(lines[i], j, 20)){// parameters: 10
                lines.erase(lines.begin()+i);
                break;
            }
        }
    }
}

//blocksA is text 1
void check_num_patterns(vector<block>& blocksA, vector<block>& blocksB, vector<pattern> patterns){
    /**If the word density in a block is too small and the block's type is text, change the type to title. 
     *If the word density is too large and the block's type is title, change the type to text.
     **/
    vector<block> tmpblockA;
    vector<block> tmpblockB;
    vector<int> todel;
    float count;
    for(long i = blocksA.size()-1;i >= 0;i--){
        count = 0;
        for(int j = 0; j < patterns.size();j++){
            if(patterns[j].left >= blocksA[i].left){
                if(patterns[j].right <= blocksA[i].right){
                    if(patterns[j].top >= blocksA[i].top){
                        if(patterns[j].bottom <= blocksA[i].bottom){
                            count++;
                        }
                    }
                }
            }
        }
        cout<<count / blocksA[i].area<<endl;
        if(count / blocksA[i].area < 0.003){//////////////////////////////////////////////
            blocksA[i].type = 2;
            tmpblockA.push_back(blocksA[i]);
            blocksA.erase(blocksA.begin()+i);
        }
    }
    cout<<endl;
    for(long i = blocksB.size()-1;i >= 0;i--){
        count = 0;
        for(int j = 0; j < patterns.size();j++){
            if(patterns[j].left >= blocksB[i].left){
                if(patterns[j].right <= blocksB[i].right){
                    if(patterns[j].top >= blocksB[i].top){
                        if(patterns[j].bottom <= blocksB[i].bottom){
                            count++;
                        }
                    }
                }
            }
        }
        cout<<count / blocksB[i].area<<endl;
        if(count / blocksB[i].area > 0.004 && count > 20){//////////////////////////////////
            blocksB[i].type = 1;
            tmpblockB.push_back(blocksB[i]);
            blocksB.erase(blocksB.begin()+i);
        }
    }
    
    for(auto i:tmpblockA)
        blocksA.push_back(i);
    for(auto i:tmpblockB)
        blocksB.push_back(i);
}

bool check_cluster_updown(block A, block B, vector<block> blocks, vector<block> blks){
    /**check whether two textblocks are close enough in vertical direction**/
    int r = max(A.right, B.right);
    float Amid = (A.left + A.right)/2.0;
    int l = min(A.left, B.left);
    float Bmid = (B.left + B.right)/2.0;
    bool exist = false;
    
    if(abs(Amid - Bmid) < 100){
        for(auto i:blocks){
            if(i.width + r - l >= max(i.right, r) - min(i.left, l)){
                if((A.bottom > i.top && B.top < i.bottom) || (B.bottom > i.top && A.top < i.bottom)){
                    exist = true;
                    break;
                }
            }
        }
        if(!exist)
            return true;
    }
    return false;
}


//cluster blocks up and down without refering to title blocks
void cluster(vector<block>& titleblocks, vector<block>& textblocks){
    /**If one text block is under another text block and they are close enough in vertical direction, group them into one block**/
    block tmpblock;
    long ps = 0;
    while(ps != textblocks.size()){
        ps = textblocks.size();
        for(long i = textblocks.size()-1;i >= 1;i--){
            for(long j = i-1;j >= 0;j--){
                if(check_cluster_updown(textblocks[i], textblocks[j], titleblocks, textblocks)){
                    for(auto k:textblocks[i].patterns)
                        textblocks[j].patterns.push_back(k);
                    get_block_para(textblocks[j]);
                    textblocks.erase(textblocks.begin()+i);
                    break;
                }
            }
        }
    }
}

void VD(vector<block>& titleblocks, vector<block>& textblocks){
    /**Group the text blocks under the same title block into an entire block**/
    long textsize = textblocks.size();
    long titlesize = titleblocks.size();
    vector<int> label = vector<int>(textsize, -1);
    vector<vector<int>> find_label(titlesize, vector<int>());
    vector<int> todel;
    int cur_bot;
    for(int i = 0;i < textsize;i++){
        cur_bot = INT_MIN;
        for(int j = 0;j < titleblocks.size();j++){
            if(textblocks[i].top > titleblocks[j].bottom && titleblocks[j].bottom > cur_bot){
                if(textblocks[i].width + titleblocks[j].width >= max(textblocks[i].right, titleblocks[j].right) - min(textblocks[i].left, titleblocks[j].left)){
                    label[i] = j;
                    cur_bot = titleblocks[j].bottom;
                }
            }
        }
    }
    for(int i = 0;i < textsize;i++){
        if(label[i]!=-1)
            find_label[label[i]].push_back(i);
    }
    for(int i = 0;i < find_label.size();i++){
        if(find_label[i].size() <= 1)
            continue;
        for(int k = 1;k < find_label[i].size();k++){
            todel.push_back(find_label[i][k]);
            for(auto p:textblocks[find_label[i][k]].patterns){
                textblocks[find_label[i][0]].patterns.push_back(p);
            }
            get_block_para(textblocks[find_label[i][0]]);
            for(auto q:titleblocks){
                if(check_tt_near(q, textblocks[find_label[i][0]])){
                    for(int pp = 0;pp < textblocks[find_label[i][k]].patterns.size();pp++)
                        textblocks[find_label[i][0]].patterns.pop_back();
                    todel.pop_back();
                    get_block_para(textblocks[find_label[i][0]]);
                    break;
                }
            }
        }
    }
    sort(todel.begin(), todel.end());
    for(long i = todel.size()-1;i >= 0;i--)
        textblocks.erase(textblocks.begin()+todel[i]);
}

int main(int argc, const char * argv[]) {
     imgname = argv[1];
     string jsoname = argv[2];
     image_ori0 = imread(imgname, 0);
     float original_height = (float)image_ori0.rows;
     float original_width = (float)image_ori0.cols;
     Size size1(2300, 3200);
     cv::resize(image_ori0, image_ori, size1);
     cv::Rect roi(50,50,2200,3100);
     image_roi = image_ori(roi);

     height = image_roi.size().height;
     width = image_roi.cols;
    // //timer for the program
     clock_t begin = clock();
    //
    // //Binarize the image
     cvtColor(image_ori0, imageBGR, CV_GRAY2BGR);

    // //image baseline algorithm
     vector<rect> Rects;
     int count = -1;
     while(1){
         count++;
         if(Rects.size() < 50000){
             threshold(image_roi, image, 160+count*10, 255.0, THRESH_BINARY);
             Rects = locate_rects();
         }else
             break;
     }
     
     vector<pattern> patterns = generate_patterns(Rects);
     vector<pattern> plines;
     vector<pattern> text;
     vector<pattern> title;
     vector<pattern> graph;
     pattern_classfy(patterns, text, title, plines, graph);
     vector<pattern> boxes = generate_boxes(patterns);
     vector<pattern> lines = extract_line_boxes(boxes, 1);

     for(auto i:plines)
         lines.push_back(i);

     threshold(image_roi, image, 200, 255.0, THRESH_BINARY);
     extend_lines(lines);
     vector<block> NULLBLOCK;
     vector<pattern> NULLLINE;

     vector<block> textblocks;
     vector<block> titleblocks;
     clean(lines, text);
     clean(lines, title);
     
     textblocks = regionform(text, lines, titleblocks, 0.5, 1.1);
     long bs = textblocks.size();
     merge_blocks(textblocks, 5, 10, titleblocks, lines);
     
     titleblocks = regionform(title, lines, textblocks, 1.1, 1.1);
     long ps = titleblocks.size();
     vector<block> tmp_textblocks;
     tmp_textblocks = deletesmallarea(textblocks, 2000);
     cleanregion2(titleblocks, textblocks, 10);
     merge_blocks(titleblocks, 10, 10, textblocks, lines);
     cleanregion2(textblocks, titleblocks, 10);
     
     while(bs != textblocks.size() || ps != titleblocks.size()){
         bs = textblocks.size();
         ps = titleblocks.size();
         merge_blocks(textblocks, 2, 2, NULLBLOCK, lines);
         merge_blocks(titleblocks, 10, 10, NULLBLOCK, lines);
         cleanregion2(textblocks, titleblocks, 10);
         cleanregion2(titleblocks, textblocks, 10);
         cleanregion(textblocks, 2);
         cleanregion(titleblocks, 2);
         cout<<"first"<<endl;
     }
     
     ps = 0;
     while(ps != titleblocks.size()){
         ps = titleblocks.size();
         cluster(titleblocks, textblocks);
         VD(titleblocks, textblocks);
         cleanregion2(titleblocks, textblocks, 10);
         cleanregion(textblocks, 2);
     }
     
     ps = 0;
     while(ps != titleblocks.size()){
         ps = titleblocks.size();
         merge_blocks(titleblocks, 50, 50, NULLBLOCK, lines);
         cleanregion2(textblocks, titleblocks, 10);
         cleanregion(titleblocks, 2);
         cout<<"second"<<endl;
     }

     for(auto i:titleblocks)
         textblocks.push_back(i);

     clock_t end = clock();
     cout<<imgname<<" Fineshed"<<endl;
     generate_json(jsoname, textblocks, original_height/3200, original_width/2300);

       double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
       cout<<"The real running time in total is: "<<elapsed_secs<<"s"<<endl;
     write_time(elapsed_secs);
     Draw(textblocks, false, imgname+"txtblks", original_height/3200, original_width/2300);
     return 0;
 }