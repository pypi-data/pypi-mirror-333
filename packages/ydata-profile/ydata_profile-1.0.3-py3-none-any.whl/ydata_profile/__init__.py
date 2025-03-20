def run_ydata_profile():
    import os
    path_file = os.path.realpath(__file__)
    folder_file = os.path.dirname(path_file)
    os.chdir(folder_file)
    os.system("streamlit run streamlit_app.py")
