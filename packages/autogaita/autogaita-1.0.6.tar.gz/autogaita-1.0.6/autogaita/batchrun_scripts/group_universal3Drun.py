import autogaita


def group_universal3Drun():
    """
    Batchrun script to run AutoGaitA Group for Results obtained with AutoGaitA Universal 3D.
    folderinfo & cfg dictionaries must be configured as explained in our documentation. See the "AutoGaitA without the GUI" section of our documentation for references to in-depth explanations to all dictionary keys (note that each key of dicts corresponds to some object in the AutoGaitA Group GUI)
    """
    # loop over legs - currently no option to do both legs in a single run
    cfg = {}
    # folderinfo
    # => Note that length of folderinfo's group_names & group_dirs lists determines #    how many groups are compared.
    # => Also note that indices must correspond (i.e., idx #    1's name will be #    used for dataset stored in group_dir's idx 1)
    folderinfo = {}
    folderinfo["group_names"] = [
        "crawling",
        "sideways",
        "walking",
        "jogging",
        "jumping_jack",
        "vertical_jumping",
    ]
    folderinfo["group_dirs"] = [
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/crawling/Results/",
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/sideways/Results/",
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/walking/Results/",
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/jogging/Results/",
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/jumping_jack/Results/",
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/vertical_jumping/Results/",
    ]
    folderinfo["results_dir"] = (
        "/Users/mahan/sciebo/Research/AutoGaitA/Showcase 3/MOVI/First Analysis/gaita prepared/group/"
    )
    folderinfo["load_dir"] = ""
    # cfg
    cfg["do_permtest"] = True
    cfg["do_anova"] = True
    cfg["permutation_number"] = 10000
    cfg["PCA_n_components"] = 10
    cfg["PCA_custom_scatter_PCs"] = ""
    cfg["PCA_save_3D_video"] = True
    cfg["PCA_bins"] = ""
    cfg["stats_threshold"] = 0.05
    cfg["plot_SE"] = False
    cfg["color_palette"] = "Set2"
    cfg["legend_outside"] = True
    cfg["dont_show_plots"] = True
    cfg["anova_design"] = "Mixed ANOVA"
    cfg["which_leg"] = "right"
    cfg["PCA_variables"] = [
        "Head Y",
        "Head Z",
        "Hip Y",
        "Hip Z",
        "Pelvis Y",
        "Pelvis Z",
        "Thorax Y",
        "Thorax Z",
        "Ankle, left Y",
        "Ankle, left Z",
        "Elbow, left Y",
        "Elbow, left Z",
        "Hip, left Y",
        "Hip, left Z",
        "Hand, left Y",
        "Hand, left Z",
        "Knee, left Y",
        "Knee, left Z",
        "Shoulder, left Y",
        "Shoulder, left Z",
        "Wrist, left Y",
        "Wrist, left Z",
        "Foot, left Y",
        "Foot, left Z",
        "Ankle, right Y",
        "Ankle, right Z",
        "Elbow, right Y",
        "Elbow, right Z",
        "Hip, right Y",
        "Hip, right Z",
        "Hand, right Y",
        "Hand, right Z",
        "Knee, right Y",
        "Knee, right Z",
        "Shoulder, right Y",
        "Shoulder, right Z",
        "Wrist, right Y",
        "Wrist, right Z",
        "Foot, right Y",
        "Foot, right Z",
        "Ankle, left Angle",
        "Knee, left Angle",
        "Elbow, left Angle",
        "Foot, left Velocity",
        "Foot, left Acceleration",
        "Ankle, left Velocity",
        "Ankle, left Acceleration",
        "Knee, left Velocity",
        "Knee, left Acceleration",
        "Hip Velocity",
        "Hip Acceleration",
        "Pelvis Velocity",
        "Pelvis Acceleration",
        "Shoulder, left Velocity",
        "Shoulder, left Acceleration",
        "Head Velocity",
        "Head Acceleration",
        "Ankle, left Angle Velocity",
        "Ankle, left Angle Acceleration",
        "Knee, left Angle Velocity",
        "Knee, left Angle Acceleration",
        "Elbow, left Angle Velocity",
        "Elbow, left Angle Acceleration",
        "Ankle, right Angle",
        "Knee, right Angle",
        "Elbow, right Angle",
        "Foot, right Velocity",
        "Foot, right Acceleration",
        "Ankle, right Velocity",
        "Ankle, right Acceleration",
        "Knee, right Velocity",
        "Knee, right Acceleration",
        "Shoulder, right Velocity",
        "Shoulder, right Acceleration",
        "Ankle, right Angle Velocity",
        "Ankle, right Angle Acceleration",
        "Knee, right Angle Velocity",
        "Knee, right Angle Acceleration",
        "Elbow, right Angle Velocity",
        "Elbow, right Angle Acceleration",
    ]
    cfg["stats_variables"] = []
    # run
    autogaita.group(folderinfo, cfg)


# %% what happens if we just hit run
if __name__ == "__main__":
    group_universal3Drun()
