//
//  main.cpp
//  VD
//
//  Created by Panfeng Cao on 16/6/1.
//  Copyright © 2016年 Panfeng Cao. All rights reserved.
//

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
using namespace std;
class VerticalDominance{
public:
    vector<vector<string>> contents;
    vector<vector<float>> coors;
    vector<float> height;
    vector<vector<float>> textcoors;
    vector<vector<float>> titlecoors;
    vector<vector<vector<float>>> assignments;
    vector<vector<vector<float>>> articleblocks;
    vector<float> title_assignments;
    
    VerticalDominance(){
        contents = vector<vector<string>>();
        coors = vector<vector<float>>();
        height = vector<float>();
        textcoors = vector<vector<float>>();
        titlecoors = vector<vector<float>>();
        assignments = vector<vector<vector<float>>>();
        articleblocks = vector<vector<vector<float>>>();
        title_assignments = vector<float>();
    }
    
    vector<float> tocorners(float y, float x, float h, float w);
    
    float vector_sum(vector<float> v);
    
    vector<float> join_hori(vector<vector<float>> coordinates);
    //care len(coors)
    vector<float> join_hori2(vector<float> coors1, vector<float> coors2);
    
    vector<float> join_verti(vector<vector<float>> coordinates);
    
    void parse(const char* scrapedname);
    
    float findtitleheight();
    
    bool adjoins(vector<float>a, vector<float>b);

    bool sitson(vector<float>a, vector<float>b);
    
    void getstrips();
    
    void gettitleblocks();
    
    bool dominates(vector<float> a, vector<float> b);
    
    bool supports(vector<float> a, vector<float> b);
    
    void assign_textblocks();
    
    void group_textblocks();

    void group_titleblocks();
};