
import sply

class sp_example_conf:
    def __init__(self, show, mode, model_id, seed, temp, num_ctx):
        self.show = show
        self.mode = mode
        self.model_id = model_id
        self.seed = seed
        self.temp = temp
        self.num_ctx = num_ctx
        self.prompt = ""

    def parse_args(self, args):
        for arg in args[1:]:
            if arg.find("--help") == 0:
                print(f"usage: {args[0]}"\
                    f" [--help]"\
                    f" [mode=\"plain\"|\"think\"|\"im\"|\"im_think\" ({self.mode})]"\
                    f" [model_id=\"model_id\" ({self.model_id})]"\
                    f" [seed=\"seed\" ({self.seed})]"\
                    f" [temp=\"temp\" ({self.temp})]"\
                    f" [num_ctx=\"num_ctx\" ({self.num_ctx})]"\
                    f" [show=\"True|False\" ({self.show})]"\
                    "")
                return False
            elif arg.find("mode=") == 0:
                self.mode = arg[5:]
            elif arg.find("model_id=") == 0:
                self.model_id = arg[9:]
            elif arg.find("seed=") == 0:
                self.seed = int(arg[5:])
            elif arg.find("temp=") == 0:
                self.temp = float(arg[5:])
            elif arg.find("num_ctx=") == 0:
                self.num_ctx = int(arg[8:])
            elif arg.find("show=") == 0:
                self.show = True if arg[5:] == "True" else False

        if self.mode == "plain":
            self.prompt = sply.sp.create_prompt_default()
        elif self.mode == "think":
            self.prompt = sply.sp.create_prompt_think()
        elif self.mode == "im":
            self.prompt = sply.sp.create_prompt_im()
        elif self.mode == "im_think":
            self.prompt = sply.sp.create_prompt_im_think()

        return True

