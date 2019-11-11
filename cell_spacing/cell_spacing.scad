include <pack_settings.scad>;

function pack_spacing() =
    column_spacing(g_cells_in_series);

function column_spacing(num_columns) = [
    // Build by column
    for (col = [0 : g_cells_in_series-1])
        for (pt = single_column()) [pt[0] + horz_pos(col), pt[1]]
];
        
function single_column() = [
    for (row = [0 : g_cells_in_parallel-1])
        (row % 2 == 0) ?
            [0,             vert_pos(row)]:
            [g_row_offset, vert_pos(row)]
];
    
function vert_pos(row) =
   row * (g_cell_diam + g_cell_vspace) + g_cell_diam/2;
    
function horz_pos(col) =
    col * (g_cell_diam + g_cell_hspace) + g_cell_diam/2;