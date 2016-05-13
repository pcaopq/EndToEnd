function generate_json(file, scale)
    %scale 30740/1929
    load(file);
    num_patterns = size(pattern, 1);
    fileID = fopen('0003.json', 'w');
    fprintf(fileID, '[\n\t{\n\t\t"annotations":\n\t\t[\n');
    
    for i = 1:num_patterns
%         fprintf(fileID, '\t\t\t{\n\t\t\t\t"class":');
        switch pattern(i).type
            case 1
                        fprintf(fileID, '\t\t\t{\n\t\t\t\t"class":');

                  fprintf(fileID, '"article",\n\t\t\t\t');  
                          fprintf(fileID, '"height":%f,\n\t\t\t\t', pattern(i).para.height*scale);
        fprintf(fileID, '"id":"%d",\n\t\t\t\t', i);
        fprintf(fileID, '"type":"rect",\n\t\t\t\t');
        fprintf(fileID, '"width":%f,\n\t\t\t\t', pattern(i).para.width*scale);
        fprintf(fileID, '"x":%f,\n\t\t\t\t', pattern(i).para.left*scale);
        if i < num_patterns
            fprintf(fileID, '"y":%f\n\t\t\t},\n', pattern(i).para.top*scale);
        else
            fprintf(fileID, '"y":%f\n\t\t\t}\n\t\t],\n\t\t', pattern(i).para.top*scale);
            fprintf(fileID, '"class": "image",\n\t\t');
            fprintf(fileID, '"filename": "%s.jpg"', file);
            fprintf(fileID, '\n\t}\n]');
        end
            case 2
                        fprintf(fileID, '\t\t\t{\n\t\t\t\t"class":');

                  fprintf(fileID, '"text",\n\t\t\t\t');  
                          fprintf(fileID, '"height":%f,\n\t\t\t\t', pattern(i).para.height*scale);
        fprintf(fileID, '"id":"%d",\n\t\t\t\t', i);
        fprintf(fileID, '"type":"rect",\n\t\t\t\t');
        fprintf(fileID, '"width":%f,\n\t\t\t\t', pattern(i).para.width*scale);
        fprintf(fileID, '"x":%f,\n\t\t\t\t', pattern(i).para.left*scale);
                if i < num_patterns
            fprintf(fileID, '"y":%f\n\t\t\t},\n', pattern(i).para.top*scale);
        else
            fprintf(fileID, '"y":%f\n\t\t\t}\n\t\t],\n\t\t', pattern(i).para.top*scale);
            fprintf(fileID, '"class": "image",\n\t\t');
            fprintf(fileID, '"filename": "%s.jpg"', file);
            fprintf(fileID, '\n\t}\n]');
        end
%             case 3
%                   fprintf(fileID, '"inverse text",\n\t\t\t\t');  
            case 4
                        fprintf(fileID, '\t\t\t{\n\t\t\t\t"class":');

                  fprintf(fileID, '"photograph",\n\t\t\t\t');  
                          fprintf(fileID, '"height":%f,\n\t\t\t\t', pattern(i).para.height*scale);
        fprintf(fileID, '"id":"%d",\n\t\t\t\t', i);
        fprintf(fileID, '"type":"rect",\n\t\t\t\t');
        fprintf(fileID, '"width":%f,\n\t\t\t\t', pattern(i).para.width*scale);
        fprintf(fileID, '"x":%f,\n\t\t\t\t', pattern(i).para.left*scale);
                if i < num_patterns
            fprintf(fileID, '"y":%f\n\t\t\t},\n', pattern(i).para.top*scale);
        else
            fprintf(fileID, '"y":%f\n\t\t\t}\n\t\t],\n\t\t', pattern(i).para.top*scale);
            fprintf(fileID, '"class": "image",\n\t\t');
            fprintf(fileID, '"filename": "%s.jpg"', file);
            fprintf(fileID, '\n\t}\n]');
        end
%             case 5
%                   fprintf(fileID, '"graphic",\n\t\t\t\t');  
%             case 6
%                   fprintf(fileID, '"vertical line",\n\t\t\t\t');  
%             case 7
%                   fprintf(fileID, '"horizontal line",\n\t\t\t\t');  
%             case 8
%                   fprintf(fileID, '"small pattern",\n\t\t\t\t');  
        end
%         fprintf(fileID, '"height":%f,\n\t\t\t\t', pattern(i).para.height*scale);
%         fprintf(fileID, '"id":"%d",\n\t\t\t\t', i);
%         fprintf(fileID, '"type":"rect",\n\t\t\t\t');
%         fprintf(fileID, '"width":%f,\n\t\t\t\t', pattern(i).para.width*scale);
%         fprintf(fileID, '"x":%f,\n\t\t\t\t', pattern(i).para.left*scale);
%         if i < num_patterns
%             fprintf(fileID, '"y":%f\n\t\t\t},\n', pattern(i).para.top*scale);
%         else
%             fprintf(fileID, '"y":%f\n\t\t\t}\n\t\t],\n\t\t', pattern(i).para.top*scale);
%             fprintf(fileID, '"class": "image",\n\t\t');
%             fprintf(fileID, '"filename": "%s.jpg"', file);
%             fprintf(fileID, '\n\t}\n]');
%         end
    end
    fclose(fileID);
end

