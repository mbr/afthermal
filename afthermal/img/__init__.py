import os

# these images have been created with gimp; nd is the normally dithered
# (Floyd-Steinberg) version, while rb uses the "reduce bleeding" setting
LENA_ND_FN = os.path.join(os.path.dirname(__file__), 'lena-nd.png')
LENA_RB_FN = os.path.join(os.path.dirname(__file__), 'lena-rb.png')
