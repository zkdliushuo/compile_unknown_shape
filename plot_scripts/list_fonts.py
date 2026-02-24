import matplotlib.font_manager
fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
print('Available fonts:', len(fonts))
for f in sorted(set(fonts))[:20]:
    print(f)