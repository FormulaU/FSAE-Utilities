include <pack_settings.scad>;
include <cell_spacing.scad>;

segment2D();

module segment2D()
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

  translate(v = [g_wall_hspace, g_wall_vspace])
  {
    cells2D();
  }
}

module cells2D()
{
  // Plot the cells themselves form the points
  points = pack_spacing();
  for (point = points)
  {
    translate(v=[point[0], point[1]])
    {
      circle(d=g_cell_diam);
    }
  }
}
