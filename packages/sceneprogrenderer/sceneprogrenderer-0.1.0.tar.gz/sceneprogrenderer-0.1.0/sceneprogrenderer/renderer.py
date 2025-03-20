from .utils import *

class SceneRenderer:
    def __init__(self, resolution_x: int = 1920, resolution_y: int = 1080, samples: int = 100, frame_rate: int = 30, num_frames: int = 360, cuda: bool = False):
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.samples = samples
        self.frame_rate = frame_rate
        self.num_frames = num_frames
        self.cuda = cuda
        self.scene_center = None
        self.scene_size = None

    def add_environment_texture(self):
        """
        Add the add_environment_texture function to the scene script.
        """
        def get_image_path() -> str:
            """
            Get the path to the environment texture image.

            Returns:
                str: The path to the environment texture image.
            """
            # Calculate the absolute path dynamically
            package_dir = os.path.dirname(__file__)  # Directory of the current file
            image_path = os.path.join(package_dir, "assets", "env.exr")
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")
            return image_path

        image_path = get_image_path()

        # Add the environment texture
        add_environment_texture(image_path)

    def init(self, path):
        clear_scene()
        load_scene(path)
        apply_smooth_shading()
        set_clamp_factor_to_zero()
        cam_ob = initialize_camera()
        self.add_environment_texture()
        self.scene_center, self.scene_size = get_scene_params()
        return cam_ob

    def render(self, path, output_path, location=None, target=None):
        cam_ob = self.init(path)

        base_location = self.scene_center
        base_target = self.scene_size

         # Adjust location and target if custom inputs are provided
        if location is not None:
            base_location = [base_location[i] + location[i] for i in range(3)]
        if target is not None:
            base_target = [base_target[i] + target[i] for i in range(3)]

        base_location[1] = -base_location[1]
        base_target[1] = -base_target[1]

        place_camera(cam_ob, location, target)
        setup_renderer(output_path, self.resolution_x, self.resolution_y, self.samples)
        render_image()

    def render_from_front(self, path, output_path):
        """
        Render the scene from the front view.

        Args:
            path (str): Path to the scene file.
            output_path (str): Path to save the rendered image.
        """
        cam_ob = self.init(path)
        scene_dims = self.scene_size
        scene_center = self.scene_center
        W, D, H = scene_dims
        cx, cz, cy = scene_center
        dist = np.max([W, D, H])
        cy_ = dist * 3.0
        # cz_ = cy_ * 0.5
        cz_ = D / 2

        place_camera(cam_ob, (cx, -cy_, cz_), (cx, cz, cy))
        setup_renderer(output_path, self.resolution_x, self.resolution_y, self.samples)
        
        render_image()

    def render_from_top(self, path, output_path):
        """
        Render the scene from the top view.

        Args:
            path (str): Path to the scene file.
            output_path (str): Path to save the rendered image.
        """
        cam_ob = self.init(path)
        W, D, H = self.scene_size
        cx, cz, cy = self.scene_center
        dist = np.max([W, D, H])
        cy_ = dist * 3
        cz_ = cy_ * 0.5

        place_camera(cam_ob, (cx, cz, cy_), (cx, cz, 0))
        setup_renderer(output_path, self.resolution_x, self.resolution_y, self.samples)
        render_image()

    def render_from_corners(self, path, output_paths):
        """
        Render the scene from the four corners.

        Args:
            path (str): Path to the scene file.
            output_paths (list): List of paths to save the rendered images from each corner.
        """
        cam_ob = self.init(path)
        scene_dims = self.scene_size
        scene_center = self.scene_center
        W,D,H = scene_dims
        cx, cz, cy = scene_center
        # cz = -cz

        corners = [
        ((cx+W, cz-D, 2*H),  (cx, cz, 0)),  # Camera at (0, 0, h) looking at (w, d, 0)
        ((cx+W, cz+D, 2*H), (cx, cz, 0)),  # Camera at (w, 0, h) looking at (0, d, 0)
        ((cx-W, cz+D, 2*H), (cx, cz, 0)),  # Camera at (0, d, h) looking at (w, 0, 0)
        ((cx-W, cz-D, 2*H),  (cx, cz, 0))   # Camera at (w, d, h) looking at (0, 0, 0)
        ]
        
        for i, (camera_location, target_location) in enumerate(corners):
            place_camera(cam_ob, camera_location, target_location)
            setup_renderer(output_paths[i], self.resolution_x, self.resolution_y, self.samples)
            render_image()
    
    def render_from_edge_midpoints(self, path, output_paths):
        """
        Render the scene from the four upper edge midpoints.

        Args:
            path (str): Path to the scene file.
            output_paths (list): List of paths to save the rendered images from each edge midpoint.
        """
        cam_ob = self.init(path)
        scene_dims = self.scene_size
        scene_center = self.scene_center
        W, D, H = scene_dims
        cx, cz, cy = scene_center

        # Midpoints of the four upper edges
        edges = [
            ((cx + 2*W, cz, 2 * H), (cx, cz, 0)),  # Front-midpoint
            ((cx, cz + 2*D, 2 * H), (cx, cz, 0)),  # Back-midpoint
            ((cx - 2*W, cz, 2 * H), (cx, cz, 0)),  # Left-midpoint
            ((cx, cz - 2*D, 2 * H), (cx, cz, 0))   # Right-midpoint
        ]

        for i, (camera_location, target_location) in enumerate(edges):
            place_camera(cam_ob, camera_location, target_location)
            setup_renderer(output_paths[i], self.resolution_x, self.resolution_y, self.samples)
            render_image()

    def render_360(self, path, output_path):
        """
        Render a 360-degree view of the scene.

        Args:
            path (str): Path to the scene file.
            output_path (str): Path to save the rendered video.
            scene_dims (list): Dimensions of the scene (width, depth, height).
            scene_center (list): Center of the scene.
        """
        cam_ob = self.init(path)
        scene_dims = self.scene_size
        scene_center = self.scene_center
        cx, cz, cy = scene_center

        W,D,H = scene_dims
        cam_radius = 3 * np.sqrt((W / 2) ** 2 + (D / 2) ** 2)
        animate_camera(cam_ob, cam_radius, scene_center)
        setup_renderer_video(output_path, self.resolution_x, self.resolution_y, self.frame_rate, self.samples)
        render_video()
        
# renderer = SceneRenderer(resolution_x=512, resolution_y=512, samples=5)
# renderer.render_from_corners("/Users/kunalgupta/Documents/opttool2.blend", ["/Users/kunalgupta/Documents/packages/sceneprogrenderer/output1.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output2.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output3.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output4.png"])
# renderer.render_360("/Users/kunalgupta/Documents/opttool2.blend", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output.mp4")
# renderer.render_from_edge_midpoints("/Users/kunalgupta/Documents/opttool2.blend", ["/Users/kunalgupta/Documents/packages/sceneprogrenderer/output1.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output2.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output3.png", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output4.png"])
# renderer.render("/Users/kunalgupta/Documents/opttool2.blend", "/Users/kunalgupta/Documents/packages/sceneprogrenderer/output.png")