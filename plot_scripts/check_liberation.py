import matplotlib.font_manager
fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
liberation = [f for f in fonts if 'Liberation' in f]
print('Liberation fonts:', liberation)
# also check for Arial
arial = [f for f in fonts if 'Arial' in f]
print('Arial fonts:', arial)