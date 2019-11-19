include <pack_settings.scad>;
use <fuselinks.scad>;

fuse_test_array(g_fuse_count, g_min_fuse_wid, g_max_fuse_wid);

module fuse_test_array(num_fuses, min_fuse, max_fuse)
{
  // Derive fuse length from pack parameters.
  fuse_len = sqrt(pow((g_cell_hspace + g_row_offset), 2) + pow(g_cell_vspace, 2));
  for (idx = [0 : num_fuses])
  {
    // Spacing: 2.5 times max pad width
    vspacing = 1.5 * max(g_neg_pad_diam, g_pos_pad_diam);
    translate(v = [0, vspacing * idx, 0])
    {
      fuse_test_element(fuse_len, ((max_fuse - min_fuse) * idx) / num_fuses + min_fuse);
    }
  }
}

module fuse_test_element(length, fuse_width)
{
  fuse(length, fuse_width);
  circle(d = g_neg_pad_diam);
  translate(v = [length, 0, 0])
  {
    circle(d = g_pos_pad_diam);
  }
}
