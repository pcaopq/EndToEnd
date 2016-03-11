path_in  = 'C:\\Users\\Samuel\\Desktop\\Engr355\\Batch 1\\Batch 1\\sn85042289\\15032502570\\1961110101\\';
path_out = 'C:\\Users\\Samuel\\Desktop\\ProquestNews2016\\';

for ord = 5:46
   sprintf('%04d',ord)
   fname_in  = strcat(path_in , sprintf('%04d',ord),'.jp2');
   fname_out = strcat(path_out, sprintf('%04d',ord),'.jpg');
   A = imread(fname_in);
   imwrite(A,fname_out);
end
