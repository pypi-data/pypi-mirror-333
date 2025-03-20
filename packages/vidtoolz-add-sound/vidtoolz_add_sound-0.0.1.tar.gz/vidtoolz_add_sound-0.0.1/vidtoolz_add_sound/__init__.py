import vidtoolz

from vidtoolz_add_sound.add_sound import add_audio_to_video, write_clip

def create_parser(subparser):
    parser = subparser.add_parser("addsound", description="Add sound to a video")
    # Add subprser arguments here.
    parser.add_argument("video", type=str, help="Video file to which sound has to be added.")
    parser.add_argument("audio", type=str, help="Sound file to add")
    parser.add_argument("-s", "--start-time", type=int, default=3, help="Time in seconds where audio has to be added")
    parser.add_argument("-o", "--output-path", type=str, help="Sound file to add")
    return parser


class ViztoolzPlugin:
    """ Add sound to a video """
    __name__ = "addsound"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)
    
    def run(self, args):
        clip = add_audio_to_video(args.video, args.audio, args.start_time)
        write_clip(clip, args.output_path)
        print(f"{args.output_path} written.")

    
    def hello(self, args):
        # this routine will be called when "vidtoolz "addsound is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")

addsound_plugin = ViztoolzPlugin()
