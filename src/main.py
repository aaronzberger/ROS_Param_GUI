'''
Edit ROS Param Server values via a GUI
Usage: main.py [NAMESPACES]
'''

import tkinter as tk
import rospy
import sys

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

APPROX_ROW_HEIGHT = 45

# Name: Min, Max, Tick
PARAM_BOUNDS = {'WinSize': [0, 10, 1],
                'MinDisparity': [-2048, 2048, 1],
                'MaxDisparity': [0, 1024, 16],
                'UniqueRatio': [0, 100, 1],
                'PreFilterCap': [0, 63, 1],
                'SpeckleWinSize': [0, 1000, 1],
                'SpeckleRange': [0, 31, 1],
                'Cx': [0, 4000, 1],
                'Cy': [0, 4000, 1],
                'Disp12MaxDisff': [0, 128, 1],
                'ResizeImgFlag': [0, 1, 1],
                'ResizeImgVal': [0, 1, 0.01]}

if __name__ == '__main__':
    rospy.init_node('ROS_Param_Server_GUI')

    namespaces = None
    if len(sys.argv) > 1:
        namespaces = sys.argv[1:]

    label_width = 20

    master = tk.Tk()
    master.title('ROS Param Server GUI')
    width, height = master.winfo_screenwidth(), master.winfo_screenheight()

    master.geometry('+0+0')

    def setup_param_slider(row, param_name):
        master.update()
        if master.winfo_height() > height - master.winfo_rooty() - APPROX_ROW_HEIGHT:
            print(FAIL + 'Can not add param to the GUI. There is not enough space: {}{}'.format(
                ENDC, param_name) + ENDC)
            return -1

        initial_param_val = float(rospy.get_param(param_name))

        options = None
        for key in PARAM_BOUNDS:
            if param_name in key or key in param_name:
                options = PARAM_BOUNDS[key]
                break
        if options is None:
            options = [0, 1000, 1]

        def entry_callback(event):
            rospy.set_param(param_name, float(entry.get()))
            slider.set(float(entry.get()))
        
        def slider_callback(event):
            rospy.set_param(param_name, float(slider.get()))
            entry.delete(0, tk.END)
            entry.insert(0, int(slider.get()) if \
                int(slider.get()) == float(slider.get()) else float(slider.get()))

        label = tk.Label(text=param_name, anchor=tk.NE, relief=tk.RIDGE,
                         width=label_width, padx=10)

        slider = tk.Scale(master, from_=options[0], to=options[1], resolution=options[2],
                          orient=tk.HORIZONTAL, width=20, length=600, command=slider_callback)
        entry = tk.Entry(master, relief=tk.RIDGE)
        entry.bind("<Return>", entry_callback)

        start_label = tk.Label(text=options[0], font=("Helvetica", "12", "italic"), padx=10)
        end_label = tk.Label(text=options[1], font=("Helvetica", "12", "italic"), padx=10)

        slider.set(initial_param_val)
        entry.insert(0, int(initial_param_val) if \
            int(initial_param_val) == float(initial_param_val) else float(initial_param_val))

        label.grid(row=row, column=0, sticky='s')
        start_label.grid(row=row, column=1, sticky='s')
        slider.grid(row=row, column=2, sticky='s')
        end_label.grid(row=row, column=3, sticky='s')
        entry.grid(row=row, column=4, sticky='s')

        row += 1

    param_names = rospy.get_param_names()

    editable_param_names = []

    for param in param_names:
        try:
            param_val = float(rospy.get_param(param))
            label_width = max(label_width, len(param))
            editable_param_names.append(param)
        except:
            pass

    in_namespace_params = []
    params_per_ns = dict()

    if namespaces is not None:
        for param in editable_param_names:
            for ns in namespaces:
                if ns in param:
                    in_namespace_params.append(param)
                    if ns not in params_per_ns:
                        params_per_ns[ns] = 1
                    else:
                        params_per_ns[ns] += 1
                    continue

    max_len = max([len(ns) for ns in namespaces])

    print('Using the following namespaces:')
    for ns in namespaces:
        print('\t{}{}{}: {} editable params'.format(
            OKGREEN if ns in params_per_ns else FAIL, ns.rjust(max_len),
            ENDC, 0 if ns not in params_per_ns else params_per_ns[ns]))
    print('')

    row = 0
    num_succeed = 0
    for param in sorted(in_namespace_params):
        return_val = setup_param_slider(row, param)
        if return_val != -1:
            num_succeed += 1
            row += 1

    print('{}Added {}{}/{} ROS parameters to the GUI{}'.format(
        OKGREEN if num_succeed == len(in_namespace_params) else WARNING,
        'only ' if num_succeed < len(in_namespace_params) else '',
        num_succeed, len(in_namespace_params), ENDC))
    master.update()

    tk.mainloop()