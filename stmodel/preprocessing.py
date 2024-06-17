

def clean_gt(gt):
    return [pred for pred in gt if pred[1]!="###"]

def clean_GTs(GTs):
    return [clean_gt(gt) for gt in GTs]

def superResolution(image):
    return image

def color_normalize(image):
    return image