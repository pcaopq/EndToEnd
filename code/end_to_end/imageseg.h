
#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
// using namespace cv;

struct rect{
    int left;
    int right;
    int top;
    int bottom;
};

struct pattern{
    vector<rect> rects;
    float bp_density;
    float vbrl;
    float sp;
    int mbrl;
    int nbr;
    int left;
    int right;
    int top;
    int bottom;
    int width;
    int height;
    int area;
    int num_bp;
    int type;
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

int search_right(int x, int y, int xstep);
int lowest_row(rect R);

bool checksquare(int i, int j);
int search_below(rect R, int ry, int ystep);

vector<rect> locate_rects();

bool check_near(rect rectA, vector<rect> rects, int wthreshold, int hthreshold);

vector<pattern> generate_patterns(vector<rect> rects);

void mbprl(int left, int right, int top, int bottom, int& mbrl, int& nbr, float& vbrl);

void get_pattern_para(vector<pattern> &patterns, bool line);

vector<pattern> generate_boxes(vector<pattern>& patterns);

vector<pattern> extract_line_boxes(vector<pattern>& boxes, int count_threshold);

vector<pattern> reclass(vector<pattern>& patterns, vector<pattern>& line_patterns);
void get_block_para(block& blocks);

template<typename T>
void get_block_gap(vector<T>& patterns, float& avh, float& hgap, float& vgap);

vector<block> getblocks(vector<block>& blocks, int type, vector<int>& index);
template <typename T1, typename T2>
bool insideblk(T1 blockA, T2 blockB, int threshold);

void cleanregion(vector<block>& blocks, int threshold);

void cleanregion2(vector<block>& block1, vector<block> block2, int threshold);

template<typename T1, typename T2>
bool check_tt_near(T1 A, T2 B);

template<typename T>
vector<block> regionform(vector<T>& patterns, vector<pattern> lines, vector<block> oblk);

vector<pattern> get_line_from_patterns(vector<pattern>& patterns);

template<typename T>
float get_BlockH(vector<T> patterns);
void cleanonenearanother(vector<block>& one, vector<block>& another, int threshold, int areathreshold, int cpf);

//mereg blocks that overlap together
void merge_blocks(vector<block>& blocks, int w, int h, vector<block> oblk, vector<pattern> lines);

void deletesmallarea(vector<block>& blocks,int threshold);

float get_block_threhold(vector<block> blocks);

float get_max_area(vector<block> blocks);

float get_min_area(vector<block> blocks);

template<typename T>
void Draw(vector<T> patterns, bool print_info, string name);

void formetablk(vector<block>& titleblock, vector<block>& txtblock, vector<pattern> lines);

void txtToline(vector<block>& blocks, vector<block>& lines);

template<typename T>
void saveInfo(vector<T> patterns, string name);

template<typename T>
void readInfo(vector<T>& patterns, string name);

template<typename T>
void createXML(vector<T> patterns, const char* name);

template<typename T>
float average_pixel_value(T R);

void generate_json(vector<block> blocks, float scale);

bool checkline(int x, int y, vector<pattern> lines, int threshold);

void top_extend(pattern& line, vector<pattern>& lines);
void left_extend(pattern& line, vector<pattern>& lines);

void bottom_extend(pattern& line, vector<pattern>& lines);

void right_extend(pattern& line, vector<pattern>& lines);

void extend_lines(vector<pattern>& lines);

template<typename T>
void clean(vector<pattern>& lines, vector<T> blocks);
