import argparse
import mycam


def main():
    # Define the parser for cli arguments
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')

    parser.add_argument('-b', '--blur',
                        action='store_true',
                        default=argparse.SUPPRESS,
                        help='Blur background'
                        )

    parser.add_argument("-i", "--image",
                        nargs='?',
                        const='data/images/img1.jpg',
                        default=argparse.SUPPRESS,
                        metavar='IMAGE_FILE',
                        help='Replace background with image'
                        )

    parser.add_argument('-v', '--video',
                        nargs='?',
                        const='data/videos/vid1.mp4',
                        default=argparse.SUPPRESS,
                        metavar='VIDEO_FILE',
                        help='Replace background with video'
                        )

    args = parser.parse_args()
    config = vars(args)

    # Call the camera function with the desired configurations
    mycam.play(config)


if __name__ == '__main__':
    main()
