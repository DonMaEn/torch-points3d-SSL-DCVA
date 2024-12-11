import laspy
import open3d as o3d
import numpy as np
import argparse

def las_to_ply(las_filename,
               ply_filename,
               subtract_x = None,
               subtract_y = None,
               subtract_z = None):

    if (not (
        ((subtract_x is None) and (subtract_y is None) and (subtract_z is None)) or
        ((subtract_x is not None) and (subtract_y is not None) and (subtract_z is not None))
       )):
        raise RuntimeError("subtract x, y, and z must all be either set or unset")
    
    # Read the LAS file using laspy
    las = laspy.read(las_filename)

    # Extract point cloud data (coordinates and optionally color)
    points = np.vstack((las.x, las.y, las.z)).transpose()
    # Subtract off the minimum x, y, and z to make coordinates local
    if (subtract_x is None):
        points[:,0] = points[:,0] - points[:,0].min()
        points[:,1] = points[:,1] - points[:,1].min()
        points[:,2] = points[:,2] - points[:,2].min()
    else:
        points[:,0] = points[:,0] - subtract_x
        points[:,1] = points[:,1] - subtract_y
        points[:,2] = points[:,2] - subtract_z

    # If color data is available, extract RGB values (assuming it exists)
    if 'red' in las.point_format.dimension_names:
        colors = np.vstack((las.red, las.green, las.blue)).transpose() / 65535.0  # Normalize to [0,1] range
    else:
        colors = np.zeros_like(points)  # Default to white if no color data is present

    # Create an Open3D point cloud object
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # Write the point cloud to a .ply file
    o3d.io.write_point_cloud(ply_filename, point_cloud)

    print(f"Point cloud saved to {ply_filename}")

def main():
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Convert a LAS file to a PLY file.")
    parser.add_argument("input", type=str, help="Path to the input LAS file")
    parser.add_argument("output", type=str, help="Path to the output PLY file")

    parser.add_argument('--subtract-x', '-x', default=None, type=float)
    parser.add_argument('--subtract-y', '-y', default=None, type=float)
    parser.add_argument('--subtract-z', '-z', default=None, type=float)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the conversion function with input and output filenames from command line
    las_to_ply(args.input,
               args.output,
               args.subtract_x,
               args.subtract_y,
               args.subtract_z)

if __name__ == "__main__":
    main()
