// ********** Overall pack settings: Cell Layout **********
g_cells_in_parallel = 10;
g_cells_in_series = 12;
g_cell_diam = 18;
g_cell_hspace = 4;
g_cell_vspace = 4;
g_row_offset = (g_cell_diam + g_cell_hspace)/2;

// ********** Settings for determining the distance from walls **********
g_wall_vspace = 5;
g_wall_hspace = 25;
g_wall_thickness = 1;

// ********** Settings for the fusible links **********
g_fuse_mat_thickness=0.1;
g_fuse_area_sqmm=0.5;
g_fuse_width=g_fuse_area_sqmm/g_fuse_mat_thickness;
g_neg_pad_diam = 15;
g_pos_pad_diam = 10;
g_lat_fuse_pos = .65;

// ********** Settings for the fuse link test array **********
g_fuse_count = 10;
g_max_fuse_wid = 8;
g_min_fuse_wid = 3;
