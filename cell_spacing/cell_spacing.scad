include <pack_settings.scad>;

gen_segment();

module gen_segment()
{
    // Derived values
    segment_hgt = g_cells_in_parallel * (g_cell_diam) +
                    (g_cells_in_parallel - 1) * (g_cell_vspace) +
                    (2 * g_wall_vspace);
    segment_wid = g_cells_in_series * (g_cell_diam) +
                    (g_cells_in_series - 1) * (g_cell_hspace) +
                    g_row_offset +
                    (2 * g_wall_hspace);
    
    // Build the walls for the segment.
    mirror(v = [0,1,0])
    {
            // Mirrored about a plane defined by the y axis, so that the inside of the wall is at y=0
            square(size = [segment_wid, g_wall_thickness], center=false);
    }   
    translate(v = [0, segment_hgt, 0])
    {
        // Translate without mirroring, 
        square(size = [segment_wid, g_wall_thickness], center=false);
    }
    
    // Build the cells themselves
    for (row = [0 : g_cells_in_parallel-1])
    {
        v_offset = row * (g_cell_diam + g_cell_vspace) +
                   (g_wall_vspace + g_cell_diam/2);
        // Determine if our row is offset: odd rows are offset, even ones are not.
        if (row % 2 == 1)
        {
            h_offset = g_cell_diam/2 +
                       g_wall_hspace +
                       g_row_offset;
            translate(v = [h_offset, v_offset, 0])
            {
                gen_row(g_cells_in_series, g_cell_hspace, g_cell_diam);
            }
        }
        else
        {
            h_offset = g_cell_diam/2 + g_wall_hspace;
            translate(v = [h_offset, v_offset, 0])
            {
                gen_row(g_cells_in_series, g_cell_hspace, g_cell_diam);
            }
        }
    }
}
module gen_row(n_cells, h_space, g_cell_diam)
{
    // For cleanliness, consolidate our vertical offset into one variable.
    for (cell = [0 : n_cells-1])
    {
        h_pos = cell * (g_cell_diam + h_space);
        translate(v = [h_pos,0,0])
        {
            circle(d=g_cell_diam);
        }
    }
}