% Make sure Fulcher hctsa is installed an in path


% Load JSON config
configData = fileread('./Configs/cleanedMasterOperations.json');
config = jsondecode(configData);

% Read parquet file
input_file = './Data/initial_tests.parquet';
data = parquetread(input_file);

% Separate unprocessed and processed columns
unprocessed_columns = data(:, 1:3);
processed_columns = data(:, 4:303);

% Initialize results storage
all_results = [];
all_fieldnames = {};

% Process each series in processed_columns
for i = 1:height(processed_columns)
    series = table2array(processed_columns(i, :));
    results = run_analysis(series, config, OPERATIONS_MAP);
    results.index = i;
    flattened_results = flatten_struct(results);
    
    % Collect field names
    all_fieldnames = union(all_fieldnames, fieldnames(flattened_results));
    
    % Ensure all fields are present in the current result
    missing_fields = setdiff(all_fieldnames, fieldnames(flattened_results));
    for j = 1:numel(missing_fields)
        flattened_results.(missing_fields{j}) = NaN;
    end
    
    % Ensure all previous results have the new fields
    if ~isempty(all_results)
        missing_fields_in_all = setdiff(all_fieldnames, fieldnames(all_results));
        for j = 1:numel(missing_fields_in_all)
            [all_results.(missing_fields_in_all{j})] = deal(NaN);
        end
    end
    
    all_results = [all_results; flattened_results];
end

% Ensure all results have consistent fields
for i = 1:numel(all_results)
    missing_fields = setdiff(all_fieldnames, fieldnames(all_results(i)));
    for j = 1:numel(missing_fields)
        all_results(i).(missing_fields{j}) = NaN;
    end
end

% Convert results to table with consistent fields
results_table = struct2table(all_results);

% Merge unprocessed columns with results
final_table = [unprocessed_columns, results_table];

% Write final table to a CSV file
output_csv_file = 'analysis_results.csv';
writetable(final_table, output_csv_file);

% Function to flatten a nested struct
function flat_struct = flatten_struct(s)
    fields = fieldnames(s);
    flat_struct = struct();
    for i = 1:numel(fields)
        field = fields{i};
        value = s.(field);
        if isstruct(value)
            sub_flat_struct = flatten_struct(value);
            sub_fields = fieldnames(sub_flat_struct);
            for j = 1:numel(sub_fields)
                sub_field = sub_fields{j};
                flat_struct.(sprintf('%s_%s', field, sub_field)) = sub_flat_struct.(sub_field);
            end
        else
            flat_struct.(field) = value;
        end
    end
end

function results = run_analysis(series, config, operations_map)
    results = struct();
    config_fields = fieldnames(config);
    for i = 1:numel(config_fields)
        func_name = config_fields{i};
        param_sets = config.(func_name);
        if isKey(operations_map, func_name)
            func = operations_map(func_name);
            if iscell(param_sets) % Handle cell array of parameter sets
                for j = 1:numel(param_sets)
                    params = param_sets{j};
                    % Check for transform
                    if isfield(params, 'transform')
                        transform = params.transform;
                        params = rmfield(params, 'transform'); % Remove the transform field
                        transformed_series = apply_transform(series, transform);
                    else
                        transformed_series = series;
                    end
                    
                    param_str = '';
                    param_fields = fieldnames(params);
                    for k = 1:numel(param_fields)
                        field = param_fields{k};
                        value = params.(field);
                        param_str = [param_str, sprintf('%s_%s_', field, num2str(value))];
                    end
                    param_str = param_str(1:end-1); % Remove trailing underscore
                    param_str = regexprep(param_str, '[^a-zA-Z0-9_]', '_'); % Replace invalid characters
                    result_key = sprintf('%s_%s', func_name, param_str);
                    try
                        results.(result_key) = call_function_with_params(func, transformed_series, params);
                    catch
                        results.(result_key) = NaN;
                    end
                end
            elseif numel(param_sets) > 1 % Handle struct arrays
                for j = 1:numel(param_sets)
                    params = param_sets(j);
                    % Check for transform
                    if isfield(params, 'transform')
                        transform = params.transform;
                        params = rmfield(params, 'transform'); % Remove the transform field
                        transformed_series = apply_transform(series, transform);
                    else
                        transformed_series = series;
                    end
                    
                    param_str = strjoin(cellfun(@(k, v) sprintf('%s_%s', k, num2str(v)), ...
                        fieldnames(params), struct2cell(params), 'UniformOutput', false), '_');
                    param_str = regexprep(param_str, '[^a-zA-Z0-9_]', '_'); % Replace invalid characters
                    result_key = sprintf('%s_%s', func_name, param_str);
                    try
                        results.(result_key) = call_function_with_params(func, transformed_series, params);
                    catch
                        results.(result_key) = NaN;
                    end
                end
            else % Handle single struct
                params = param_sets;
                % Check for transform
                if isfield(params, 'transform')
                    transform = params.transform;
                    params = rmfield(params, 'transform'); % Remove the transform field
                    transformed_series = apply_transform(series, transform);
                else
                    transformed_series = series;
                end
                
                param_str = '';
                param_fields = fieldnames(params);
                for k = 1:numel(param_fields)
                    field = param_fields{k};
                    value = params.(field);
                    param_str = [param_str, sprintf('%s_%s_', field, num2str(value))];
                end
                param_str = param_str(1:end-1); % Remove trailing underscore
                param_str = regexprep(param_str, '[^a-zA-Z0-9_]', '_'); % Replace invalid characters
                result_key = sprintf('%s_%s', func_name, param_str);
                try
                    results.(result_key) = call_function_with_params(func, transformed_series, params);
                catch
                    results.(result_key) = NaN;
                end
            end
        else
            results.(func_name) = "Missing Operation";
        end
    end
end

function transformed_series = apply_transform(series, transform)
    switch transform
        case 'x_z'
            transformed_series = (series - mean(series)) / std(series);
        case 'abs(x_z)'
            transformed_series = abs((series - mean(series)) / std(series));
        case 'zscore(abs(x_z))'
            abs_series = abs((series - mean(series)) / std(series));
            transformed_series = (abs_series - mean(abs_series)) / std(abs_series);
        case 'diff(x_z)'
            z_scored_series = (series - mean(series)) / std(series);
            transformed_series = diff(z_scored_series);
        case 'zscore(sign(x_z))'
            z_scored_series = (series - mean(series)) / std(series);
            sign_series = sign(z_scored_series);
            transformed_series = (sign_series - mean(sign_series)) / std(sign_series);
        otherwise
            error('Unknown transform type ''%s''', transform);
    end
end

function result = call_function_with_params(func, series, params)
    % Convert struct fields and values to cell arrays
    param_values = struct2cell(params);
    
    % Create a cell array for the input arguments to the function
    input_args = [{series}, param_values'];
    
    % Call the function with the unpacked parameters
    result = feval(func, input_args{:});
end
