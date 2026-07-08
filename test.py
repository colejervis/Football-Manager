
# ENSURES KEY ATTRIBUTES GROW RAPIDLY
def high_curve(x):
    return (x / 10) ** 1.3 * 10

# ENSURES DECENTLY IMPORTANT ATTRIBUTES GROW EXPONENTIALLY
def mid_curve(x):
    return (x / 10) ** 1.05 * 10

print(high_curve(10))