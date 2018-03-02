function process_rules(rules, category_token)
%PROCESS_RULES Takes in a string of rules formatted as single lines and a 
%category token (EV, IC, etc.) and exports them to a csv file as rule-text
%pairs.
    %Tokenize rules by newline.
    split_rules = strsplit(rules, '\n');
    output = cell(length(split_rules), 2);
    output(:) = {' '};
    for idx = 1:length(split_rules)
        str = split_rules(idx);
        %Article case
        if (startsWith(str, 'ARTICLE'))
            output(idx, 1) = str;
            continue;
        end
        %category case
        if (startsWith(str, category_token))
            spc_idx = strfind(str, ' ');
            output(idx, 1) = extractBefore(str, spc_idx{1}(1));
            output(idx,2) = extractAfter(str, spc_idx{1}(1));
        end
    end
    xlswrite('excel_output', output);
end

