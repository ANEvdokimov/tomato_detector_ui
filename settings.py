class Settings:
    minH = 0
    minS = 0
    minV = 0
    maxH = 179
    maxS = 255
    maxV = 255

    whiteBalance = False
    contrast = False

    filterByCircularity = False
    minCircularity = 0.0
    maxCircularity = 1.0

    filterByConvexity = False
    minConvexity = 0.0
    maxConvexity = 1.0

    filterByInertia = False
    minInertia = 0.0
    maxInertia = 1.0

    filterByArea = False
    minArea = 0.0
    maxArea = 1.0

    splitFruit = False

    def __init__(self, minH, minS, minV, maxH, maxS, maxV, whiteBalance, contrast, filterByCircularity, minCircularity,
                 maxCircularity, filterByConvexity, minConvexity, maxConvexity, filterByInertia, minInertia,
                 maxInertia, filterByArea, minArea, maxArea, splitFruit):
        self.minH = minH
        self.minS = minS
        self.minV = minV
        self.maxH = maxH
        self.maxS = maxS
        self.maxV = maxV

        self.whiteBalance = whiteBalance
        self.contrast = contrast

        self.filterByCircularity = filterByCircularity
        self.minCircularity = minCircularity
        self.maxCircularity = maxCircularity

        self.filterByConvexity = filterByConvexity
        self.minConvexity = minConvexity
        self.maxConvexity = maxConvexity

        self.filterByInertia = filterByInertia
        self.minInertia = minInertia
        self.maxInertia = maxInertia

        self.filterByArea = filterByArea
        self.minArea = minArea
        self.maxArea = maxArea

        self.splitFruit = splitFruit
