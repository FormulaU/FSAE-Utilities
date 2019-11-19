include <pack_settings.scad>;
include <cell_spacing.scad>;


fuselinks();

module fuselinks()
{
  union()
  {
    cell_pads();
    busbar();
    fuses();
  }
}

module busbar()
{
  points = column_spacing(1);
  for (idx = [0: len(points)-2])
  {
    pt1 = points[idx];
    pt2 = points[idx+1];
    delta_x = pt2[0] - pt1[0];
    delta_y = pt2[1] - pt1[1];
    // Connect with a rectangle
    length = sqrt(pow(delta_x, 2) + pow(delta_y, 2));
    translate([pt1[0] + delta_x/2, pt1[1] + delta_y/2, 0])
    {
      rotate(a=atan(delta_y/delta_x))
      {
        square(size=[length, g_neg_pad_diam], center=true);
      }
    }
  }
}

module fuses()
{
  // Note: we will always have an even number of points, as we're getting
  // two columns of the same # of points
  points = column_spacing(2);

  for (idx = [0 : (len(points)/2)-1])
  {
    pt1 = points[idx];
    pt2 = points[idx + len(points)/2];
    delta_x = pt2[0] - pt1[0];
    delta_y = pt2[1] - pt1[1];
    // Connect with a rectangle
    length = sqrt(pow(delta_x, 2) + pow(delta_y, 2));
    translate([pt1[0], pt1[1], 0])
    {
      rotate(a=atan(delta_y/delta_x))
      {
        fuse(length, g_fuse_width);
      }
    }
  }
}

module fuse(length, fuse_width)
{
  fuse_fideltiy = 10;
  end_width = g_fuse_width;
  fuse_pts = fuse_profile_pts(fuse_fideltiy, fuse_width);
  scale(v=[length, 1, 0])
  {
    polygon(points=fuse_pts);
  }
}

function fuse_profile_pts(pt_cnt, fuse_width)
  = [for (i = [0:pt_cnt]) quadratic_fuse_profile(i/pt_cnt, fuse_width),
  for (i = [0:pt_cnt]) y_reflect(quadratic_fuse_profile((1-i/pt_cnt), fuse_width))];

// The function that defines the profile of our fuses, evaluated from 0 to 1 along the length of the fuse.
function quadratic_fuse_profile(x, fuse_width) =
  [x,
  (min(g_neg_pad_diam, g_pos_pad_diam) - fuse_width/2) * pow((x-g_lat_fuse_pos), 2) + fuse_width/2];

function y_reflect(pt) = [pt[0], -pt[1]];

module cell_pads()
{
  neg_points = column_spacing(1);
  points = column_spacing(2);
  // First half of the points are the negative row, second half positive.
  idx = 0;
  for (idx = [0 : len(points)-1])
  {
    point = points[idx];
    translate(v=[point[0], point[1], 0])
    {
      if (idx < len(points)/2)
      {
        circle(d=g_neg_pad_diam);
      }
      else
      {
        circle(d=g_pos_pad_diam);
      }
    }
  }

}
