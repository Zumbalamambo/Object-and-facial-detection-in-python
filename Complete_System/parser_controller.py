import sys
import os
import threading
import time
import cv2
import shared_variables
import types
from subprocess import call

class parse_controller(threading.Thread):

    parser = None
    status_array = list() # list threads
    func_info = (('help, h', 'show how to use all commands'),
                 ('helpsh', 'open python help shell'),
                 ('start', 'start function in system. Syntax Start -func -sort id. Ex start -read -web 0'),
                 ('camera', 'see cameras in system and if active'),
                 ('imshow', 'see -web 0-camnr., -gige, -ip'),
                 ('set', '-r results to show -skincolor 0/1, -skintemp 0/1, -breath 0/1, -s system reference'),
                 ('showall', 'show all cameras and results'),
                 ('showdb', 'show total database'),
                 ('stop', 'stop a system, send with reference'),
                 ('close', 'close instances for -web 0-camnr., -gige, -ip : -all close all threads'),
                 ('status', 'show system status: Active Cameras, System Count, Syatem Reference'),
                 ('kill', 'Stop running thread'),
                    ('clear', 'clear terminal'))

    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables

    def run(self):
        args = None
        input_str = "";
        print ("----- Program -----")
        print (" type help or h to see functions")
        while True:

            input_str = input('Program>')
            input_str_array = input_str.split(' ')

            if self.get_first_arg(input_str_array) is not None:

                if self.run_command(input_str_array):
                    pass
                else:
                    print("No command : " + input_str + " (for help type h)")

            #print(help(shared_variables))
            #print(dir(shared_variables))


    def get_first_arg(self,arr):
        for s in arr:
            if len(s) > 0:
                return s

        return None


    def get_all_arg(self,arr):

        res = list()
        for s in arr:
            if len(s) > 0 :
                res.append(s)

        return res


    def run_command(self,arr):

        arg_arr = self.get_all_arg(arr);
        s = arg_arr[0]

        if s == "help" or s == "h":
            self.call_help()
            return True
        elif s == "helpsh":
            help()
            pass
        elif s == "clear":
            self.call_clear()
            return True
        elif s == "status":
            self.call_status()
            return True
        elif s == "start":
            self.call_start(arg_arr)
            return True
        elif s == "imshow":
            self.call_show(arg_arr)
            return True
        elif s == "close":
            self.call_close(arg_arr)
            return True
        else:
            return False

#
# --------- CALL FUNCTION DOWN HERE -----------
#

    def call_start(self, args = None):

        if args is not None :
            if len(args) >= 3:

                if args[1] == "-read":
                    if args[2] == "-web":
                        self.status_array.append(["web", args[3]])
                        self.shared_variables.start_intern_camera_stream(int(args[3]))
                    elif args[2] == "-gige":
                        self.status_array.append(list("gige", args[3]))
                        #self.shared_variables.start_intern_camera_stream(int(args[2]))
                    elif args[2] == "-ip":
                        self.status_array.append(list("ip", args[3]))
                        #self.shared_variables.start_intern_camera_stream(int(args[2]))

                elif args[1] == "-detect":
                    if args[2] == "-dlib":
                        self.shared_variables.start_dlib_detection_thread(0)
                        pass
                    elif args[2] == "-tf":
                        self.shared_variables.start_tf_detection_thread(0)
                        pass

                else:
                    print("No such parameter")


        else:
            print("No parameters!")

        pass

    def call_close(self, args):
         if args is not None:
            if len(args) > 2:

                if args[1] == "-web":

                    self.status_array.remove()
                    self.shared_variables.start_camera_thread()
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-gige":
                    self.status_array.append(list("show gige", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-ip":
                    self.status_array.append(list("show ip", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))

                else:
                    print("No such parameter")
         else:
            print("No parameters!")


    def call_show(self, args):
         if args is not None:
            if len(args) >= 2:

                if args[1] == "-web":

                    self.status_array.append(["show web", args[2]])
                    print("gere")
                    self.shared_variables.start_camera_thread()
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-gige":
                    self.status_array.append(list("show gige", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-ip":
                    self.status_array.append(list("show ip", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))

                else:
                    print("No such parameter")
         else:
            print("No parameters!")

    def call_kill(self):
        pass

    def call_status(self):

        print()
        print("Running threads:")
        print()

        for s in self.status_array:
            string = ""
            for i in s:
                string += i + " "

            print(string)

        pass


    def call_help(self):

        print()
        print("This is program, see functions below. ")
        print()
        print("Help: ")


        for s in self.func_info:
            print( s[0]   + "\t\t" + s[1])

        print()


    def call_clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
        pass



# test
#thread = parse_controller()
#thread.start()
