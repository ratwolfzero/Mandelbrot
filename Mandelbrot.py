import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import time
import resource

def validate_input(prompt, input_type=float, check_positive_non_zero=False, min_value=None):
    while True:
        user_input = input(prompt)
        try:
            value = input_type(user_input)
            if check_positive_non_zero and value <= 0:
                print('Invalid input. The value must be a positive non-zero number.')
                continue
            if min_value is not None and value < min_value:
                print(f'Invalid input. The value should be at least {min_value}.')
                continue
            return value
        except ValueError:
            print(f'Invalid input. Please enter a valid {input_type.__name__} value.')

def get_mandelbrot_parameters():
    width = validate_input('Enter image width: ', int, check_positive_non_zero=True, min_value=100)
    height = validate_input('Enter image height: ', int, check_positive_non_zero=True, min_value=100)
    max_iter = validate_input('Enter max iterations: ', int, check_positive_non_zero=True, min_value=10)
    return {'width': width, 'height': height, 'max_iter': max_iter}


@njit
def compute_mandelbrot_set(width, height, max_iter, x_min, x_max, y_min, y_max):
    # Create an empty image (this will hold the iteration counts)
    image = np.zeros((height, width), dtype=np.uint64)
    
    # Scale factors for mapping complex plane to image space
    scale_x = (x_max - x_min) / (width - 1)
    scale_y = (y_max - y_min) / (height - 1)
    
    # Iterate over the pixel grid
    for i in range(height):
        for j in range(width):
            c = complex(x_min + j * scale_x, y_min + i * scale_y)
            z = 0.0j  # Start with z = 0
            iteration = 0
            # Iterate and check if the point escapes
            while abs(z) <= 2.0 and iteration < max_iter:
                z = z*z + c
                iteration += 1
            # Assign black (0) to points that belong to the Mandelbrot set (max_iter reached)
            if iteration == max_iter:
                image[i, j] = 0  # Black for Mandelbrot set points
            else:
                image[i, j] = iteration
    
    return image


def render_mandelbrot_image(image, params, color_map, x_min, x_max, y_min, y_max):
    # Render the Mandelbrot image
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    
    # Display the image with specified limits
    img = ax.imshow(image, cmap=color_map, origin='lower', extent=(x_min, x_max, y_min, y_max), interpolation='none')

    ax.set_title(f'Mandelbrot Set\nMax Iterations: {params["max_iter"]}')
    ax.set_xlabel('Re(c)')
    ax.set_ylabel('Im(c)')

    # Create the colorbar
    cbar = fig.colorbar(img, ax=ax, location='bottom')
    cbar.set_label('Iterations to Escape')

    plt.tight_layout()
    plt.show()
    

def main(image_size=(1000, 1000), color_map='hot'):
    try:
        params = get_mandelbrot_parameters()
        
        # Time the process
        start_time = time.process_time()
        
        # Compute the Mandelbrot set
        x_min, x_max, y_min, y_max = -2.0, 1.0, -1.5, 1.5
        image = compute_mandelbrot_set(params['width'], params['height'], params['max_iter'], x_min, x_max, y_min, y_max)
        
        # Render the result
        render_mandelbrot_image(image, params, color_map, x_min, x_max, y_min, y_max)
        
        # End the time measurement
        end_time = time.process_time()

        # CPU time used
        cpu_time_used = end_time - start_time

        # Memory used
        memMb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0

        print(f'CPU Time: {cpu_time_used:.2f} seconds')
        print(f'Memory Used: {memMb:.2f} MB')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()




