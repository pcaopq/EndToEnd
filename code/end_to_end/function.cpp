extern "C" int* function(){
int* information = new int[10];
for(int k=0;k<10;k++){
    information[k] = k;
}
return information;
}